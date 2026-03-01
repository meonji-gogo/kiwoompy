"""kiwoompy 공통 데이터 모델 — 타입 별칭 및 TR별 요청/응답 dataclass."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# ---------------------------------------------------------------------------
# 타입 별칭
# ---------------------------------------------------------------------------

type Env = Literal["real", "demo"]
"""운영(`real`) / 모의투자(`demo`) 환경 구분."""

type AccountNo = str
"""계좌번호. ``"12345678-01"`` 형식 (8자리 계좌번호 + 상품코드).
입력값 정규화는 :func:`kiwoompy.utils.normalize_account_no` 사용.
"""

# ---------------------------------------------------------------------------
# OAuth 인증 — au10001
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TokenRequest:
    """접근토큰 발급 요청 (au10001).

    Args:
        appkey: 키움증권 앱 키.
        secretkey: 키움증권 시크릿 키.
        grant_type: OAuth2 grant type. 항상 ``"client_credentials"`` 고정.
    """

    appkey: str
    secretkey: str
    grant_type: str = "client_credentials"


@dataclass(frozen=True)
class TokenResponse:
    """접근토큰 발급 응답 (au10001).

    Args:
        token: 접근토큰. ``Authorization: Bearer <token>`` 헤더에 사용.
        token_type: 토큰 타입 (예: ``"Bearer"``).
        expires_dt: 만료일시. ``"YYYYMMDDHHMMSS"`` 형식.
    """

    token: str
    token_type: str
    expires_dt: str

    def __repr__(self) -> str:
        masked = f"{self.token[:8]}..." if len(self.token) > 8 else "***"
        return (
            f"TokenResponse(token={masked!r}, "
            f"token_type={self.token_type!r}, "
            f"expires_dt={self.expires_dt!r})"
        )
