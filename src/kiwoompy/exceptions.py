"""kiwoompy 커스텀 예외 계층."""

from __future__ import annotations


class KiwoomError(Exception):
    """kiwoompy 최상위 예외. 모든 커스텀 예외의 기반 클래스."""


class KiwoomApiError(KiwoomError):
    """HTTP 통신 오류 또는 응답 파싱 실패.

    Args:
        message: 한글 오류 메시지.
        status_code: HTTP 상태 코드. 네트워크 오류 등으로 없을 경우 ``None``.
    """

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.status_code = status_code
        super().__init__(message)

    def __str__(self) -> str:
        if self.status_code is not None:
            return f"[HTTP {self.status_code}] {super().__str__()}"
        return super().__str__()


class KiwoomAuthError(KiwoomApiError):
    """인증 실패 — 잘못된 앱 키·시크릿 키, 토큰 미발급 등 인증 관련 오류.

    Args:
        message: 한글 오류 메시지.
        status_code: HTTP 상태 코드 (주로 400·401·403).
    """
