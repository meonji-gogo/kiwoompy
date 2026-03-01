"""실시간 데이터 모듈 — WebSocket 기반 실시간 구독 관리."""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Callable, Coroutine
from typing import Any

import websockets
from websockets.asyncio.client import connect, ClientConnection

from kiwoompy.api import KiwoomApi
from kiwoompy.exceptions import KiwoomApiError
from kiwoompy.models import RealtimeEvent

logger = logging.getLogger(__name__)

_WS_URLS: dict[str, str] = {
    "real": "wss://api.kiwoom.com:10000/api/dostk/websocket",
    "demo": "wss://mockapi.kiwoom.com:10000/api/dostk/websocket",
}

# 최대 구독 건수 (키움 공식 정책)
_MAX_SUBSCRIPTIONS = 100

# 재연결 백오프 (초)
_RECONNECT_WAIT_MIN = 1.0
_RECONNECT_WAIT_MAX = 30.0

type RealtimeCallback = Callable[[RealtimeEvent], Coroutine[Any, Any, None]]
"""실시간 이벤트 콜백 타입. ``RealtimeEvent``를 인자로 받는 async 함수."""


class _Subscription:
    """단일 구독 정보를 담는 내부 클래스."""

    __slots__ = ("type", "items", "callback", "grp_no", "refresh")

    def __init__(
        self,
        type: str,
        items: list[str],
        callback: RealtimeCallback,
        grp_no: str,
        refresh: str,
    ) -> None:
        self.type = type
        self.items = list(items)
        self.callback = callback
        self.grp_no = grp_no
        self.refresh = refresh


