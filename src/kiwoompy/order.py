"""주문 모듈 — 주식·신용 매수/매도/정정/취소 주문 (kt10000~kt10009)."""

from __future__ import annotations

from kiwoompy.api import KiwoomApi
from kiwoompy.exceptions import KiwoomApiError
from kiwoompy.models import (
    CancelOrderResponse,
    ModifyOrderResponse,
    OrderExchange,
    OrderResponse,
    OrderTradeType,
)


_TRADE_TYPE_CODE: dict[str, str] = {
    "limit":       "0",
    "market":      "3",
    "conditional": "5",
    "best":        "6",
    "priority":    "7",
    "limit_ioc":   "10",
    "market_ioc":  "13",
    "best_ioc":    "16",
    "limit_fok":   "20",
    "market_fok":  "23",
    "best_fok":    "26",
    "stop":        "28",
    "mid":         "29",
    "mid_ioc":     "30",
    "mid_fok":     "31",
    "pre_market":  "61",
    "after_hours": "62",
    "post_market": "81",
}


def _check(raw: dict) -> dict:
    """응답 body의 return_code를 확인하고 오류 시 KiwoomApiError를 raise한다.

    Args:
        raw: API 응답 dict.

    Returns:
        원본 ``raw`` dict.

    Raises:
        KiwoomApiError: ``return_code``가 0이 아닌 경우.
    """
    return_code = raw.get("return_code")
    if return_code is not None and return_code != 0:
        msg = raw.get("return_msg", "주문 실패")
        raise KiwoomApiError(f"주문 실패 (return_code={return_code}): {msg}")
    return raw


