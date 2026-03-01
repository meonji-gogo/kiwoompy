"""KiwoomClient — KiwoomApi와 KiwoomAuth를 통합한 사용자 진입점 파사드."""

from __future__ import annotations

from kiwoompy.api import KiwoomApi
from kiwoompy.auth import KiwoomAuth
from kiwoompy.models import Env, TokenResponse


class KiwoomClient:
    """키움증권 REST API 통합 클라이언트.

    ``KiwoomApi``(HTTP 통신·유량 제어)와 ``KiwoomAuth``(토큰 발급·갱신)를
    하나로 묶은 파사드 클래스. 초기화 시 접근토큰을 자동으로 발급한다.

    Args:
        env: 환경 구분. ``"real"`` (운영) 또는 ``"demo"`` (모의투자). 기본값 ``"demo"``.
        appkey: 키움증권 앱 키.
        secretkey: 키움증권 시크릿 키.
        rps: 초당 최대 요청 수. ``None``이면 환경별 기본값 사용
            (``demo`` 2건/초, ``real`` 20건/초).

    Examples:
        기본 사용법:

        ```python
        from kiwoompy import KiwoomClient

        client = KiwoomClient(
            env="demo",
            appkey="YOUR_APP_KEY",
            secretkey="YOUR_APP_SECRET",
        )
        # 이후 client를 통해 API 호출
        ```

        context manager:

        ```python
        with KiwoomClient(env="demo", appkey="...", secretkey="...") as client:
            # API 호출
            pass  # 블록 종료 시 HTTP 세션 자동 종료
        ```
    """

    def __init__(
        self,
        env: Env = "demo",
        appkey: str = "",
        secretkey: str = "",
        rps: float | None = None,
    ) -> None:
        self._api = KiwoomApi(env=env, rps=rps)
        self._auth = KiwoomAuth(self._api)
        self._auth.issue_token(appkey=appkey, secretkey=secretkey)

    @property
    def api(self) -> KiwoomApi:
        """내부 ``KiwoomApi`` 인스턴스.

        고급 사용자나 테스트에서 HTTP 클라이언트에 직접 접근할 때 사용한다.
        """
        return self._api

    @property
    def auth(self) -> KiwoomAuth:
        """내부 ``KiwoomAuth`` 인스턴스.

        토큰 유효성 확인이나 수동 갱신이 필요할 때 사용한다.
        """
        return self._auth

    def refresh_token(self, appkey: str, secretkey: str) -> TokenResponse:
        """접근토큰을 재발급한다.

        토큰 만료 전후로 명시적으로 갱신이 필요할 때 호출한다.

        Args:
            appkey: 키움증권 앱 키.
            secretkey: 키움증권 시크릿 키.

        Returns:
            새로 발급된 ``TokenResponse``.
        """
        return self._auth.issue_token(appkey=appkey, secretkey=secretkey)

    def close(self) -> None:
        """HTTP 클라이언트 세션을 닫는다."""
        self._api.close()

    def __enter__(self) -> KiwoomClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
