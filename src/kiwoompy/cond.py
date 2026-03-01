"""조건검색 모듈 — WebSocket 기반 조건검색 목록 조회·일반 검색·실시간 검색·해제."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable, Coroutine
from typing import Any

import websockets
from websockets.asyncio.client import connect

from kiwoompy.api import KiwoomApi
from kiwoompy.exceptions import KiwoomApiError
from kiwoompy.models import (
    ConditionItem,
    ConditionList,
    ConditionRealtimeItem,
    ConditionRealtimeValues,
    ConditionSearchItem,
    ConditionSearchResult,
    ConditionStopResult,
)

logger = logging.getLogger(__name__)

_WS_PATHS: dict[str, str] = {
    "real": "wss://api.kiwoom.com:10000/api/dostk/websocket",
    "demo": "wss://mockapi.kiwoom.com:10000/api/dostk/websocket",
}

# 조건검색 속도 제한 (5회/초)
_COND_RPS = 5.0
# 동일 조건식 최소 재요청 간격 (60초)
_SAME_COND_COOLDOWN = 60.0


def _check(raw: dict) -> None:
    """응답의 return_code를 확인하고 오류 시 예외를 발생시킨다.

    Args:
        raw: WebSocket 응답 딕셔너리.

    Raises:
        KiwoomApiError: return_code가 0이 아닌 경우.
    """
    rc = raw.get("return_code")
    if rc is not None and rc != 0:
        msg = raw.get("return_msg", "조건검색 오류")
        raise KiwoomApiError(f"조건검색 오류 (return_code={rc}): {msg}")


class _AsyncRateLimiter:
    """asyncio 기반 간단한 유량 제어기.

    초당 ``rps``건을 초과하지 않도록 호출 간격을 제어한다.

    Args:
        rps: 초당 최대 요청 수.
    """

    def __init__(self, rps: float) -> None:
        self._min_interval = 1.0 / rps
        self._last_called = 0.0

    async def acquire(self) -> None:
        """다음 요청을 허용할 때까지 필요하면 대기한다."""
        now = time.monotonic()
        wait = self._min_interval - (now - self._last_called)
        if wait > 0:
            await asyncio.sleep(wait)
        self._last_called = time.monotonic()


class KiwoomCond:
    """키움 REST API 조건검색 WebSocket 클라이언트.

    조건검색은 REST가 아닌 WebSocket(`wss://...`)으로 JSON 메시지를
    주고받는 방식이다. 영웅문4에서 만든 조건식 목록을 조회하고,
    일반/실시간 검색을 수행한다.

    **속도 제한**: 5회/초, 동일 조건식 1회/분

    Args:
        api: 접근토큰·환경 정보를 담은 ``KiwoomApi`` 인스턴스.
        env: 환경 구분. ``"real"`` (운영) 또는 ``"demo"`` (모의투자).

    Example:
        >>> import asyncio
        >>> from kiwoompy import KiwoomApi, KiwoomAuth, KiwoomCond
        >>> api = KiwoomApi(env="demo")
        >>> KiwoomAuth(api).issue_token(appkey="...", secretkey="...")
        >>> cond = KiwoomCond(api, env="demo")
        >>> result = asyncio.run(cond.condition_list())
        >>> print(result.items)
    """

    def __init__(self, api: KiwoomApi, env: str = "demo") -> None:
        self._api = api
        self._ws_url = _WS_PATHS[env]
        self._rate_limiter = _AsyncRateLimiter(_COND_RPS)
        # 조건식 일련번호 → 마지막 요청 시각 (1분 쿨다운)
        self._last_seq_called: dict[str, float] = {}

    def _auth_header(self) -> dict[str, str]:
        """Authorization 헤더를 반환한다."""
        return self._api.get_auth_header()

    async def _send_recv(self, payload: dict) -> dict:
        """WebSocket에 payload를 전송하고 단일 응답 메시지를 반환한다.

        Args:
            payload: 전송할 JSON 딕셔너리.

        Returns:
            서버 응답 딕셔너리.

        Raises:
            KiwoomApiError: WebSocket 연결·통신 오류 또는 응답 파싱 실패.
        """
        import json

        await self._rate_limiter.acquire()
        auth = self._auth_header()
        try:
            async with connect(
                self._ws_url,
                additional_headers=auth,
            ) as ws:
                await ws.send(json.dumps(payload))
                raw_msg = await ws.recv()
                return json.loads(raw_msg)  # type: ignore[return-value]
        except websockets.exceptions.WebSocketException as exc:
            raise KiwoomApiError(f"WebSocket 오류: {exc}") from exc
        except Exception as exc:
            raise KiwoomApiError(f"조건검색 통신 오류: {exc}") from exc

    def _check_cooldown(self, seq: str) -> None:
        """동일 조건식의 1분 쿨다운을 검사한다.

        Args:
            seq: 조건검색식 일련번호.

        Raises:
            KiwoomApiError: 동일 조건식을 1분 이내에 재요청하는 경우.
        """
        last = self._last_seq_called.get(seq)
        if last is not None:
            elapsed = time.monotonic() - last
            if elapsed < _SAME_COND_COOLDOWN:
                remain = _SAME_COND_COOLDOWN - elapsed
                raise KiwoomApiError(
                    f"조건식 {seq!r}는 {remain:.1f}초 후에 다시 요청할 수 있습니다. "
                    f"(동일 조건식 1회/분 제한)"
                )
        self._last_seq_called[seq] = time.monotonic()

    async def condition_list(self) -> ConditionList:
        """조건검색 목록을 조회한다 (ka10171).

        영웅문4에서 등록한 조건검색식의 일련번호와 이름 목록을 반환한다.
        실시간 조건검색 전에 먼저 호출해야 한다.

        Returns:
            조건검색식 목록을 담은 ``ConditionList``.

        Raises:
            KiwoomApiError: WebSocket 통신 오류 또는 API 오류.
        """
        raw = await self._send_recv({"trnm": "CNSRLST"})
        _check(raw)
        items = [
            ConditionItem(seq=row[0], name=row[1])
            for row in raw.get("data", [])
        ]
        return ConditionList(items=items)

    async def condition_search(
        self,
        seq: str,
        *,
        stex_tp: str = "K",
        cont_yn: str = "N",
        next_key: str = "",
    ) -> ConditionSearchResult:
        """조건검색 일반 조회를 요청한다 (ka10172).

        조건식에 해당하는 종목 목록을 1회성으로 조회한다.
        동일 조건식은 1분에 1회만 요청할 수 있다.

        Args:
            seq: 조건검색식 일련번호.
            stex_tp: 거래소구분 (기본값 ``"K"`` — KRX).
            cont_yn: 연속조회 여부. ``"Y"`` 또는 ``"N"`` (기본값).
            next_key: 연속조회키. 연속조회 시 이전 응답값 전달.

        Returns:
            검색 결과 종목 리스트와 페이지 정보를 담은 ``ConditionSearchResult``.

        Raises:
            KiwoomApiError: 1분 쿨다운 위반, WebSocket 오류 또는 API 오류.
        """
        self._check_cooldown(seq)
        payload = {
            "trnm": "CNSRREQ",
            "seq": seq,
            "search_type": "0",
            "stex_tp": stex_tp,
            "cont_yn": cont_yn,
            "next_key": next_key,
        }
        raw = await self._send_recv(payload)
        _check(raw)

        items = [
            ConditionSearchItem(
                stock_code=row.get("9001", ""),
                stock_name=row.get("302", ""),
                current_price=row.get("10", ""),
                change_sign=row.get("25", ""),
                change=row.get("11", ""),
                change_rate=row.get("12", ""),
                volume=row.get("13", ""),
                open_price=row.get("16", ""),
                high_price=row.get("17", ""),
                low_price=row.get("18", ""),
            )
            for row in raw.get("data", [])
        ]
        return ConditionSearchResult(
            seq=raw.get("seq", seq),
            cont_yn=raw.get("cont_yn", "N"),
            next_key=raw.get("next_key", ""),
            items=items,
        )

    async def condition_realtime(
        self,
        seq: str,
        callback: Callable[[ConditionRealtimeItem], Coroutine[Any, Any, None]],
        *,
        stex_tp: str = "K",
    ) -> None:
        """조건검색 실시간 조회를 시작한다 (ka10173).

        조건검색 결과(초기 스냅샷 + 실시간 이벤트)를 수신해 ``callback``에 전달한다.
        WebSocket 연결을 유지하면서 서버에서 메시지가 올 때마다 ``callback``을 호출한다.

        실시간 조건검색 전에 반드시 ``condition_list()``를 먼저 호출해야 한다.

        Args:
            seq: 조건검색식 일련번호.
            callback: 실시간 이벤트를 수신할 async 콜백. ``ConditionRealtimeItem``을 인자로 받는다.
            stex_tp: 거래소구분 (기본값 ``"K"`` — KRX).

        Raises:
            KiwoomApiError: WebSocket 오류 또는 API 오류.

        Example:
            >>> async def on_event(item: ConditionRealtimeItem) -> None:
            ...     print(item.values.stock_code, item.values.insert_delete)
            >>> await cond.condition_realtime("4", on_event)
        """
        import json

        await self._rate_limiter.acquire()
        payload = {
            "trnm": "CNSRREQ",
            "seq": seq,
            "search_type": "1",
            "stex_tp": stex_tp,
        }
        auth = self._auth_header()
        try:
            async with connect(
                self._ws_url,
                additional_headers=auth,
            ) as ws:
                await ws.send(json.dumps(payload))
                async for raw_msg in ws:
                    raw: dict = json.loads(raw_msg)
                    trnm = raw.get("trnm", "")

                    if trnm == "CNSRREQ":
                        # 초기 스냅샷 — 조회 오류 확인만 수행
                        _check(raw)
                        continue

                    if trnm == "REAL":
                        for entry in raw.get("data", []):
                            v = entry.get("values", {})
                            item = ConditionRealtimeItem(
                                type=entry.get("type", ""),
                                name=entry.get("name", ""),
                                item=entry.get("item", ""),
                                values=ConditionRealtimeValues(
                                    serial=v.get("841", ""),
                                    stock_code=v.get("9001", ""),
                                    insert_delete=v.get("843", ""),
                                    exec_time=v.get("20", ""),
                                    sell_buy=v.get("907", ""),
                                ),
                            )
                            await callback(item)
        except websockets.exceptions.WebSocketException as exc:
            raise KiwoomApiError(f"WebSocket 오류: {exc}") from exc
        except Exception as exc:
            raise KiwoomApiError(f"조건검색 실시간 오류: {exc}") from exc

    async def condition_stop(self, seq: str) -> ConditionStopResult:
        """조건검색 실시간 구독을 해제한다 (ka10174).

        Args:
            seq: 해제할 조건검색식 일련번호.

        Returns:
            해제 결과를 담은 ``ConditionStopResult``.

        Raises:
            KiwoomApiError: WebSocket 오류 또는 API 오류.
        """
        raw = await self._send_recv({"trnm": "CNSRCLR", "seq": seq})
        _check(raw)
        return ConditionStopResult(seq=raw.get("seq", seq))