class KiwoomOrder:
    """키움 REST API 주문 클라이언트.

    주식·신용 매수/매도/정정/취소 주문 TR을 담당한다.
    모든 메서드는 ``KiwoomApi``를 통해 HTTP 요청을 전송하며,
    응답을 dataclass로 파싱하여 반환한다.

    주문은 실계좌에 직접 영향을 미치므로 ``env="real"`` 사용 시 주의한다.

    Args:
        api: 인증 토큰이 설정된 ``KiwoomApi`` 인스턴스.
    """

    _ORDR_PATH = "/api/dostk/ordr"
    _CRDORDR_PATH = "/api/dostk/crdordr"

    def __init__(self, api: KiwoomApi) -> None:
        self._api = api

    def _headers(self, api_id: str) -> dict[str, str]:
        """공통 요청 헤더를 반환한다."""
        return {**self._api.get_auth_header(), "api-id": api_id}

    # -----------------------------------------------------------------------
    # kt10000 — 주식 매수주문
    # -----------------------------------------------------------------------

    def buy(
        self,
        stock_code: str,
        quantity: str,
        trade_type: OrderTradeType,
        exchange: OrderExchange = "KRX",
        price: str = "",
        condition_price: str = "",
    ) -> OrderResponse:
        """주식 매수주문을 제출한다 (kt10000).

        Args:
            stock_code: 종목코드 (예: ``"005930"``).
            quantity: 주문수량 (단위: 주).
            trade_type: 매매구분.
                ``"market"``: 시장가, ``"limit"``: 보통(지정가), ``"conditional"``: 조건부지정가 등.
                시장가(``"market"``) 주문 시 ``price``는 공백으로 전달한다.
            exchange: 국내거래소구분. ``"KRX"``, ``"NXT"``, ``"SOR"``. 기본값 ``"KRX"``.
            price: 주문단가 (단위: 원). 시장가 주문 시 공백.
            condition_price: 조건단가. 스톱지정가(``"stop"``) 주문 시 스톱가. 기본값 공백.

        Returns:
            매수주문 응답 ``OrderResponse`` (주문번호 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._ORDR_PATH,
            {
                "dmst_stex_tp": exchange,
                "stk_cd": stock_code,
                "ord_qty": quantity,
                "ord_uv": price,
                "trde_tp": _TRADE_TYPE_CODE[trade_type],
                "cond_uv": condition_price,
            },
            headers=self._headers("kt10000"),
        ))
        return OrderResponse(
            ord_no=raw.get("ord_no", ""),
            dmst_stex_tp=raw.get("dmst_stex_tp", ""),
        )

    # -----------------------------------------------------------------------
    # kt10001 — 주식 매도주문
    # -----------------------------------------------------------------------

    def sell(
        self,
        stock_code: str,
        quantity: str,
        trade_type: OrderTradeType,
        exchange: OrderExchange = "KRX",
        price: str = "",
        condition_price: str = "",
    ) -> OrderResponse:
        """주식 매도주문을 제출한다 (kt10001).

        Args:
            stock_code: 종목코드 (예: ``"005930"``).
            quantity: 주문수량 (단위: 주).
            trade_type: 매매구분.
                ``"market"``: 시장가, ``"limit"``: 보통(지정가), ``"conditional"``: 조건부지정가 등.
                시장가(``"market"``) 주문 시 ``price``는 공백으로 전달한다.
            exchange: 국내거래소구분. ``"KRX"``, ``"NXT"``, ``"SOR"``. 기본값 ``"KRX"``.
            price: 주문단가 (단위: 원). 시장가 주문 시 공백.
            condition_price: 조건단가. 스톱지정가(``"stop"``) 주문 시 스톱가. 기본값 공백.

        Returns:
            매도주문 응답 ``OrderResponse`` (주문번호 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._ORDR_PATH,
            {
                "dmst_stex_tp": exchange,
                "stk_cd": stock_code,
                "ord_qty": quantity,
                "ord_uv": price,
                "trde_tp": _TRADE_TYPE_CODE[trade_type],
                "cond_uv": condition_price,
            },
            headers=self._headers("kt10001"),
        ))
        return OrderResponse(
            ord_no=raw.get("ord_no", ""),
            dmst_stex_tp=raw.get("dmst_stex_tp", ""),
        )

    # -----------------------------------------------------------------------
    # kt10002 — 주식 정정주문
    # -----------------------------------------------------------------------

    def modify(
        self,
        original_order_no: str,
        stock_code: str,
        modify_quantity: str,
        modify_price: str,
        exchange: OrderExchange = "KRX",
        modify_condition_price: str = "",
    ) -> ModifyOrderResponse:
        """주식 정정주문을 제출한다 (kt10002).

        미체결 주문의 수량 또는 가격을 정정한다.

        Args:
            original_order_no: 원주문번호 (정정할 주문의 주문번호).
            stock_code: 종목코드.
            modify_quantity: 정정수량 (단위: 주).
            modify_price: 정정단가 (단위: 원).
            exchange: 국내거래소구분. 기본값 ``"KRX"``.
            modify_condition_price: 정정조건단가. 기본값 공백.

        Returns:
            정정주문 응답 ``ModifyOrderResponse`` (새 주문번호 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._ORDR_PATH,
            {
                "dmst_stex_tp": exchange,
                "orig_ord_no": original_order_no,
                "stk_cd": stock_code,
                "mdfy_qty": modify_quantity,
                "mdfy_uv": modify_price,
                "mdfy_cond_uv": modify_condition_price,
            },
            headers=self._headers("kt10002"),
        ))
        return ModifyOrderResponse(
            ord_no=raw.get("ord_no", ""),
            base_orig_ord_no=raw.get("base_orig_ord_no", ""),
            mdfy_qty=raw.get("mdfy_qty", ""),
            dmst_stex_tp=raw.get("dmst_stex_tp", ""),
        )

    # -----------------------------------------------------------------------
    # kt10003 — 주식 취소주문
    # -----------------------------------------------------------------------

    def cancel(
        self,
        original_order_no: str,
        stock_code: str,
        cancel_quantity: str,
        exchange: OrderExchange = "KRX",
    ) -> CancelOrderResponse:
        """주식 취소주문을 제출한다 (kt10003).

        미체결 주문을 취소한다.

        Args:
            original_order_no: 원주문번호 (취소할 주문의 주문번호).
            stock_code: 종목코드.
            cancel_quantity: 취소수량 (단위: 주). ``"0"`` 입력 시 잔량 전부 취소.
            exchange: 국내거래소구분. 기본값 ``"KRX"``.

        Returns:
            취소주문 응답 ``CancelOrderResponse`` (새 주문번호 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._ORDR_PATH,
            {
                "dmst_stex_tp": exchange,
                "orig_ord_no": original_order_no,
                "stk_cd": stock_code,
                "cncl_qty": cancel_quantity,
            },
            headers=self._headers("kt10003"),
        ))
        return CancelOrderResponse(
            ord_no=raw.get("ord_no", ""),
            base_orig_ord_no=raw.get("base_orig_ord_no", ""),
            cncl_qty=raw.get("cncl_qty", ""),
        )

    # -----------------------------------------------------------------------
    # kt10006 — 신용 매수주문
    # -----------------------------------------------------------------------

    def credit_buy(
        self,
        stock_code: str,
        quantity: str,
        trade_type: OrderTradeType,
        exchange: OrderExchange = "KRX",
        price: str = "",
        condition_price: str = "",
    ) -> OrderResponse:
        """신용 매수주문을 제출한다 (kt10006).

        Args:
            stock_code: 종목코드.
            quantity: 주문수량 (단위: 주).
            trade_type: 매매구분. ``"market"``: 시장가, ``"limit"``: 보통(지정가) 등.
            exchange: 국내거래소구분. 기본값 ``"KRX"``.
            price: 주문단가 (단위: 원). 시장가 주문 시 공백.
            condition_price: 조건단가. 기본값 공백.

        Returns:
            신용 매수주문 응답 ``OrderResponse`` (주문번호 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._CRDORDR_PATH,
            {
                "dmst_stex_tp": exchange,
                "stk_cd": stock_code,
                "ord_qty": quantity,
                "ord_uv": price,
                "trde_tp": _TRADE_TYPE_CODE[trade_type],
                "cond_uv": condition_price,
            },
            headers=self._headers("kt10006"),
        ))
        return OrderResponse(
            ord_no=raw.get("ord_no", ""),
            dmst_stex_tp=raw.get("dmst_stex_tp", ""),
        )

    # -----------------------------------------------------------------------
    # kt10007 — 신용 매도주문
    # -----------------------------------------------------------------------

    def credit_sell(
        self,
        stock_code: str,
        quantity: str,
        trade_type: OrderTradeType,
        credit_deal_type: str,
        exchange: OrderExchange = "KRX",
        price: str = "",
        credit_loan_date: str = "",
        condition_price: str = "",
    ) -> OrderResponse:
        """신용 매도주문을 제출한다 (kt10007).

        Args:
            stock_code: 종목코드.
            quantity: 주문수량 (단위: 주).
            trade_type: 매매구분. ``"market"``: 시장가, ``"limit"``: 보통(지정가) 등.
            credit_deal_type: 신용거래구분. ``"33"``: 융자, ``"99"``: 융자합.
            exchange: 국내거래소구분. 기본값 ``"KRX"``.
            price: 주문단가 (단위: 원). 시장가 주문 시 공백.
            credit_loan_date: 대출일 (``YYYYMMDD`` 형식).
                ``credit_deal_type="33"`` (융자) 일 때 필수.
            condition_price: 조건단가. 기본값 공백.

        Returns:
            신용 매도주문 응답 ``OrderResponse`` (주문번호 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._CRDORDR_PATH,
            {
                "dmst_stex_tp": exchange,
                "stk_cd": stock_code,
                "ord_qty": quantity,
                "ord_uv": price,
                "trde_tp": _TRADE_TYPE_CODE[trade_type],
                "crd_deal_tp": credit_deal_type,
                "crd_loan_dt": credit_loan_date,
                "cond_uv": condition_price,
            },
            headers=self._headers("kt10007"),
        ))
        return OrderResponse(
            ord_no=raw.get("ord_no", ""),
            dmst_stex_tp=raw.get("dmst_stex_tp", ""),
        )

    # -----------------------------------------------------------------------
    # kt10008 — 신용 정정주문
    # -----------------------------------------------------------------------

    def credit_modify(
        self,
        original_order_no: str,
        stock_code: str,
        modify_quantity: str,
        modify_price: str,
        exchange: OrderExchange = "KRX",
        modify_condition_price: str = "",
    ) -> ModifyOrderResponse:
        """신용 정정주문을 제출한다 (kt10008).

        Args:
            original_order_no: 원주문번호.
            stock_code: 종목코드.
            modify_quantity: 정정수량 (단위: 주).
            modify_price: 정정단가 (단위: 원).
            exchange: 국내거래소구분. 기본값 ``"KRX"``.
            modify_condition_price: 정정조건단가. 기본값 공백.

        Returns:
            신용 정정주문 응답 ``ModifyOrderResponse``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._CRDORDR_PATH,
            {
                "dmst_stex_tp": exchange,
                "orig_ord_no": original_order_no,
                "stk_cd": stock_code,
                "mdfy_qty": modify_quantity,
                "mdfy_uv": modify_price,
                "mdfy_cond_uv": modify_condition_price,
            },
            headers=self._headers("kt10008"),
        ))
        return ModifyOrderResponse(
            ord_no=raw.get("ord_no", ""),
            base_orig_ord_no=raw.get("base_orig_ord_no", ""),
            mdfy_qty=raw.get("mdfy_qty", ""),
            dmst_stex_tp=raw.get("dmst_stex_tp", ""),
        )

    # -----------------------------------------------------------------------
    # kt10009 — 신용 취소주문
    # -----------------------------------------------------------------------

    def credit_cancel(
        self,
        original_order_no: str,
        stock_code: str,
        cancel_quantity: str,
        exchange: OrderExchange = "KRX",
    ) -> CancelOrderResponse:
        """신용 취소주문을 제출한다 (kt10009).

        Args:
            original_order_no: 원주문번호.
            stock_code: 종목코드.
            cancel_quantity: 취소수량 (단위: 주). ``"0"`` 입력 시 잔량 전부 취소.
            exchange: 국내거래소구분. 기본값 ``"KRX"``.

        Returns:
            신용 취소주문 응답 ``CancelOrderResponse``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._CRDORDR_PATH,
            {
                "dmst_stex_tp": exchange,
                "orig_ord_no": original_order_no,
                "stk_cd": stock_code,
                "cncl_qty": cancel_quantity,
            },
            headers=self._headers("kt10009"),
        ))
        return CancelOrderResponse(
            ord_no=raw.get("ord_no", ""),
            base_orig_ord_no=raw.get("base_orig_ord_no", ""),
            cncl_qty=raw.get("cncl_qty", ""),
        )
