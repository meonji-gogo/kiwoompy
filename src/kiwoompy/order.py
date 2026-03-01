"""주문 모듈 — 주식·신용 매수/매도/정정/취소 주문 (kt10000~kt10009) 및 금현물 주문·조회 (kt50000~kt50075)."""

from __future__ import annotations

from typing import Literal

from kiwoompy.api import KiwoomApi
from kiwoompy.exceptions import KiwoomApiError
from kiwoompy.models import (
    CancelOrderResponse,
    GoldBalance,
    GoldBalanceItem,
    GoldCancelOrderResponse,
    GoldDeposit,
    GoldModifyOrderResponse,
    GoldOrderDetailItem,
    GoldOrderDetail,
    GoldOrderResponse,
    GoldOrderStatusItem,
    GoldOrderStatus,
    GoldStockCode,
    GoldOrderTradeType,
    GoldTradeHistory,
    GoldTradeHistoryItem,
    GoldUnfilled,
    GoldUnfilledItem,
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

_GOLD_TRADE_TYPE_CODE: dict[str, str] = {
    "normal":     "00",
    "normal_ioc": "10",
    "normal_fok": "20",
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

    # ──────────────────────────────────────────────────────────
    # 9단계 — 금현물 주문·계좌 (kt50xxx)
    # ──────────────────────────────────────────────────────────

    _GOLD_ORDR_PATH = "/api/dostk/ordr"
    _GOLD_ACNT_PATH = "/api/dostk/acnt"

    def gold_buy(
        self,
        stock_code: GoldStockCode,
        order_quantity: str,
        trade_type: GoldOrderTradeType,
        order_price: str = "",
    ) -> GoldOrderResponse:
        """금현물 매수주문을 제출한다 (kt50000).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            order_quantity: 주문수량 (단위: g).
            trade_type: 매매구분. ``"normal"``:보통, ``"normal_ioc"``:보통(IOC), ``"normal_fok"``:보통(FOK).
            order_price: 주문단가. 시장가 주문 시 생략 가능.

        Returns:
            :class:`~kiwoompy.models.GoldOrderResponse` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        body: dict[str, str] = {
            "stk_cd":  stock_code,
            "ord_qty": order_quantity,
            "trde_tp": _GOLD_TRADE_TYPE_CODE[trade_type],
        }
        if order_price:
            body["ord_uv"] = order_price
        raw = _check(self._api.post(
            self._GOLD_ORDR_PATH,
            body,
            headers=self._headers("kt50000"),
        ))
        return GoldOrderResponse(ord_no=raw.get("ord_no", ""))

    def gold_sell(
        self,
        stock_code: GoldStockCode,
        order_quantity: str,
        trade_type: GoldOrderTradeType,
        order_price: str = "",
    ) -> GoldOrderResponse:
        """금현물 매도주문을 제출한다 (kt50001).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            order_quantity: 주문수량 (단위: g).
            trade_type: 매매구분. ``"normal"``:보통, ``"normal_ioc"``:보통(IOC), ``"normal_fok"``:보통(FOK).
            order_price: 주문단가. 시장가 주문 시 생략 가능.

        Returns:
            :class:`~kiwoompy.models.GoldOrderResponse` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        body: dict[str, str] = {
            "stk_cd":  stock_code,
            "ord_qty": order_quantity,
            "trde_tp": _GOLD_TRADE_TYPE_CODE[trade_type],
        }
        if order_price:
            body["ord_uv"] = order_price
        raw = _check(self._api.post(
            self._GOLD_ORDR_PATH,
            body,
            headers=self._headers("kt50001"),
        ))
        return GoldOrderResponse(ord_no=raw.get("ord_no", ""))

    def gold_modify(
        self,
        stock_code: GoldStockCode,
        original_order_no: str,
        modify_quantity: str,
        modify_price: str,
    ) -> GoldModifyOrderResponse:
        """금현물 정정주문을 제출한다 (kt50002).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            original_order_no: 원주문번호.
            modify_quantity: 정정수량 (단위: g).
            modify_price: 정정단가.

        Returns:
            :class:`~kiwoompy.models.GoldModifyOrderResponse` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._GOLD_ORDR_PATH,
            {
                "stk_cd":      stock_code,
                "orig_ord_no": original_order_no,
                "mdfy_qty":    modify_quantity,
                "mdfy_uv":     modify_price,
            },
            headers=self._headers("kt50002"),
        ))
        return GoldModifyOrderResponse(
            ord_no=raw.get("ord_no", ""),
            base_orig_ord_no=raw.get("base_orig_ord_no", ""),
            mdfy_qty=raw.get("mdfy_qty", ""),
        )

    def gold_cancel(
        self,
        stock_code: GoldStockCode,
        original_order_no: str,
        cancel_quantity: str,
    ) -> GoldCancelOrderResponse:
        """금현물 취소주문을 제출한다 (kt50003).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            original_order_no: 원주문번호.
            cancel_quantity: 취소수량 (단위: g). ``"0"`` 입력 시 잔량 전부 취소.

        Returns:
            :class:`~kiwoompy.models.GoldCancelOrderResponse` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 주문 실패.
        """
        raw = _check(self._api.post(
            self._GOLD_ORDR_PATH,
            {
                "orig_ord_no": original_order_no,
                "stk_cd":      stock_code,
                "cncl_qty":    cancel_quantity,
            },
            headers=self._headers("kt50003"),
        ))
        return GoldCancelOrderResponse(
            ord_no=raw.get("ord_no", ""),
            base_orig_ord_no=raw.get("base_orig_ord_no", ""),
            cncl_qty=raw.get("cncl_qty", ""),
        )

    def gold_balance(self) -> GoldBalance:
        """금현물 잔고를 확인한다 (kt50020).

        Returns:
            :class:`~kiwoompy.models.GoldBalance` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._GOLD_ACNT_PATH,
            {},
            headers=self._headers("kt50020"),
        ))
        holdings = [
            GoldBalanceItem(
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                real_qty=it.get("real_qty", ""),
                avg_prc=it.get("avg_prc", ""),
                cur_prc=it.get("cur_prc", ""),
                est_amt=it.get("est_amt", ""),
                est_lspft=it.get("est_lspft", ""),
                est_ratio=it.get("est_ratio", ""),
                cmsn=it.get("cmsn", ""),
                vlad_tax=it.get("vlad_tax", ""),
                book_amt2=it.get("book_amt2", ""),
                pl_prch_prc=it.get("pl_prch_prc", ""),
                qty=it.get("qty", ""),
                buy_qty=it.get("buy_qty", ""),
                sell_qty=it.get("sell_qty", ""),
                able_qty=it.get("able_qty", ""),
            )
            for it in raw.get("gold_acnt_evlt_prst", [])
        ]
        return GoldBalance(
            tot_entr=raw.get("tot_entr", ""),
            net_entr=raw.get("net_entr", ""),
            tot_est_amt=raw.get("tot_est_amt", ""),
            net_amt=raw.get("net_amt", ""),
            tot_book_amt2=raw.get("tot_book_amt2", ""),
            tot_dep_amt=raw.get("tot_dep_amt", ""),
            paym_alowa=raw.get("paym_alowa", ""),
            pl_amt=raw.get("pl_amt", ""),
            items=holdings,
        )

    def gold_deposit(self) -> GoldDeposit:
        """금현물 예수금을 조회한다 (kt50021).

        Returns:
            :class:`~kiwoompy.models.GoldDeposit` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._GOLD_ACNT_PATH,
            {},
            headers=self._headers("kt50021"),
        ))
        return GoldDeposit(
            entra=raw.get("entra", ""),
            profa_ch=raw.get("profa_ch", ""),
            chck_ina_amt=raw.get("chck_ina_amt", ""),
            etc_loan=raw.get("etc_loan", ""),
            etc_loan_dlfe=raw.get("etc_loan_dlfe", ""),
            etc_loan_tot=raw.get("etc_loan_tot", ""),
            prsm_entra=raw.get("prsm_entra", ""),
            buy_exct_amt=raw.get("buy_exct_amt", ""),
            sell_exct_amt=raw.get("sell_exct_amt", ""),
            sell_buy_exct_amt=raw.get("sell_buy_exct_amt", ""),
            dly_amt=raw.get("dly_amt", ""),
            prsm_pymn_alow_amt=raw.get("prsm_pymn_alow_amt", ""),
            pymn_alow_amt=raw.get("pymn_alow_amt", ""),
            ord_alow_amt=raw.get("ord_alow_amt", ""),
        )

    def gold_order_status(
        self,
        order_date: str,
        market_deal_type: str,
        stock_bond_type: Literal["0", "1", "2"],
        sell_type: Literal["0", "1", "2"],
        query_type: Literal["1", "2"] = "1",
        stock_code: str = "",
        from_order_no: str = "",
        exchange: str = "%",
    ) -> GoldOrderStatus:
        """금현물 주문체결전체를 조회한다 (kt50030).

        Args:
            order_date: 주문일자 (``"YYYYMMDD"``).
            market_deal_type: 시장구분.
            stock_bond_type: 주식채권구분. ``"0"``:전체, ``"1"``:주식, ``"2"``:채권.
            sell_type: 매도수구분. ``"0"``:전체, ``"1"``:매도, ``"2"``:매수.
            query_type: 조회구분. ``"1"``:주문순, ``"2"``:역순. 기본값 ``"1"``.
            stock_code: 종목코드. 공백 시 전체 종목.
            from_order_no: 시작주문번호. 공백 시 전체 주문.
            exchange: 국내거래소구분. ``"%"``:전체, ``"KRX"``, ``"NXT"``, ``"SOR"``. 기본값 ``"%"``.

        Returns:
            :class:`~kiwoompy.models.GoldOrderStatus` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._GOLD_ACNT_PATH,
            {
                "ord_dt":       order_date,
                "qry_tp":       query_type,
                "mrkt_deal_tp": market_deal_type,
                "stk_bond_tp":  stock_bond_type,
                "slby_tp":      sell_type,
                "stk_cd":       stock_code,
                "fr_ord_no":    from_order_no,
                "dmst_stex_tp": exchange,
            },
            headers=self._headers("kt50030"),
        ))
        items = [
            GoldOrderStatusItem(
                stk_bond_tp=it.get("stk_bond_tp", ""),
                ord_no=it.get("ord_no", ""),
                stk_cd=it.get("stk_cd", ""),
                trde_tp=it.get("trde_tp", ""),
                io_tp_nm=it.get("io_tp_nm", ""),
                ord_qty=it.get("ord_qty", ""),
                ord_uv=it.get("ord_uv", ""),
                cnfm_qty=it.get("cnfm_qty", ""),
                data_send_end_tp=it.get("data_send_end_tp", ""),
                mrkt_deal_tp=it.get("mrkt_deal_tp", ""),
                rsrv_tp=it.get("rsrv_tp", ""),
                orig_ord_no=it.get("orig_ord_no", ""),
                stk_nm=it.get("stk_nm", ""),
                dcd_tp_nm=it.get("dcd_tp_nm", ""),
                crd_deal_tp=it.get("crd_deal_tp", ""),
                cntr_qty=it.get("cntr_qty", ""),
                cntr_uv=it.get("cntr_uv", ""),
                ord_remnq=it.get("ord_remnq", ""),
                comm_ord_tp=it.get("comm_ord_tp", ""),
                mdfy_cncl_tp=it.get("mdfy_cncl_tp", ""),
                dmst_stex_tp=it.get("dmst_stex_tp", ""),
                cond_uv=it.get("cond_uv", ""),
            )
            for it in raw.get("acnt_ord_cntr_prst", [])
        ]
        return GoldOrderStatus(items=items)

    def gold_order_detail(
        self,
        stock_bond_type: Literal["0", "1", "2"],
        sell_type: Literal["0", "1", "2"],
        exchange: str,
        query_type: Literal["1", "2", "3", "4"] = "1",
        order_date: str = "",
        stock_code: str = "",
        from_order_no: str = "",
    ) -> GoldOrderDetail:
        """금현물 주문체결을 조회한다 (kt50031).

        Args:
            stock_bond_type: 주식채권구분. ``"0"``:전체, ``"1"``:주식, ``"2"``:채권.
            sell_type: 매도수구분. ``"0"``:전체, ``"1"``:매도, ``"2"``:매수.
            exchange: 국내거래소구분. ``"%"``:전체, ``"KRX"``, ``"NXT"``, ``"SOR"``.
            query_type: 조회구분. ``"1"``:주문순, ``"2"``:역순, ``"3"``:미체결, ``"4"``:체결내역만. 기본값 ``"1"``.
            order_date: 주문일자 (``"YYYYMMDD"``). 공백 허용.
            stock_code: 종목코드. 공백 시 전체 종목.
            from_order_no: 시작주문번호. 공백 시 전체 주문.

        Returns:
            :class:`~kiwoompy.models.GoldOrderDetail` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._GOLD_ACNT_PATH,
            {
                "ord_dt":       order_date,
                "qry_tp":       query_type,
                "stk_bond_tp":  stock_bond_type,
                "sell_tp":      sell_type,
                "stk_cd":       stock_code,
                "fr_ord_no":    from_order_no,
                "dmst_stex_tp": exchange,
            },
            headers=self._headers("kt50031"),
        ))
        items = [
            GoldOrderDetailItem(
                ord_no=it.get("ord_no", ""),
                stk_cd=it.get("stk_cd", ""),
                trde_tp=it.get("trde_tp", ""),
                crd_tp=it.get("crd_tp", ""),
                ord_qty=it.get("ord_qty", ""),
                ord_uv=it.get("ord_uv", ""),
                cnfm_qty=it.get("cnfm_qty", ""),
                acpt_tp=it.get("acpt_tp", ""),
                rsrv_tp=it.get("rsrv_tp", ""),
                ord_tm=it.get("ord_tm", ""),
                ori_ord=it.get("ori_ord", ""),
                stk_nm=it.get("stk_nm", ""),
                io_tp_nm=it.get("io_tp_nm", ""),
                loan_dt=it.get("loan_dt", ""),
                cntr_qty=it.get("cntr_qty", ""),
                cntr_uv=it.get("cntr_uv", ""),
                ord_remnq=it.get("ord_remnq", ""),
                comm_ord_tp=it.get("comm_ord_tp", ""),
                mdfy_cncl=it.get("mdfy_cncl", ""),
                cnfm_tm=it.get("cnfm_tm", ""),
                dmst_stex_tp=it.get("dmst_stex_tp", ""),
                cond_uv=it.get("cond_uv", ""),
            )
            for it in raw.get("acnt_ord_cntr_prps_dtl", [])
        ]
        return GoldOrderDetail(items=items)

    def gold_trade_history(
        self,
        start_date: str = "",
        end_date: str = "",
        trade_type: Literal["0", "1", "2", "3", "4", "5", "6", "7"] = "0",
        stock_code: str = "",
    ) -> GoldTradeHistory:
        """금현물 거래내역을 조회한다 (kt50032).

        Args:
            start_date: 시작일자 (``"YYYYMMDD"``). 공백 허용.
            end_date: 종료일자 (``"YYYYMMDD"``). 공백 허용.
            trade_type: 구분. ``"0"``:전체, ``"1"``:입출금, ``"2"``:출고, ``"3"``:매매,
                ``"4"``:매수, ``"5"``:매도, ``"6"``:입금, ``"7"``:출금. 기본값 ``"0"``.
            stock_code: 종목코드. 공백 시 전체 종목.

        Returns:
            :class:`~kiwoompy.models.GoldTradeHistory` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._GOLD_ACNT_PATH,
            {
                "strt_dt": start_date,
                "end_dt":  end_date,
                "tp":      trade_type,
                "stk_cd":  stock_code,
            },
            headers=self._headers("kt50032"),
        ))
        items = [
            GoldTradeHistoryItem(
                deal_dt=it.get("deal_dt", ""),
                deal_no=it.get("deal_no", ""),
                rmrk_nm=it.get("rmrk_nm", ""),
                deal_qty=it.get("deal_qty", ""),
                gold_spot_vat=it.get("gold_spot_vat", ""),
                exct_amt=it.get("exct_amt", ""),
                dly_sum=it.get("dly_sum", ""),
                entra_remn=it.get("entra_remn", ""),
                mdia_nm=it.get("mdia_nm", ""),
                orig_deal_no=it.get("orig_deal_no", ""),
                stk_nm=it.get("stk_nm", ""),
                uv_exrt=it.get("uv_exrt", ""),
                cmsn=it.get("cmsn", ""),
                uncl_ocr=it.get("uncl_ocr", ""),
                rpym_sum=it.get("rpym_sum", ""),
                spot_remn=it.get("spot_remn", ""),
                proc_time=it.get("proc_time", ""),
                rcpy_no=it.get("rcpy_no", ""),
                stk_cd=it.get("stk_cd", ""),
                deal_amt=it.get("deal_amt", ""),
                tax_tot_amt=it.get("tax_tot_amt", ""),
                cntr_dt=it.get("cntr_dt", ""),
                proc_brch_nm=it.get("proc_brch_nm", ""),
                prcsr=it.get("prcsr", ""),
            )
            for it in raw.get("gold_trde_hist", [])
        ]
        return GoldTradeHistory(
            acnt_print=raw.get("acnt_print", ""),
            items=items,
        )

    def gold_unfilled(
        self,
        order_date: str,
        market_deal_type: str,
        stock_bond_type: Literal["0", "1", "2"],
        sell_type: Literal["0", "1", "2"],
        query_type: Literal["1", "2"] = "1",
        stock_code: str = "",
        from_order_no: str = "",
        exchange: str = "%",
    ) -> GoldUnfilled:
        """금현물 미체결을 조회한다 (kt50075).

        Args:
            order_date: 주문일자 (``"YYYYMMDD"``).
            market_deal_type: 시장구분.
            stock_bond_type: 주식채권구분. ``"0"``:전체, ``"1"``:주식, ``"2"``:채권.
            sell_type: 매도수구분. ``"0"``:전체, ``"1"``:매도, ``"2"``:매수.
            query_type: 조회구분. ``"1"``:주문순, ``"2"``:역순. 기본값 ``"1"``.
            stock_code: 종목코드. 공백 시 전체 종목.
            from_order_no: 시작주문번호. 공백 시 전체 주문.
            exchange: 국내거래소구분. ``"%"``:전체, ``"KRX"``, ``"NXT"``, ``"SOR"``. 기본값 ``"%"``.

        Returns:
            :class:`~kiwoompy.models.GoldUnfilled` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._GOLD_ACNT_PATH,
            {
                "ord_dt":       order_date,
                "qry_tp":       query_type,
                "mrkt_deal_tp": market_deal_type,
                "stk_bond_tp":  stock_bond_type,
                "sell_tp":      sell_type,
                "stk_cd":       stock_code,
                "fr_ord_no":    from_order_no,
                "dmst_stex_tp": exchange,
            },
            headers=self._headers("kt50075"),
        ))
        items = [
            GoldUnfilledItem(
                stk_bond_tp=it.get("stk_bond_tp", ""),
                ord_no=it.get("ord_no", ""),
                stk_cd=it.get("stk_cd", ""),
                trde_tp=it.get("trde_tp", ""),
                io_tp_nm=it.get("io_tp_nm", ""),
                ord_qty=it.get("ord_qty", ""),
                ord_uv=it.get("ord_uv", ""),
                cnfm_qty=it.get("cnfm_qty", ""),
                data_send_end_tp=it.get("data_send_end_tp", ""),
                mrkt_deal_tp=it.get("mrkt_deal_tp", ""),
                rsrv_tp=it.get("rsrv_tp", ""),
                orig_ord_no=it.get("orig_ord_no", ""),
                stk_nm=it.get("stk_nm", ""),
                dcd_tp_nm=it.get("dcd_tp_nm", ""),
                crd_deal_tp=it.get("crd_deal_tp", ""),
                cntr_qty=it.get("cntr_qty", ""),
                cntr_uv=it.get("cntr_uv", ""),
                ord_remnq=it.get("ord_remnq", ""),
                comm_ord_tp=it.get("comm_ord_tp", ""),
                mdfy_cncl_tp=it.get("mdfy_cncl_tp", ""),
                dmst_stex_tp=it.get("dmst_stex_tp", ""),
                cond_uv=it.get("cond_uv", ""),
            )
            for it in raw.get("acnt_ord_oso_prst", [])
        ]
        return GoldUnfilled(items=items)
