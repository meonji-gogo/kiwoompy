"""REST 통신 계층 — base URL 관리, 토큰 보관, HTTP get/post 단일 진입점."""

from __future__ import annotations

import logging
import threading
import time

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from kiwoompy.exceptions import KiwoomApiError, KiwoomAuthError
from kiwoompy.models import Env

logger = logging.getLogger(__name__)

_BASE_URLS: dict[str, str] = {
    "real": "https://api.kiwoom.com",
    "demo": "https://mockapi.kiwoom.com",
}

# 환경별 기본 RPS (Requests Per Second)
# 출처: 키움 REST API 공식 정책
#   실전: 1계좌당 1초당 20건
#   모의: 1계좌당 1초당 2건
_DEFAULT_RPS: dict[str, float] = {
    "real": 20.0,
    "demo": 2.0,
}

_TIMEOUT = 10.0   # 초
_MAX_ATTEMPTS = 3  # 최초 1회 + 재시도 2회
_WAIT_MIN = 1.0   # 지수 백오프 최소 대기 (초)
_WAIT_MAX = 8.0   # 지수 백오프 최대 대기 (초)


def _is_retryable(exc: BaseException) -> bool:
    """재시도 대상 예외인지 판별한다.

    ``KiwoomApiError`` 중 4xx 인증 오류(``KiwoomAuthError``)는 재시도하지 않는다.
    네트워크 오류·타임아웃·5xx 서버 오류만 재시도한다.
    """
    return isinstance(exc, KiwoomApiError) and not isinstance(exc, KiwoomAuthError)


_retry = retry(
    retry=retry_if_exception(_is_retryable),
    stop=stop_after_attempt(_MAX_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=_WAIT_MIN, max=_WAIT_MAX),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True,
)


class _RateLimiter:
    """스레드 안전 토큰 버킷 기반 유량 제어기.

    초당 ``rps``건을 초과하지 않도록 호출 간격을 제어한다.
    멀티스레드 환경에서도 안전하게 동작한다.

    Args:
        rps: 초당 최대 요청 수.
    """

    def __init__(self, rps: float) -> None:
        self._min_interval = 1.0 / rps
        self._lock = threading.Lock()
        self._last_called = 0.0

    def acquire(self) -> None:
        """다음 요청을 허용할 때까지 필요하면 대기한다."""
        with self._lock:
            now = time.monotonic()
            wait = self._min_interval - (now - self._last_called)
            if wait > 0:
                time.sleep(wait)
            self._last_called = time.monotonic()


class KiwoomApi:
    """키움 REST API HTTP 클라이언트.

    모든 HTTP 호출은 이 클래스를 통해서만 이루어진다.
    발급된 접근토큰을 내부에 보관하고, 이후 요청 헤더에 자동으로 포함한다.

    **유량 제어**: 환경별 기본 RPS를 자동 적용한다.

    - 실전(``real``): 기본 20건/초
    - 모의(``demo``): 기본 2건/초

    ``rps`` 파라미터로 직접 조정할 수 있다.

    **재시도**: 네트워크 오류·타임아웃·5xx 서버 오류는 지수 백오프로 최대
    ``_MAX_ATTEMPTS``회 재시도한다. 4xx 인증 오류는 재시도하지 않는다.

    Args:
        env: 환경 구분. ``"real"`` (운영) 또는 ``"demo"`` (모의투자).
        rps: 초당 최대 요청 수. ``None``이면 환경별 기본값 사용.
    """

    def __init__(self, env: Env = "demo", rps: float | None = None) -> None:
        self._base_url: str = _BASE_URLS[env]
        self._token: str | None = None
        self._rate_limiter = _RateLimiter(rps if rps is not None else _DEFAULT_RPS[env])
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={"Content-Type": "application/json;charset=UTF-8"},
            timeout=_TIMEOUT,
        )

    def set_token(self, token: str) -> None:
        """발급된 접근토큰을 저장한다. 이후 모든 요청에 자동 포함된다.

        Args:
            token: 접근토큰 문자열.
        """
        self._token = token

    def get_auth_header(self) -> dict[str, str]:
        """현재 저장된 접근토큰으로 Authorization 헤더를 반환한다.

        Returns:
            ``{"Authorization": "Bearer <token>"}`` 형태의 딕셔너리.

        Raises:
            KiwoomAuthError: 토큰이 아직 발급되지 않은 경우.
        """
        if self._token is None:
            raise KiwoomAuthError("접근토큰이 없습니다. issue_token()을 먼저 호출하세요.")
        return {"Authorization": f"Bearer {self._token}"}

    @_retry
    def post(self, path: str, body: dict, headers: dict[str, str] | None = None) -> dict:
        """JSON POST 요청을 보내고 응답 JSON을 반환한다.

        유량 제어 후 요청을 전송한다. 네트워크 오류·타임아웃·5xx는 지수 백오프로
        재시도한다. 4xx 응답(``KiwoomAuthError``)은 재시도하지 않고 즉시 raise한다.

        Args:
            path: 엔드포인트 경로 (예: ``"/oauth2/token"``).
            body: 요청 본문 딕셔너리.
            headers: 추가 요청 헤더. ``None``이면 기본 헤더만 사용.

        Returns:
            응답 JSON을 파싱한 딕셔너리.

        Raises:
            KiwoomAuthError: HTTP 4xx 응답 (인증 실패 등). 재시도 없음.
            KiwoomApiError: 최대 재시도 후에도 5xx·네트워크·파싱 오류가 지속되는 경우.
        """
        self._rate_limiter.acquire()

        try:
            response = self._client.post(path, json=body, headers=headers)
        except httpx.TimeoutException as exc:
            raise KiwoomApiError(f"요청 타임아웃: {path}") from exc
        except httpx.RequestError as exc:
            raise KiwoomApiError(f"네트워크 오류: {exc}") from exc

        if 400 <= response.status_code < 500:
            raise KiwoomAuthError(
                f"인증 오류: {response.text}",
                status_code=response.status_code,
            )
        if response.status_code >= 500:
            raise KiwoomApiError(
                f"서버 오류: {response.text}",
                status_code=response.status_code,
            )

        try:
            return response.json()
        except Exception as exc:
            raise KiwoomApiError(f"응답 파싱 실패: {response.text}") from exc

    def close(self) -> None:
        """HTTP 클라이언트 세션을 닫는다."""
        self._client.close()

    def __enter__(self) -> KiwoomApi:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