class KiwoomRealtime:
    """키움 REST API 실시간 데이터 WebSocket 클라이언트.

    단일 WebSocket 연결을 유지하면서 여러 TR 타입의 실시간 데이터를 구독한다.
    수신된 메시지는 TR 타입별로 등록된 콜백에 라우팅된다.

    **구독 제한**: 최대 100건 (키움 공식 정책).

    **재연결**: 연결이 끊기면 지수 백오프로 자동 재연결하고 기존 구독을 복원한다.

    Args:
        api: 접근토큰·환경 정보를 담은 ``KiwoomApi`` 인스턴스.
        env: 환경 구분. ``"real"`` (운영) 또는 ``"demo"`` (모의투자).
        reconnect: 자동 재연결 여부. 기본값 ``True``.

    Example:
        >>> import asyncio
        >>> from kiwoompy import KiwoomApi, KiwoomAuth, KiwoomRealtime, RealtimeEvent
        >>>
        >>> async def on_trade(event: RealtimeEvent) -> None:
        ...     price = event.values.get("10", "")
        ...     print(f"[{event.item}] 현재가={price}")
        >>>
        >>> async def main():
        ...     api = KiwoomApi(env="real")
        ...     KiwoomAuth(api).issue_token(appkey="...", secretkey="...")
        ...     async with KiwoomRealtime(api, env="real") as rt:
        ...         await rt.subscribe("0B", items=["005930", "000660"], callback=on_trade)
        ...         await asyncio.sleep(60)
        >>>
        >>> asyncio.run(main())
    """

    def __init__(
        self,
        api: KiwoomApi,
        env: str = "demo",
        *,
        reconnect: bool = True,
    ) -> None:
        self._api = api
        self._ws_url = _WS_URLS[env]
        self._reconnect = reconnect

        self._subscriptions: dict[str, _Subscription] = {}  # type → _Subscription
        self._sub_count: int = 0

        self._ws: ClientConnection | None = None
        self._recv_task: asyncio.Task[None] | None = None
        self._connected = asyncio.Event()
        self._closed = False

    # ------------------------------------------------------------------ #
    # 공개 API
    # ------------------------------------------------------------------ #

    async def connect(self) -> None:
        """WebSocket 연결을 시작하고 백그라운드 수신 루프를 실행한다.

        이미 연결된 상태면 아무 동작도 하지 않는다.

        Raises:
            KiwoomApiError: WebSocket 연결 실패.
        """
        if self._recv_task is not None and not self._recv_task.done():
            return
        self._closed = False
        self._recv_task = asyncio.create_task(self._run_loop(), name="kiwoom-realtime")
        await self._connected.wait()

    async def subscribe(
        self,
        type: str,
        items: list[str],
        callback: RealtimeCallback,
        *,
        grp_no: str = "1",
        refresh: str = "1",
    ) -> None:
        """실시간 데이터 구독을 등록한다.

        동일 ``type``이 이미 등록된 경우 기존 구독을 덮어쓴다(items·callback 갱신).

        Args:
            type: 실시간 항목 TR명. (예: ``"0B"`` — 주식체결, ``"00"`` — 주문체결)
            items: 구독할 종목코드 목록. 계좌 기반 타입(``"00"``, ``"04"``)은 ``[""]`` 전달.
            callback: 이벤트 수신 시 호출할 async 콜백.
            grp_no: 그룹번호. 기본값 ``"1"``.
            refresh: 기존 등록 유지 여부. ``"1"``: 유지 (기본값), ``"0"``: 해지 후 재등록.

        Raises:
            KiwoomApiError: 최대 구독 수(100건) 초과 또는 WebSocket 미연결.
        """
        is_new = type not in self._subscriptions
        if is_new and self._sub_count >= _MAX_SUBSCRIPTIONS:
            raise KiwoomApiError(
                f"실시간 구독 한도 초과: 최대 {_MAX_SUBSCRIPTIONS}건까지 구독 가능합니다."
            )

        sub = _Subscription(type, items, callback, grp_no, refresh)
        self._subscriptions[type] = sub
        if is_new:
            self._sub_count += 1

        if self._ws is not None:
            await self._send_reg(sub)

    async def unsubscribe(self, type: str, items: list[str] | None = None) -> None:
        """실시간 데이터 구독을 해제한다.

        Args:
            type: 해제할 실시간 항목 TR명.
            items: 해제할 종목코드 목록. ``None``이면 해당 타입 전체 해제.

        Raises:
            KiwoomApiError: WebSocket 미연결.
        """
        if type not in self._subscriptions:
            return

        sub = self._subscriptions[type]
        target_items = items if items is not None else sub.items

        if self._ws is not None:
            await self._send_remove(type, target_items, sub.grp_no)

        if items is None or set(items) >= set(sub.items):
            del self._subscriptions[type]
            self._sub_count -= 1
        else:
            remaining = [i for i in sub.items if i not in items]
            self._subscriptions[type] = _Subscription(
                type, remaining, sub.callback, sub.grp_no, sub.refresh
            )

    async def close(self) -> None:
        """WebSocket 연결을 종료하고 수신 루프를 멈춘다."""
        self._closed = True
        self._connected.clear()
        if self._recv_task is not None:
            self._recv_task.cancel()
            try:
                await self._recv_task
            except asyncio.CancelledError:
                pass
        if self._ws is not None:
            await self._ws.close()
            self._ws = None

    # ------------------------------------------------------------------ #
    # 컨텍스트 매니저
    # ------------------------------------------------------------------ #

    async def __aenter__(self) -> KiwoomRealtime:
        """컨텍스트 진입 시 WebSocket 연결을 시작한다."""
        await self.connect()
        return self

    async def __aexit__(self, *_: object) -> None:
        """컨텍스트 종료 시 연결을 닫는다."""
        await self.close()

    # ------------------------------------------------------------------ #
    # 내부 구현
    # ------------------------------------------------------------------ #

    def _auth_headers(self) -> dict[str, str]:
        """Authorization 헤더를 반환한다."""
        return self._api.get_auth_header()

    async def _send_reg(self, sub: _Subscription) -> None:
        """REG 메시지를 현재 WebSocket 연결에 전송한다."""
        if self._ws is None:
            return
        payload = {
            "trnm": "REG",
            "grp_no": sub.grp_no,
            "refresh": sub.refresh,
            "data": [{"item": sub.items, "type": [sub.type]}],
        }
        await self._ws.send(json.dumps(payload))

    async def _send_remove(self, type: str, items: list[str], grp_no: str) -> None:
        """REMOVE 메시지를 현재 WebSocket 연결에 전송한다."""
        if self._ws is None:
            return
        payload = {
            "trnm": "REMOVE",
            "grp_no": grp_no,
            "data": [{"item": items, "type": [type]}],
        }
        await self._ws.send(json.dumps(payload))

    async def _restore_subscriptions(self) -> None:
        """재연결 후 기존 구독을 모두 서버에 다시 등록한다."""
        for sub in list(self._subscriptions.values()):
            await self._send_reg(sub)

    async def _handle_message(self, raw: dict) -> None:
        """수신된 메시지를 파싱해 콜백에 라우팅한다."""
        trnm = raw.get("trnm", "")

        if trnm in ("REG", "REMOVE"):
            rc = raw.get("return_code")
            if rc is not None and rc != 0:
                msg = raw.get("return_msg", "등록/해지 오류")
                logger.warning("실시간 등록/해지 오류 (return_code=%s): %s", rc, msg)
            return

        if trnm != "REAL":
            return

        for entry in raw.get("data", []):
            event_type = entry.get("type", "")
            sub = self._subscriptions.get(event_type)
            if sub is None:
                continue

            event = RealtimeEvent(
                type=event_type,
                name=entry.get("name", ""),
                item=entry.get("item", ""),
                values=dict(entry.get("values", {})),
            )
            try:
                await sub.callback(event)
            except Exception:
                logger.exception("실시간 콜백 처리 중 예외 발생 (type=%s)", event_type)

    async def _run_loop(self) -> None:
        """WebSocket 수신 루프. 재연결 로직 포함."""
        wait = _RECONNECT_WAIT_MIN
        while not self._closed:
            try:
                async with connect(
                    self._ws_url,
                    additional_headers=self._auth_headers(),
                ) as ws:
                    self._ws = ws
                    self._connected.set()
                    wait = _RECONNECT_WAIT_MIN  # 연결 성공 시 대기 초기화
                    logger.info("실시간 WebSocket 연결됨: %s", self._ws_url)

                    await self._restore_subscriptions()

                    async for raw_msg in ws:
                        if self._closed:
                            break
                        try:
                            raw: dict = json.loads(raw_msg)
                            await self._handle_message(raw)
                        except json.JSONDecodeError:
                            logger.warning("WebSocket 메시지 파싱 실패: %r", raw_msg)

            except asyncio.CancelledError:
                break
            except websockets.exceptions.WebSocketException as exc:
                logger.warning("WebSocket 연결 끊김: %s", exc)
            except Exception as exc:
                logger.warning("실시간 루프 오류: %s", exc)
            finally:
                self._ws = None
                self._connected.clear()

            if self._closed or not self._reconnect:
                break

            logger.info("%.1f초 후 재연결 시도...", wait)
            await asyncio.sleep(wait)
            wait = min(wait * 2, _RECONNECT_WAIT_MAX)
            self._connected.clear()
