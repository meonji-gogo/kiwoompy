"""인증 모듈 — OAuth2 접근토큰 발급 및 갱신 (au10001)."""

from __future__ import annotations

from dataclasses import asdict
from datetime import datetime

from kiwoompy.api import KiwoomApi
from kiwoompy.exceptions import KiwoomApiError, KiwoomAuthError
from kiwoompy.models import TokenRequest, TokenResponse

_EXPIRES_DT_FORMAT = "%Y%m%d%H%M%S"


class KiwoomAuth:
    """키움 REST API 인증 관리자.

    접근토큰 발급 후 ``KiwoomApi`` 계층에 저장하여
    이후 모든 API 호출에서 자동으로 재사용되도록 한다.

    Args:
        api: HTTP 클라이언트 인스턴스. 토큰을 발급 즉시 이 객체에 저장한다.
    """

    def __init__(self, api: KiwoomApi) -> None:
        self._api = api
        self._expires_at: datetime | None = None

    def issue_token(self, appkey: str, secretkey: str) -> TokenResponse:
        """접근토큰을 발급하고 API 클라이언트에 저장한다 (au10001).

        Args:
            appkey: 키움증권 앱 키.
            secretkey: 키움증권 시크릿 키.

        Returns:
            발급된 토큰 정보 (`TokenResponse`).

        Raises:
            KiwoomAuthError: 앱 키·시크릿 키가 올바르지 않거나 인증 서버 4xx 응답.
            KiwoomApiError: 서버 5xx 오류, 네트워크 타임아웃, 응답 파싱 실패.
        """
        request = TokenRequest(appkey=appkey, secretkey=secretkey)
        raw = self._api.post("/oauth2/token", asdict(request))

        response = self._parse_response(raw)
        self._api.set_token(response.token)
        self._expires_at = self._parse_expires_dt(response.expires_dt)
        return response

    def is_token_valid(self) -> bool:
        """현재 토큰이 유효한지 확인한다.

        Returns:
            토큰이 발급되어 있고 아직 만료되지 않으면 ``True``.
        """
        if self._expires_at is None:
            return False
        return datetime.now() < self._expires_at

    @staticmethod
    def _parse_response(raw: dict) -> TokenResponse:
        """API 응답 딕셔너리를 ``TokenResponse``로 변환한다.

        키움 API는 HTTP 200이더라도 ``return_code != 0`` 이면 인증 실패를 의미한다.
        이 경우 ``return_msg``를 포함한 ``KiwoomAuthError``를 raise한다.

        Args:
            raw: ``KiwoomApi.post()`` 반환값.

        Returns:
            파싱된 ``TokenResponse``.

        Raises:
            KiwoomAuthError: ``return_code != 0`` — 인증 실패 (앱 키·시크릿 키 오류 등).
            KiwoomApiError: 필수 필드(`token`, `token_type`, `expires_dt`) 누락 시.
        """
        return_code = raw.get("return_code")
        if return_code is not None and return_code != 0:
            msg = raw.get("return_msg", "인증 실패")
            raise KiwoomAuthError(f"인증 실패 (return_code={return_code}): {msg}")

        missing = [f for f in ("token", "token_type", "expires_dt") if not raw.get(f)]
        if missing:
            raise KiwoomApiError(f"응답 파싱 실패: 필수 필드 누락 — {', '.join(missing)}")
        return TokenResponse(
            token=raw["token"],
            token_type=raw["token_type"],
            expires_dt=raw["expires_dt"],
        )

    @staticmethod
    def _parse_expires_dt(expires_dt: str) -> datetime:
        """``expires_dt`` 문자열을 ``datetime``으로 변환한다.

        Args:
            expires_dt: ``"YYYYMMDDHHMMSS"`` 형식 만료일시 문자열.

        Returns:
            변환된 ``datetime`` 객체.

        Raises:
            KiwoomApiError: 형식이 맞지 않아 파싱에 실패한 경우.
        """
        try:
            return datetime.strptime(expires_dt, _EXPIRES_DT_FORMAT)
        except ValueError as exc:
            raise KiwoomApiError(
                f"만료일시 파싱 실패: {expires_dt!r} — YYYYMMDDHHMMSS 형식이어야 합니다."
            ) from exc
