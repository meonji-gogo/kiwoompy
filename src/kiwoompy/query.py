"""조회 모듈 — 계좌·잔고·손익·주문체결 조회 (2단계: kt00xxx, ka00xxx, ka01xxx, ka10xxx/acnt)."""

from __future__ import annotations

from typing import Literal

from kiwoompy.api import KiwoomApi
from kiwoompy.exceptions import KiwoomApiError
from kiwoompy.models import (
    AccountBalance,
    AccountEvaluation,
    AccountEvaluationItem,
    AccountNumbers,
    AccountReturnItem,
    CreditOrderableQuantity,
    DailyAccountReturn,
    DailyAccountStatus,
    DailyBalanceReturn,
    DailyBalanceReturnItem,
    DailyRealizedProfit,
    DailyRealizedProfitDetail,
    DailyRealizedProfitDetailItem,
    DailyRealizedProfitItem,
    DailyTradeJournal,
    DailyTradeJournalItem,
    DepositDetail,
    DailyEstimatedAssetItem,
    EstimatedAsset,
    ExecutionBalance,
    ExecutionBalanceItem,
    FilledOrderItem,
    FxDepositItem,
    HoldingItem,
    MarginDetail,
    NextDaySettlement,
    NextDaySettlementItem,
    OrderableAmount,
    OrderableQuantity,
    OrderExecutionStatus,
    OrderExecutionStatusItem,
    OrderHistoryDetailItem,
    RealizedProfitByDateItem,
    RealizedProfitByPeriodItem,
    SplitOrderDetailItem,
    TransactionHistoryItem,
    UnfilledOrderItem,
)

type QueryType = Literal["1", "2", "3"]
"""예수금 조회구분. ``"2"``: 일반조회, ``"3"``: 추정조회."""

type DomesticExchange = Literal["KRX", "NXT", "%", "SOR"]
"""국내거래소구분.
- ``"KRX"``: 한국거래소
- ``"NXT"``: 넥스트트레이드
- ``"%"``: 전체
- ``"SOR"``: 최선주문집행
"""

type ExchangeType = Literal["all", "krx", "nxt"]
"""거래소구분.

- ``"all"``: 통합 — API ``"0"``
- ``"krx"``: 한국거래소 — API ``"1"``
- ``"nxt"``: 넥스트트레이드 — API ``"2"``
"""

_EXCHANGE_CODE: dict[str, str] = {
    "all": "0",
    "krx": "1",
    "nxt": "2",
}

type SellType = Literal["all", "sell", "buy"]
"""매도수구분.

- ``"all"``: 전체 — API ``"0"``
- ``"sell"``: 매도 — API ``"1"``
- ``"buy"``: 매수 — API ``"2"``
"""

type TradeSide = Literal["sell", "buy"]
"""매매구분 (전체 없음).

- ``"sell"``: 매도 — API ``"1"``
- ``"buy"``: 매수 — API ``"2"``
"""

type UnfilledTradeType = Literal["all", "sell", "buy"]
"""미체결 매매구분.

- ``"all"``: 전체 — API ``"0"``
- ``"sell"``: 매도 — API ``"1"``
- ``"buy"``: 매수 — API ``"2"``
"""

_SELL_TYPE_CODE: dict[str, str] = {
    "all":  "0",
    "sell": "1",
    "buy":  "2",
}

# ---------------------------------------------------------------------------
# 3단계 타입 정의
# ---------------------------------------------------------------------------

type DepositQueryType = Literal["normal", "estimated"]
"""예수금 조회구분.

- ``"normal"``: 일반조회 — API ``"2"``
- ``"estimated"``: 추정조회 — API ``"3"``
"""

type DelistedQueryType = Literal["all", "exclude_delisted"]
"""상장폐지 조회구분.

- ``"all"``: 전체 — API ``"0"``
- ``"exclude_delisted"``: 상장폐지종목제외 — API ``"1"``
"""

type OrderHistoryQueryType = Literal["asc", "desc", "unfilled", "filled_only"]
"""주문체결내역상세 조회구분.

- ``"asc"``: 주문순 — API ``"1"``
- ``"desc"``: 역순 — API ``"2"``
- ``"unfilled"``: 미체결 — API ``"3"``
- ``"filled_only"``: 체결내역만 — API ``"4"``
"""

type StockBondType = Literal["all", "stock", "bond"]
"""주식채권구분.

- ``"all"``: 전체 — API ``"0"``
- ``"stock"``: 주식 — API ``"1"``
- ``"bond"``: 채권 — API ``"2"``
"""

type MarketType = Literal["all", "kospi", "kosdaq", "otcbb", "ecn"]
"""시장구분.

- ``"all"``: 전체 — API ``"0"``
- ``"kospi"``: 코스피 — API ``"1"``
- ``"kosdaq"``: 코스닥 — API ``"2"``
- ``"otcbb"``: OTCBB — API ``"3"``
- ``"ecn"``: ECN — API ``"4"``
"""

type ExecutionQueryType = Literal["all", "filled"]
"""주문체결현황 조회구분.

- ``"all"``: 전체 — API ``"0"``
- ``"filled"``: 체결 — API ``"1"``
"""

type GoodsType = Literal["all", "domestic_stock", "fund", "overseas_stock", "financial"]
"""위탁종합거래내역 상품구분.

- ``"all"``: 전체 — API ``"0"``
- ``"domestic_stock"``: 국내주식 — API ``"1"``
- ``"fund"``: 수익증권 — API ``"2"``
- ``"overseas_stock"``: 해외주식 — API ``"3"``
- ``"financial"``: 금융상품 — API ``"4"``
"""

type BalanceQueryType = Literal["combined", "individual"]
"""계좌평가잔고 조회구분.

- ``"combined"``: 합산 — API ``"1"``
- ``"individual"``: 개별 — API ``"2"``
"""

type FilledQueryType = Literal["all", "by_stock"]
"""체결조회 조회구분.

- ``"all"``: 전체 — API ``"0"``
- ``"by_stock"``: 종목 — API ``"1"``
"""

type SingleStockType = Literal["today_buy_sell", "today_sell_all"]
"""당일매매일지 단주구분.

- ``"today_buy_sell"``: 당일매수에 대한 당일매도 — API ``"1"``
- ``"today_sell_all"``: 당일매도 전체 — API ``"2"``
"""

type CashCreditType = Literal["all", "cash", "credit"]
"""당일매매일지 현금신용구분.

- ``"all"``: 전체 — API ``"0"``
- ``"cash"``: 현금매매만 — API ``"1"``
- ``"credit"``: 신용매매만 — API ``"2"``
"""

_DEPOSIT_QUERY_CODE: dict[str, str] = {
    "normal":    "2",
    "estimated": "3",
}
_DELISTED_QUERY_CODE: dict[str, str] = {
    "all":              "0",
    "exclude_delisted": "1",
}
_ORDER_HISTORY_QUERY_CODE: dict[str, str] = {
    "asc":         "1",
    "desc":        "2",
    "unfilled":    "3",
    "filled_only": "4",
}
_STOCK_BOND_CODE: dict[str, str] = {
    "all":   "0",
    "stock": "1",
    "bond":  "2",
}
_MARKET_TYPE_CODE: dict[str, str] = {
    "all":    "0",
    "kospi":  "1",
    "kosdaq": "2",
    "otcbb":  "3",
    "ecn":    "4",
}
_EXECUTION_QUERY_CODE: dict[str, str] = {
    "all":    "0",
    "filled": "1",
}
_GOODS_TYPE_CODE: dict[str, str] = {
    "all":            "0",
    "domestic_stock": "1",
    "fund":           "2",
    "overseas_stock": "3",
    "financial":      "4",
}
_BALANCE_QUERY_CODE: dict[str, str] = {
    "combined":   "1",
    "individual": "2",
}
_FILLED_QUERY_CODE: dict[str, str] = {
    "all":      "0",
    "by_stock": "1",
}
_SINGLE_STOCK_CODE: dict[str, str] = {
    "today_buy_sell": "1",
    "today_sell_all": "2",
}
_CASH_CREDIT_CODE: dict[str, str] = {
    "all":    "0",
    "cash":   "1",
    "credit": "2",
}


def _check(raw: dict) -> dict:
    """응답 body의 return_code를 확인하고 오류 시 KiwoomApiError를 raise한다.

    Args:
        raw: API 응답 dict.

    Returns:
        원본 ``raw`` dict (체이닝 편의).

    Raises:
        KiwoomApiError: ``return_code``가 0이 아닌 경우.
    """
    return_code = raw.get("return_code")
    if return_code is not None and return_code != 0:
        msg = raw.get("return_msg", "조회 실패")
        raise KiwoomApiError(f"조회 실패 (return_code={return_code}): {msg}")
    return raw


class KiwoomQuery:
    """키움 REST API 조회 클라이언트.

    계좌·잔고·손익·주문체결 등 조회성 TR을 담당한다.
    모든 메서드는 ``KiwoomApi``를 통해 HTTP 요청을 전송하며,
    응답을 dataclass로 파싱하여 반환한다.

    Args:
        api: 인증 토큰이 설정된 ``KiwoomApi`` 인스턴스.
    """

    _ACNT_PATH = "/api/dostk/acnt"
    _STKINFO_PATH = "/api/dostk/stkinfo"

    def __init__(self, api: KiwoomApi) -> None:
        self._api = api

    def _headers(self, api_id: str) -> dict[str, str]:
        """공통 요청 헤더를 반환한다."""
        return {**self._api.get_auth_header(), "api-id": api_id}

    # -----------------------------------------------------------------------
    # kt00001 — 예수금상세현황요청
    # -----------------------------------------------------------------------

    def get_deposit(self, query_type: DepositQueryType = "normal") -> DepositDetail:
        """예수금상세현황을 조회한다 (kt00001).

        Args:
            query_type: 조회구분. ``"normal"``: 일반조회, ``"estimated"``: 추정조회.

        Returns:
            예수금상세현황 ``DepositDetail``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"qry_tp": _DEPOSIT_QUERY_CODE[query_type]},
            headers=self._headers("kt00001"),
        ))
        fx_list = [
            FxDepositItem(
                crnc_cd=item.get("crnc_cd", ""),
                fx_entr=item.get("fx_entr", ""),
                fc_krw_repl_evlta=item.get("fc_krw_repl_evlta", ""),
                fc_trst_profa=item.get("fc_trst_profa", ""),
                pymn_alow_amt=item.get("pymn_alow_amt", ""),
                pymn_alow_amt_entr=item.get("pymn_alow_amt_entr", ""),
                ord_alow_amt_entr=item.get("ord_alow_amt_entr", ""),
                fc_uncla=item.get("fc_uncla", ""),
                fc_ch_uncla=item.get("fc_ch_uncla", ""),
                dly_amt=item.get("dly_amt", ""),
                d1_fx_entr=item.get("d1_fx_entr", ""),
                d2_fx_entr=item.get("d2_fx_entr", ""),
                d3_fx_entr=item.get("d3_fx_entr", ""),
                d4_fx_entr=item.get("d4_fx_entr", ""),
            )
            for item in raw.get("stk_entr_prst", [])
        ]
        return DepositDetail(
            entr=raw.get("entr", ""),
            profa_ch=raw.get("profa_ch", ""),
            pymn_alow_amt=raw.get("pymn_alow_amt", ""),
            ord_alow_amt=raw.get("ord_alow_amt", ""),
            d1_entra=raw.get("d1_entra", ""),
            d1_pymn_alow_amt=raw.get("d1_pymn_alow_amt", ""),
            d2_entra=raw.get("d2_entra", ""),
            d2_pymn_alow_amt=raw.get("d2_pymn_alow_amt", ""),
            repl_amt=raw.get("repl_amt", ""),
            ch_uncla=raw.get("ch_uncla", ""),
            nrpy_loan=raw.get("nrpy_loan", ""),
            crd_grnt_rt=raw.get("crd_grnt_rt", ""),
            fx_deposits=fx_list,
        )

    # -----------------------------------------------------------------------
    # kt00002 — 일별추정예탁자산현황요청
    # -----------------------------------------------------------------------

    def get_daily_estimated_asset(
        self,
        start_dt: str,
        end_dt: str,
    ) -> list[DailyEstimatedAssetItem]:
        """일별추정예탁자산현황을 조회한다 (kt00002).

        Args:
            start_dt: 시작조회기간 (``YYYYMMDD`` 형식).
            end_dt: 종료조회기간 (``YYYYMMDD`` 형식).

        Returns:
            일별추정예탁자산 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"start_dt": start_dt, "end_dt": end_dt},
            headers=self._headers("kt00002"),
        ))
        return [
            DailyEstimatedAssetItem(
                dt=item.get("dt", ""),
                entr=item.get("entr", ""),
                grnt_use_amt=item.get("grnt_use_amt", ""),
                crd_loan=item.get("crd_loan", ""),
                ls_grnt=item.get("ls_grnt", ""),
                repl_amt=item.get("repl_amt", ""),
                prsm_dpst_aset_amt=item.get("prsm_dpst_aset_amt", ""),
                prsm_dpst_aset_amt_bncr_skip=item.get("prsm_dpst_aset_amt_bncr_skip", ""),
            )
            for item in raw.get("daly_prsm_dpst_aset_amt_prst", [])
        ]

    # -----------------------------------------------------------------------
    # kt00003 — 추정자산조회요청
    # -----------------------------------------------------------------------

    def get_estimated_asset(
        self,
        query_type: DelistedQueryType = "all",
    ) -> EstimatedAsset:
        """추정자산을 조회한다 (kt00003).

        Args:
            query_type: 상장폐지조회구분. ``"all"``: 전체, ``"exclude_delisted"``: 상장폐지종목제외.

        Returns:
            추정자산 ``EstimatedAsset``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"qry_tp": _DELISTED_QUERY_CODE[query_type]},
            headers=self._headers("kt00003"),
        ))
        return EstimatedAsset(prsm_dpst_aset_amt=raw.get("prsm_dpst_aset_amt", ""))

    # -----------------------------------------------------------------------
    # kt00004 — 계좌평가현황요청
    # -----------------------------------------------------------------------

    def get_account_evaluation(
        self,
        query_type: DelistedQueryType = "all",
        exchange: Literal["KRX", "NXT"] = "KRX",
    ) -> AccountEvaluation:
        """계좌평가현황을 조회한다 (kt00004).

        Args:
            query_type: 상장폐지조회구분. ``"all"``: 전체, ``"exclude_delisted"``: 상장폐지종목제외.
            exchange: 국내거래소구분. ``"KRX"`` 또는 ``"NXT"``.

        Returns:
            계좌평가현황 ``AccountEvaluation`` (종목별 목록 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"qry_tp": _DELISTED_QUERY_CODE[query_type], "dmst_stex_tp": exchange},
            headers=self._headers("kt00004"),
        ))
        holdings = [
            AccountEvaluationItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                rmnd_qty=item.get("rmnd_qty", ""),
                avg_prc=item.get("avg_prc", ""),
                cur_prc=item.get("cur_prc", ""),
                evlt_amt=item.get("evlt_amt", ""),
                pl_amt=item.get("pl_amt", ""),
                pl_rt=item.get("pl_rt", ""),
                loan_dt=item.get("loan_dt", ""),
                pur_amt=item.get("pur_amt", ""),
                setl_remn=item.get("setl_remn", ""),
                pred_buyq=item.get("pred_buyq", ""),
                pred_sellq=item.get("pred_sellq", ""),
                tdy_buyq=item.get("tdy_buyq", ""),
                tdy_sellq=item.get("tdy_sellq", ""),
            )
            for item in raw.get("stk_acnt_evlt_prst", [])
        ]
        return AccountEvaluation(
            acnt_nm=raw.get("acnt_nm", ""),
            brch_nm=raw.get("brch_nm", ""),
            entr=raw.get("entr", ""),
            d2_entra=raw.get("d2_entra", ""),
            tot_est_amt=raw.get("tot_est_amt", ""),
            aset_evlt_amt=raw.get("aset_evlt_amt", ""),
            tot_pur_amt=raw.get("tot_pur_amt", ""),
            prsm_dpst_aset_amt=raw.get("prsm_dpst_aset_amt", ""),
            tdy_lspft=raw.get("tdy_lspft", ""),
            tdy_lspft_rt=raw.get("tdy_lspft_rt", ""),
            lspft_ratio=raw.get("lspft_ratio", ""),
            lspft_rt=raw.get("lspft_rt", ""),
            holdings=holdings,
        )

    # -----------------------------------------------------------------------
    # kt00005 — 체결잔고요청
    # -----------------------------------------------------------------------

    def get_execution_balance(
        self,
        exchange: Literal["KRX", "NXT"] = "KRX",
    ) -> ExecutionBalance:
        """체결잔고를 조회한다 (kt00005).

        Args:
            exchange: 국내거래소구분. ``"KRX"`` 또는 ``"NXT"``.

        Returns:
            체결잔고 ``ExecutionBalance`` (종목별 목록 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"dmst_stex_tp": exchange},
            headers=self._headers("kt00005"),
        ))
        holdings = [
            ExecutionBalanceItem(
                crd_tp=item.get("crd_tp", ""),
                loan_dt=item.get("loan_dt", ""),
                expr_dt=item.get("expr_dt", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                setl_remn=item.get("setl_remn", ""),
                cur_qty=item.get("cur_qty", ""),
                cur_prc=item.get("cur_prc", ""),
                buy_uv=item.get("buy_uv", ""),
                pur_amt=item.get("pur_amt", ""),
                evlt_amt=item.get("evlt_amt", ""),
                evltv_prft=item.get("evltv_prft", ""),
                pl_rt=item.get("pl_rt", ""),
            )
            for item in raw.get("stk_cntr_remn", [])
        ]
        return ExecutionBalance(
            entr=raw.get("entr", ""),
            entr_d1=raw.get("entr_d1", ""),
            entr_d2=raw.get("entr_d2", ""),
            pymn_alow_amt=raw.get("pymn_alow_amt", ""),
            ord_alowa=raw.get("ord_alowa", ""),
            evlt_amt_tot=raw.get("evlt_amt_tot", ""),
            tot_pl_tot=raw.get("tot_pl_tot", ""),
            tot_pl_rt=raw.get("tot_pl_rt", ""),
            holdings=holdings,
        )

    # -----------------------------------------------------------------------
    # kt00007 — 계좌별주문체결내역상세요청
    # -----------------------------------------------------------------------

    def get_order_history_detail(
        self,
        query_type: OrderHistoryQueryType,
        stock_bond_type: StockBondType,
        sell_type: SellType,
        exchange: DomesticExchange = "%",
        order_date: str = "",
        stock_code: str = "",
        from_order_no: str = "",
    ) -> list[OrderHistoryDetailItem]:
        """계좌별주문체결내역상세를 조회한다 (kt00007).

        Args:
            query_type: 조회구분.
                ``"asc"``: 주문순, ``"desc"``: 역순, ``"unfilled"``: 미체결, ``"filled_only"``: 체결내역만.
            stock_bond_type: 주식채권구분. ``"all"``: 전체, ``"stock"``: 주식, ``"bond"``: 채권.
            sell_type: 매도수구분. ``"all"``: 전체, ``"sell"``: 매도, ``"buy"``: 매수.
            exchange: 국내거래소구분. 기본값 ``"%"`` (전체).
            order_date: 주문일자 (``YYYYMMDD`` 형식). 공백이면 당일.
            stock_code: 종목코드. 공백이면 전체 종목.
            from_order_no: 시작주문번호. 공백이면 전체 주문.

        Returns:
            주문체결내역 상세 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {
                "ord_dt": order_date,
                "qry_tp": _ORDER_HISTORY_QUERY_CODE[query_type],
                "stk_bond_tp": _STOCK_BOND_CODE[stock_bond_type],
                "sell_tp": _SELL_TYPE_CODE[sell_type],
                "stk_cd": stock_code,
                "fr_ord_no": from_order_no,
                "dmst_stex_tp": exchange,
            },
            headers=self._headers("kt00007"),
        ))
        return [
            OrderHistoryDetailItem(
                ord_no=item.get("ord_no", ""),
                stk_cd=item.get("stk_cd", ""),
                trde_tp=item.get("trde_tp", ""),
                crd_tp=item.get("crd_tp", ""),
                ord_qty=item.get("ord_qty", ""),
                ord_uv=item.get("ord_uv", ""),
                cnfm_qty=item.get("cnfm_qty", ""),
                acpt_tp=item.get("acpt_tp", ""),
                rsrv_tp=item.get("rsrv_tp", ""),
                ord_tm=item.get("ord_tm", ""),
                ori_ord=item.get("ori_ord", ""),
                stk_nm=item.get("stk_nm", ""),
                io_tp_nm=item.get("io_tp_nm", ""),
                loan_dt=item.get("loan_dt", ""),
                cntr_qty=item.get("cntr_qty", ""),
                cntr_uv=item.get("cntr_uv", ""),
                ord_remnq=item.get("ord_remnq", ""),
                comm_ord_tp=item.get("comm_ord_tp", ""),
                mdfy_cncl=item.get("mdfy_cncl", ""),
                cnfm_tm=item.get("cnfm_tm", ""),
                dmst_stex_tp=item.get("dmst_stex_tp", ""),
                cond_uv=item.get("cond_uv", ""),
            )
            for item in raw.get("acnt_ord_cntr_prps_dtl", [])
        ]

    # -----------------------------------------------------------------------
    # kt00008 — 계좌별익일결제예정내역요청
    # -----------------------------------------------------------------------

    def get_next_day_settlement(
        self,
        from_settlement_no: str = "",
    ) -> NextDaySettlement:
        """계좌별익일결제예정내역을 조회한다 (kt00008).

        Args:
            from_settlement_no: 시작결제번호. 공백이면 전체.

        Returns:
            익일결제예정내역 ``NextDaySettlement``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"strt_dcd_seq": from_settlement_no},
            headers=self._headers("kt00008"),
        ))
        items = [
            NextDaySettlementItem(
                seq=item.get("seq", ""),
                stk_cd=item.get("stk_cd", ""),
                loan_dt=item.get("loan_dt", ""),
                qty=item.get("qty", ""),
                engg_amt=item.get("engg_amt", ""),
                cmsn=item.get("cmsn", ""),
                incm_tax=item.get("incm_tax", ""),
                rstx=item.get("rstx", ""),
                stk_nm=item.get("stk_nm", ""),
                sell_tp=item.get("sell_tp", ""),
                unp=item.get("unp", ""),
                exct_amt=item.get("exct_amt", ""),
                trde_tax=item.get("trde_tax", ""),
                resi_tax=item.get("resi_tax", ""),
                crd_tp=item.get("crd_tp", ""),
            )
            for item in raw.get("acnt_nxdy_setl_frcs_prps_array", [])
        ]
        return NextDaySettlement(
            trde_dt=raw.get("trde_dt", ""),
            setl_dt=raw.get("setl_dt", ""),
            sell_amt_sum=raw.get("sell_amt_sum", ""),
            buy_amt_sum=raw.get("buy_amt_sum", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # kt00009 — 계좌별주문체결현황요청
    # -----------------------------------------------------------------------

    def get_order_execution_status(
        self,
        stock_bond_type: StockBondType,
        market_type: MarketType,
        sell_type: SellType,
        query_type: ExecutionQueryType,
        exchange: DomesticExchange = "KRX",
        order_date: str = "",
        stock_code: str = "",
        from_order_no: str = "",
    ) -> OrderExecutionStatus:
        """계좌별주문체결현황을 조회한다 (kt00009).

        Args:
            stock_bond_type: 주식채권구분. ``"all"``: 전체, ``"stock"``: 주식, ``"bond"``: 채권.
            market_type: 시장구분.
                ``"all"``: 전체, ``"kospi"``: 코스피, ``"kosdaq"``: 코스닥, ``"otcbb"``: OTCBB, ``"ecn"``: ECN.
            sell_type: 매도수구분. ``"all"``: 전체, ``"sell"``: 매도, ``"buy"``: 매수.
            query_type: 조회구분. ``"all"``: 전체, ``"filled"``: 체결.
            exchange: 국내거래소구분. 기본값 ``"KRX"``.
            order_date: 주문일자 (``YYYYMMDD`` 형식). 공백이면 당일.
            stock_code: 종목코드. 공백이면 전체.
            from_order_no: 시작주문번호. 공백이면 전체.

        Returns:
            주문체결현황 ``OrderExecutionStatus``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {
                "ord_dt": order_date,
                "stk_bond_tp": _STOCK_BOND_CODE[stock_bond_type],
                "mrkt_tp": _MARKET_TYPE_CODE[market_type],
                "sell_tp": _SELL_TYPE_CODE[sell_type],
                "qry_tp": _EXECUTION_QUERY_CODE[query_type],
                "stk_cd": stock_code,
                "fr_ord_no": from_order_no,
                "dmst_stex_tp": exchange,
            },
            headers=self._headers("kt00009"),
        ))
        items = [
            OrderExecutionStatusItem(
                stk_bond_tp=item.get("stk_bond_tp", ""),
                ord_no=item.get("ord_no", ""),
                stk_cd=item.get("stk_cd", ""),
                trde_tp=item.get("trde_tp", ""),
                io_tp_nm=item.get("io_tp_nm", ""),
                ord_qty=item.get("ord_qty", ""),
                ord_uv=item.get("ord_uv", ""),
                cnfm_qty=item.get("cnfm_qty", ""),
                rsrv_oppo=item.get("rsrv_oppo", ""),
                cntr_no=item.get("cntr_no", ""),
                acpt_tp=item.get("acpt_tp", ""),
                orig_ord_no=item.get("orig_ord_no", ""),
                stk_nm=item.get("stk_nm", ""),
                setl_tp=item.get("setl_tp", ""),
                crd_deal_tp=item.get("crd_deal_tp", ""),
                cntr_qty=item.get("cntr_qty", ""),
                cntr_uv=item.get("cntr_uv", ""),
                comm_ord_tp=item.get("comm_ord_tp", ""),
                mdfy_cncl_tp=item.get("mdfy_cncl_tp", ""),
                cntr_tm=item.get("cntr_tm", ""),
                dmst_stex_tp=item.get("dmst_stex_tp", ""),
                cond_uv=item.get("cond_uv", ""),
            )
            for item in raw.get("acnt_ord_cntr_prst_array", [])
        ]
        return OrderExecutionStatus(
            sell_grntl_engg_amt=raw.get("sell_grntl_engg_amt", ""),
            buy_engg_amt=raw.get("buy_engg_amt", ""),
            engg_amt=raw.get("engg_amt", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # kt00010 — 주문인출가능금액요청
    # -----------------------------------------------------------------------

    def get_orderable_amount(
        self,
        stock_code: str,
        trade_type: TradeSide,
        price: str,
        io_amount: str = "",
        trade_qty: str = "",
        expected_buy_price: str = "",
    ) -> OrderableAmount:
        """주문인출가능금액을 조회한다 (kt00010).

        Args:
            stock_code: 종목번호.
            trade_type: 매매구분. ``"sell"``: 매도, ``"buy"``: 매수.
            price: 매수가격 (단위: 원).
            io_amount: 입출금액. 공백 허용.
            trade_qty: 매매수량. 공백 허용.
            expected_buy_price: 예상매수단가. 공백 허용.

        Returns:
            주문인출가능금액 ``OrderableAmount``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {
                "io_amt": io_amount,
                "stk_cd": stock_code,
                "trde_tp": _SELL_TYPE_CODE[trade_type],
                "trde_qty": trade_qty,
                "uv": price,
                "exp_buy_unp": expected_buy_price,
            },
            headers=self._headers("kt00010"),
        ))
        return OrderableAmount(
            profa_20ord_alow_amt=raw.get("profa_20ord_alow_amt", ""),
            profa_20ord_alowq=raw.get("profa_20ord_alowq", ""),
            profa_30ord_alow_amt=raw.get("profa_30ord_alow_amt", ""),
            profa_30ord_alowq=raw.get("profa_30ord_alowq", ""),
            profa_40ord_alow_amt=raw.get("profa_40ord_alow_amt", ""),
            profa_40ord_alowq=raw.get("profa_40ord_alowq", ""),
            profa_50ord_alow_amt=raw.get("profa_50ord_alow_amt", ""),
            profa_50ord_alowq=raw.get("profa_50ord_alowq", ""),
            profa_60ord_alow_amt=raw.get("profa_60ord_alow_amt", ""),
            profa_60ord_alowq=raw.get("profa_60ord_alowq", ""),
            profa_100ord_alow_amt=raw.get("profa_100ord_alow_amt", ""),
            profa_100ord_alowq=raw.get("profa_100ord_alowq", ""),
            entr=raw.get("entr", ""),
            repl_amt=raw.get("repl_amt", ""),
            ord_alowa=raw.get("ord_alowa", ""),
            wthd_alowa=raw.get("wthd_alowa", ""),
            nxdy_wthd_alowa=raw.get("nxdy_wthd_alowa", ""),
            d2entra=raw.get("d2entra", ""),
        )

    # -----------------------------------------------------------------------
    # kt00011 — 증거금율별주문가능수량조회요청
    # -----------------------------------------------------------------------

    def get_orderable_quantity(
        self,
        stock_code: str,
        price: str = "",
    ) -> OrderableQuantity:
        """증거금율별주문가능수량을 조회한다 (kt00011).

        Args:
            stock_code: 종목번호.
            price: 매수가격. 공백 허용.

        Returns:
            증거금율별주문가능수량 ``OrderableQuantity``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"stk_cd": stock_code, "uv": price},
            headers=self._headers("kt00011"),
        ))
        return OrderableQuantity(
            stk_profa_rt=raw.get("stk_profa_rt", ""),
            profa_rt=raw.get("profa_rt", ""),
            aplc_rt=raw.get("aplc_rt", ""),
            profa_20ord_alow_amt=raw.get("profa_20ord_alow_amt", ""),
            profa_20ord_alowq=raw.get("profa_20ord_alowq", ""),
            profa_30ord_alow_amt=raw.get("profa_30ord_alow_amt", ""),
            profa_30ord_alowq=raw.get("profa_30ord_alowq", ""),
            profa_40ord_alow_amt=raw.get("profa_40ord_alow_amt", ""),
            profa_40ord_alowq=raw.get("profa_40ord_alowq", ""),
            profa_50ord_alow_amt=raw.get("profa_50ord_alow_amt", ""),
            profa_50ord_alowq=raw.get("profa_50ord_alowq", ""),
            profa_60ord_alow_amt=raw.get("profa_60ord_alow_amt", ""),
            profa_60ord_alowq=raw.get("profa_60ord_alowq", ""),
            profa_100ord_alow_amt=raw.get("profa_100ord_alow_amt", ""),
            profa_100ord_alowq=raw.get("profa_100ord_alowq", ""),
            entr=raw.get("entr", ""),
            repl_amt=raw.get("repl_amt", ""),
            ord_alowa=raw.get("ord_alowa", ""),
        )

    # -----------------------------------------------------------------------
    # kt00012 — 신용보증금율별주문가능수량조회요청
    # -----------------------------------------------------------------------

    def get_credit_orderable_quantity(
        self,
        stock_code: str,
        price: str = "",
    ) -> CreditOrderableQuantity:
        """신용보증금율별주문가능수량을 조회한다 (kt00012).

        Args:
            stock_code: 종목번호.
            price: 매수가격. 공백 허용.

        Returns:
            신용보증금율별주문가능수량 ``CreditOrderableQuantity``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"stk_cd": stock_code, "uv": price},
            headers=self._headers("kt00012"),
        ))
        return CreditOrderableQuantity(
            stk_assr_rt=raw.get("stk_assr_rt", ""),
            stk_assr_rt_nm=raw.get("stk_assr_rt_nm", ""),
            assr_30ord_alow_amt=raw.get("assr_30ord_alow_amt", ""),
            assr_30ord_alowq=raw.get("assr_30ord_alowq", ""),
            assr_40ord_alow_amt=raw.get("assr_40ord_alow_amt", ""),
            assr_40ord_alowq=raw.get("assr_40ord_alowq", ""),
            assr_50ord_alow_amt=raw.get("assr_50ord_alow_amt", ""),
            assr_50ord_alowq=raw.get("assr_50ord_alowq", ""),
            assr_60ord_alow_amt=raw.get("assr_60ord_alow_amt", ""),
            assr_60ord_alowq=raw.get("assr_60ord_alowq", ""),
            entr=raw.get("entr", ""),
            repl_amt=raw.get("repl_amt", ""),
            ord_alowa=raw.get("ord_alowa", ""),
            out_alowa=raw.get("out_alowa", ""),
            min_amt=raw.get("min_amt", ""),
        )

    # -----------------------------------------------------------------------
    # kt00013 — 증거금세부내역조회요청
    # -----------------------------------------------------------------------

    def get_margin_detail(self) -> MarginDetail:
        """증거금세부내역을 조회한다 (kt00013).

        Returns:
            증거금세부내역 ``MarginDetail``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {},
            headers=self._headers("kt00013"),
        ))
        return MarginDetail(
            tdy_reu_alowa=raw.get("tdy_reu_alowa", ""),
            tdy_reu_alowa_fin=raw.get("tdy_reu_alowa_fin", ""),
            pred_reu_alowa=raw.get("pred_reu_alowa", ""),
            pred_reu_alowa_fin=raw.get("pred_reu_alowa_fin", ""),
            use_pos_ch=raw.get("use_pos_ch", ""),
            use_pos_ch_fin=raw.get("use_pos_ch_fin", ""),
            use_pos_repl=raw.get("use_pos_repl", ""),
            use_pos_repl_fin=raw.get("use_pos_repl_fin", ""),
            uncla=raw.get("uncla", ""),
            ord_alow_20=raw.get("20ord_alow_amt", ""),
            ord_alow_30=raw.get("30ord_alow_amt", ""),
            ord_alow_40=raw.get("40ord_alow_amt", ""),
            ord_alow_50=raw.get("50ord_alow_amt", ""),
            ord_alow_60=raw.get("60ord_alow_amt", ""),
            ord_alow_100=raw.get("100ord_alow_amt", ""),
            d2vexct_entr=raw.get("d2vexct_entr", ""),
            d2ch_ord_alow_amt=raw.get("d2ch_ord_alow_amt", ""),
        )

    # -----------------------------------------------------------------------
    # kt00015 — 위탁종합거래내역요청
    # -----------------------------------------------------------------------

    def get_transaction_history(
        self,
        start_dt: str,
        end_dt: str,
        trade_type: str,
        goods_type: GoodsType,
        exchange: DomesticExchange = "%",
        stock_code: str = "",
        currency_code: str = "",
        foreign_exchange_code: str = "",
    ) -> list[TransactionHistoryItem]:
        """위탁종합거래내역을 조회한다 (kt00015).

        Args:
            start_dt: 시작일자 (``YYYYMMDD`` 형식).
            end_dt: 종료일자 (``YYYYMMDD`` 형식).
            trade_type: 구분.
                ``"0"``: 전체, ``"1"``: 입출금, ``"2"``: 입출고, ``"3"``: 매매,
                ``"4"``: 매수, ``"5"``: 매도, ``"6"``: 입금, ``"7"``: 출금.
            goods_type: 상품구분.
                ``"all"``: 전체, ``"domestic_stock"``: 국내주식, ``"fund"``: 수익증권,
                ``"overseas_stock"``: 해외주식, ``"financial"``: 금융상품.
            exchange: 국내거래소구분. 기본값 ``"%"`` (전체).
            stock_code: 종목코드. 공백 허용.
            currency_code: 통화코드. 공백 허용.
            foreign_exchange_code: 해외거래소코드. 공백 허용.

        Returns:
            위탁종합거래내역 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {
                "strt_dt": start_dt,
                "end_dt": end_dt,
                "tp": trade_type,
                "stk_cd": stock_code,
                "crnc_cd": currency_code,
                "gds_tp": _GOODS_TYPE_CODE[goods_type],
                "frgn_stex_code": foreign_exchange_code,
                "dmst_stex_tp": exchange,
            },
            headers=self._headers("kt00015"),
        ))
        return [
            TransactionHistoryItem(
                trde_dt=item.get("trde_dt", ""),
                trde_no=item.get("trde_no", ""),
                rmrk_nm=item.get("rmrk_nm", ""),
                crd_deal_tp_nm=item.get("crd_deal_tp_nm", ""),
                exct_amt=item.get("exct_amt", ""),
                entra_remn=item.get("entra_remn", ""),
                crnc_cd=item.get("crnc_cd", ""),
                trde_kind_nm=item.get("trde_kind_nm", ""),
                stk_nm=item.get("stk_nm", ""),
                trde_amt=item.get("trde_amt", ""),
                io_tp_nm=item.get("io_tp_nm", ""),
                stk_cd=item.get("stk_cd", ""),
                trde_qty_jwa_cnt=item.get("trde_qty_jwa_cnt", ""),
                cmsn=item.get("cmsn", ""),
                proc_tm=item.get("proc_tm", ""),
            )
            for item in raw.get("trst_ovrl_trde_prps_array", [])
        ]

    # -----------------------------------------------------------------------
    # kt00016 — 일별계좌수익률상세현황요청
    # -----------------------------------------------------------------------

    def get_daily_account_return(
        self,
        from_dt: str,
        to_dt: str,
    ) -> DailyAccountReturn:
        """일별계좌수익률상세현황을 조회한다 (kt00016).

        Args:
            from_dt: 평가시작일 (``YYYYMMDD`` 형식).
            to_dt: 평가종료일 (``YYYYMMDD`` 형식).

        Returns:
            일별계좌수익률상세현황 ``DailyAccountReturn``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"fr_dt": from_dt, "to_dt": to_dt},
            headers=self._headers("kt00016"),
        ))
        return DailyAccountReturn(
            mang_empno=raw.get("mang_empno", ""),
            mngr_nm=raw.get("mngr_nm", ""),
            dept_nm=raw.get("dept_nm", ""),
            entr_fr=raw.get("entr_fr", ""),
            entr_to=raw.get("entr_to", ""),
            scrt_evlt_amt_fr=raw.get("scrt_evlt_amt_fr", ""),
            scrt_evlt_amt_to=raw.get("scrt_evlt_amt_to", ""),
            tot_amt_fr=raw.get("tot_amt_fr", ""),
            tot_amt_to=raw.get("tot_amt_to", ""),
            evltv_prft=raw.get("evltv_prft", ""),
            prft_rt=raw.get("prft_rt", ""),
            tern_rt=raw.get("tern_rt", ""),
            termin_tot_trns=raw.get("termin_tot_trns", ""),
            termin_tot_pymn=raw.get("termin_tot_pymn", ""),
        )

    # -----------------------------------------------------------------------
    # kt00017 — 계좌별당일현황요청
    # -----------------------------------------------------------------------

    def get_daily_status(self) -> DailyAccountStatus:
        """계좌별당일현황을 조회한다 (kt00017).

        Returns:
            계좌별당일현황 ``DailyAccountStatus``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {},
            headers=self._headers("kt00017"),
        ))
        return DailyAccountStatus(
            d2_entra=raw.get("d2_entra", ""),
            gnrl_stk_evlt_amt_d2=raw.get("gnrl_stk_evlt_amt_d2", ""),
            crd_loan_d2=raw.get("crd_loan_d2", ""),
            ina_amt=raw.get("ina_amt", ""),
            outa=raw.get("outa", ""),
            sell_amt=raw.get("sell_amt", ""),
            buy_amt=raw.get("buy_amt", ""),
            cmsn=raw.get("cmsn", ""),
            tax=raw.get("tax", ""),
            dvida_amt=raw.get("dvida_amt", ""),
        )

    # -----------------------------------------------------------------------
    # kt00018 — 계좌평가잔고내역요청 (핵심)
    # -----------------------------------------------------------------------

    def get_account_balance(
        self,
        query_type: BalanceQueryType = "combined",
        exchange: Literal["KRX", "NXT"] = "KRX",
    ) -> AccountBalance:
        """계좌평가잔고내역을 조회한다 (kt00018).

        보유 종목별 매입금액·평가금액·평가손익·수익률을 포함한
        계좌 전체 잔고 현황을 반환한다.

        Args:
            query_type: 조회구분. ``"combined"``: 합산, ``"individual"``: 개별.
            exchange: 국내거래소구분. ``"KRX"`` 또는 ``"NXT"``.

        Returns:
            계좌평가잔고내역 ``AccountBalance`` (종목별 목록 포함).

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"qry_tp": _BALANCE_QUERY_CODE[query_type], "dmst_stex_tp": exchange},
            headers=self._headers("kt00018"),
        ))
        holdings = [
            HoldingItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                evltv_prft=item.get("evltv_prft", ""),
                prft_rt=item.get("prft_rt", ""),
                pur_pric=item.get("pur_pric", ""),
                pred_close_pric=item.get("pred_close_pric", ""),
                rmnd_qty=item.get("rmnd_qty", ""),
                trde_able_qty=item.get("trde_able_qty", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_buyq=item.get("pred_buyq", ""),
                pred_sellq=item.get("pred_sellq", ""),
                tdy_buyq=item.get("tdy_buyq", ""),
                tdy_sellq=item.get("tdy_sellq", ""),
                pur_amt=item.get("pur_amt", ""),
                pur_cmsn=item.get("pur_cmsn", ""),
                evlt_amt=item.get("evlt_amt", ""),
                sell_cmsn=item.get("sell_cmsn", ""),
                tax=item.get("tax", ""),
                sum_cmsn=item.get("sum_cmsn", ""),
                poss_rt=item.get("poss_rt", ""),
                crd_tp=item.get("crd_tp", ""),
                crd_tp_nm=item.get("crd_tp_nm", ""),
                crd_loan_dt=item.get("crd_loan_dt", ""),
            )
            for item in raw.get("acnt_evlt_remn_indv_tot", [])
        ]
        return AccountBalance(
            tot_pur_amt=raw.get("tot_pur_amt", ""),
            tot_evlt_amt=raw.get("tot_evlt_amt", ""),
            tot_evlt_pl=raw.get("tot_evlt_pl", ""),
            tot_prft_rt=raw.get("tot_prft_rt", ""),
            prsm_dpst_aset_amt=raw.get("prsm_dpst_aset_amt", ""),
            tot_loan_amt=raw.get("tot_loan_amt", ""),
            tot_crd_loan_amt=raw.get("tot_crd_loan_amt", ""),
            tot_crd_ls_amt=raw.get("tot_crd_ls_amt", ""),
            holdings=holdings,
        )

    # -----------------------------------------------------------------------
    # ka00001 — 계좌번호조회
    # -----------------------------------------------------------------------

    def get_account_numbers(self) -> AccountNumbers:
        """현재 토큰에 연결된 계좌번호 목록을 조회한다 (ka00001).

        Returns:
            계좌번호 목록 ``AccountNumbers``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {},
            headers=self._headers("ka00001"),
        ))
        acct_raw = raw.get("acctNo", "")
        if isinstance(acct_raw, list):
            numbers = [str(a) for a in acct_raw]
        elif acct_raw:
            numbers = [str(acct_raw)]
        else:
            numbers = []
        return AccountNumbers(account_numbers=numbers)

    # -----------------------------------------------------------------------
    # ka01690 — 일별잔고수익률
    # -----------------------------------------------------------------------

    def get_daily_balance_return(self, query_date: str) -> DailyBalanceReturn:
        """일별잔고수익률을 조회한다 (ka01690).

        모의투자를 지원하지 않는 TR이다.

        Args:
            query_date: 조회일자 (``YYYYMMDD`` 형식).

        Returns:
            일별잔고수익률 ``DailyBalanceReturn``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"qry_dt": query_date},
            headers=self._headers("ka01690"),
        ))
        items = [
            DailyBalanceReturnItem(
                cur_prc=item.get("cur_prc", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                rmnd_qty=item.get("rmnd_qty", ""),
                buy_uv=item.get("buy_uv", ""),
                buy_wght=item.get("buy_wght", ""),
                evltv_prft=item.get("evltv_prft", ""),
                prft_rt=item.get("prft_rt", ""),
                evlt_amt=item.get("evlt_amt", ""),
                evlt_wght=item.get("evlt_wght", ""),
            )
            for item in raw.get("day_bal_rt", [])
        ]
        return DailyBalanceReturn(
            dt=raw.get("dt", ""),
            tot_buy_amt=raw.get("tot_buy_amt", ""),
            tot_evlt_amt=raw.get("tot_evlt_amt", ""),
            tot_evltv_prft=raw.get("tot_evltv_prft", ""),
            tot_prft_rt=raw.get("tot_prft_rt", ""),
            dbst_bal=raw.get("dbst_bal", ""),
            day_stk_asst=raw.get("day_stk_asst", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka10072 — 일자별종목별실현손익요청_일자
    # -----------------------------------------------------------------------

    def get_realized_profit_by_date(
        self,
        start_dt: str,
        stock_code: str = "",
    ) -> list[RealizedProfitByDateItem]:
        """일자별종목별실현손익(일자 기준)을 조회한다 (ka10072).

        Args:
            start_dt: 시작일자 (``YYYYMMDD`` 형식).
            stock_code: 종목코드. 공백이면 전체 종목.

        Returns:
            일자별종목별실현손익 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"stk_cd": stock_code, "strt_dt": start_dt},
            headers=self._headers("ka10072"),
        ))
        return [
            RealizedProfitByDateItem(
                stk_nm=item.get("stk_nm", ""),
                cntr_qty=item.get("cntr_qty", ""),
                buy_uv=item.get("buy_uv", ""),
                cntr_pric=item.get("cntr_pric", ""),
                tdy_sel_pl=item.get("tdy_sel_pl", ""),
                pl_rt=item.get("pl_rt", ""),
                stk_cd=item.get("stk_cd", ""),
                tdy_trde_cmsn=item.get("tdy_trde_cmsn", ""),
                tdy_trde_tax=item.get("tdy_trde_tax", ""),
                wthd_alowa=item.get("wthd_alowa", ""),
                loan_dt=item.get("loan_dt", ""),
                crd_tp=item.get("crd_tp", ""),
            )
            for item in raw.get("dt_stk_div_rlzt_pl", [])
        ]

    # -----------------------------------------------------------------------
    # ka10073 — 일자별종목별실현손익요청_기간
    # -----------------------------------------------------------------------

    def get_realized_profit_by_period(
        self,
        start_dt: str,
        end_dt: str,
        stock_code: str = "",
    ) -> list[RealizedProfitByPeriodItem]:
        """일자별종목별실현손익(기간 기준)을 조회한다 (ka10073).

        Args:
            start_dt: 시작일자 (``YYYYMMDD`` 형식).
            end_dt: 종료일자 (``YYYYMMDD`` 형식).
            stock_code: 종목코드. 공백이면 전체 종목.

        Returns:
            일자별종목별실현손익 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"stk_cd": stock_code, "strt_dt": start_dt, "end_dt": end_dt},
            headers=self._headers("ka10073"),
        ))
        return [
            RealizedProfitByPeriodItem(
                dt=item.get("dt", ""),
                tdy_htssel_cmsn=item.get("tdy_htssel_cmsn", ""),
                stk_nm=item.get("stk_nm", ""),
                cntr_qty=item.get("cntr_qty", ""),
                buy_uv=item.get("buy_uv", ""),
                cntr_pric=item.get("cntr_pric", ""),
                tdy_sel_pl=item.get("tdy_sel_pl", ""),
                pl_rt=item.get("pl_rt", ""),
                stk_cd=item.get("stk_cd", ""),
                tdy_trde_cmsn=item.get("tdy_trde_cmsn", ""),
                tdy_trde_tax=item.get("tdy_trde_tax", ""),
                wthd_alowa=item.get("wthd_alowa", ""),
                loan_dt=item.get("loan_dt", ""),
                crd_tp=item.get("crd_tp", ""),
            )
            for item in raw.get("dt_stk_rlzt_pl", [])
        ]

    # -----------------------------------------------------------------------
    # ka10074 — 일자별실현손익요청
    # -----------------------------------------------------------------------

    def get_daily_realized_profit(
        self,
        start_dt: str,
        end_dt: str,
    ) -> DailyRealizedProfit:
        """일자별실현손익을 조회한다 (ka10074).

        실현손익이 발생한 일자에 대해서만 데이터가 채워진다.

        Args:
            start_dt: 시작일자 (``YYYYMMDD`` 형식).
            end_dt: 종료일자 (``YYYYMMDD`` 형식).

        Returns:
            일자별실현손익 ``DailyRealizedProfit``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"strt_dt": start_dt, "end_dt": end_dt},
            headers=self._headers("ka10074"),
        ))
        items = [
            DailyRealizedProfitItem(
                dt=item.get("dt", ""),
                buy_amt=item.get("buy_amt", ""),
                sell_amt=item.get("sell_amt", ""),
                tdy_sel_pl=item.get("tdy_sel_pl", ""),
                tdy_trde_cmsn=item.get("tdy_trde_cmsn", ""),
                tdy_trde_tax=item.get("tdy_trde_tax", ""),
            )
            for item in raw.get("dt_rlzt_pl", [])
        ]
        return DailyRealizedProfit(
            tot_buy_amt=raw.get("tot_buy_amt", ""),
            tot_sell_amt=raw.get("tot_sell_amt", ""),
            rlzt_pl=raw.get("rlzt_pl", ""),
            trde_cmsn=raw.get("trde_cmsn", ""),
            trde_tax=raw.get("trde_tax", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka10075 — 미체결요청
    # -----------------------------------------------------------------------

    def get_unfilled_orders(
        self,
        all_stock_type: Literal["0", "1"],
        trade_type: UnfilledTradeType,
        exchange: ExchangeType = "all",
        stock_code: str = "",
    ) -> list[UnfilledOrderItem]:
        """미체결 주문 목록을 조회한다 (ka10075).

        Args:
            all_stock_type: 전체종목구분. ``"0"``: 전체, ``"1"``: 종목.
            trade_type: 매매구분. ``"all"``: 전체, ``"sell"``: 매도, ``"buy"``: 매수.
            exchange: 거래소구분. ``"all"``: 통합, ``"krx"``: KRX, ``"nxt"``: NXT.
            stock_code: 종목코드. ``all_stock_type="1"`` 일 때 필수.

        Returns:
            미체결 주문 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {
                "all_stk_tp": all_stock_type,
                "trde_tp": _SELL_TYPE_CODE[trade_type],
                "stk_cd": stock_code,
                "stex_tp": _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10075"),
        ))
        return [
            UnfilledOrderItem(
                acnt_no=item.get("acnt_no", ""),
                ord_no=item.get("ord_no", ""),
                stk_cd=item.get("stk_cd", ""),
                ord_stt=item.get("ord_stt", ""),
                stk_nm=item.get("stk_nm", ""),
                ord_qty=item.get("ord_qty", ""),
                ord_pric=item.get("ord_pric", ""),
                oso_qty=item.get("oso_qty", ""),
                orig_ord_no=item.get("orig_ord_no", ""),
                io_tp_nm=item.get("io_tp_nm", ""),
                trde_tp=item.get("trde_tp", ""),
                tm=item.get("tm", ""),
                cntr_pric=item.get("cntr_pric", ""),
                cntr_qty=item.get("cntr_qty", ""),
                cur_prc=item.get("cur_prc", ""),
                stex_tp=item.get("stex_tp", ""),
                stex_tp_txt=item.get("stex_tp_txt", ""),
                sor_yn=item.get("sor_yn", ""),
            )
            for item in raw.get("oso", [])
        ]

    # -----------------------------------------------------------------------
    # ka10076 — 체결요청
    # -----------------------------------------------------------------------

    def get_filled_orders(
        self,
        query_type: FilledQueryType,
        sell_type: SellType,
        exchange: ExchangeType = "all",
        stock_code: str = "",
        order_no: str = "",
    ) -> list[FilledOrderItem]:
        """체결 주문 목록을 조회한다 (ka10076).

        Args:
            query_type: 조회구분. ``"all"``: 전체, ``"by_stock"``: 종목.
            sell_type: 매도수구분. ``"all"``: 전체, ``"sell"``: 매도, ``"buy"``: 매수.
            exchange: 거래소구분. ``"all"``: 통합, ``"krx"``: KRX, ``"nxt"``: NXT.
            stock_code: 종목코드. 공백 허용.
            order_no: 주문번호. 입력한 주문번호보다 과거에 체결된 내역을 조회한다.

        Returns:
            체결 주문 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {
                "stk_cd": stock_code,
                "qry_tp": _FILLED_QUERY_CODE[query_type],
                "sell_tp": _SELL_TYPE_CODE[sell_type],
                "ord_no": order_no,
                "stex_tp": _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10076"),
        ))
        return [
            FilledOrderItem(
                ord_no=item.get("ord_no", ""),
                stk_nm=item.get("stk_nm", ""),
                io_tp_nm=item.get("io_tp_nm", ""),
                ord_pric=item.get("ord_pric", ""),
                ord_qty=item.get("ord_qty", ""),
                cntr_pric=item.get("cntr_pric", ""),
                cntr_qty=item.get("cntr_qty", ""),
                oso_qty=item.get("oso_qty", ""),
                tdy_trde_cmsn=item.get("tdy_trde_cmsn", ""),
                tdy_trde_tax=item.get("tdy_trde_tax", ""),
                ord_stt=item.get("ord_stt", ""),
                trde_tp=item.get("trde_tp", ""),
                orig_ord_no=item.get("orig_ord_no", ""),
                ord_tm=item.get("ord_tm", ""),
                stk_cd=item.get("stk_cd", ""),
                stex_tp=item.get("stex_tp", ""),
                stex_tp_txt=item.get("stex_tp_txt", ""),
                sor_yn=item.get("sor_yn", ""),
            )
            for item in raw.get("cntr", [])
        ]

    # -----------------------------------------------------------------------
    # ka10077 — 당일실현손익상세요청
    # -----------------------------------------------------------------------

    def get_daily_realized_profit_detail(
        self,
        stock_code: str,
    ) -> DailyRealizedProfitDetail:
        """당일실현손익상세를 조회한다 (ka10077).

        Args:
            stock_code: 종목코드.

        Returns:
            당일실현손익상세 ``DailyRealizedProfitDetail``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10077"),
        ))
        items = [
            DailyRealizedProfitDetailItem(
                stk_nm=item.get("stk_nm", ""),
                cntr_qty=item.get("cntr_qty", ""),
                buy_uv=item.get("buy_uv", ""),
                cntr_pric=item.get("cntr_pric", ""),
                tdy_sel_pl=item.get("tdy_sel_pl", ""),
                pl_rt=item.get("pl_rt", ""),
                tdy_trde_cmsn=item.get("tdy_trde_cmsn", ""),
                tdy_trde_tax=item.get("tdy_trde_tax", ""),
                stk_cd=item.get("stk_cd", ""),
            )
            for item in raw.get("tdy_rlzt_pl_dtl", [])
        ]
        return DailyRealizedProfitDetail(
            tdy_rlzt_pl=raw.get("tdy_rlzt_pl", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka10085 — 계좌수익률요청
    # -----------------------------------------------------------------------

    def get_account_return(
        self,
        exchange: ExchangeType = "all",
    ) -> list[AccountReturnItem]:
        """계좌수익률을 조회한다 (ka10085).

        Args:
            exchange: 거래소구분. ``"all"``: 통합, ``"krx"``: KRX, ``"nxt"``: NXT.

        Returns:
            계좌수익률 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"stex_tp": _EXCHANGE_CODE[exchange]},
            headers=self._headers("ka10085"),
        ))
        return [
            AccountReturnItem(
                dt=item.get("dt", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pur_pric=item.get("pur_pric", ""),
                pur_amt=item.get("pur_amt", ""),
                rmnd_qty=item.get("rmnd_qty", ""),
                tdy_sel_pl=item.get("tdy_sel_pl", ""),
                tdy_trde_cmsn=item.get("tdy_trde_cmsn", ""),
                tdy_trde_tax=item.get("tdy_trde_tax", ""),
                crd_tp=item.get("crd_tp", ""),
                loan_dt=item.get("loan_dt", ""),
                setl_remn=item.get("setl_remn", ""),
                clrn_alow_qty=item.get("clrn_alow_qty", ""),
                crd_amt=item.get("crd_amt", ""),
                crd_int=item.get("crd_int", ""),
                expr_dt=item.get("expr_dt", ""),
            )
            for item in raw.get("acnt_prft_rt", [])
        ]

    # -----------------------------------------------------------------------
    # ka10088 — 미체결 분할주문 상세
    # -----------------------------------------------------------------------

    def get_split_order_detail(
        self,
        order_no: str,
    ) -> list[SplitOrderDetailItem]:
        """미체결 분할주문 상세를 조회한다 (ka10088).

        Args:
            order_no: 주문번호.

        Returns:
            미체결 분할주문 상세 목록.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {"ord_no": order_no},
            headers=self._headers("ka10088"),
        ))
        return [
            SplitOrderDetailItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                ord_no=item.get("ord_no", ""),
                ord_qty=item.get("ord_qty", ""),
                ord_pric=item.get("ord_pric", ""),
                osop_qty=item.get("osop_qty", ""),
                io_tp_nm=item.get("io_tp_nm", ""),
                trde_tp=item.get("trde_tp", ""),
                sell_tp=item.get("sell_tp", ""),
                cntr_qty=item.get("cntr_qty", ""),
                ord_stt=item.get("ord_stt", ""),
                cur_prc=item.get("cur_prc", ""),
                stex_tp=item.get("stex_tp", ""),
                stex_tp_txt=item.get("stex_tp_txt", ""),
            )
            for item in raw.get("osop", [])
        ]

    # -----------------------------------------------------------------------
    # ka10170 — 당일매매일지요청
    # -----------------------------------------------------------------------

    def get_daily_trade_journal(
        self,
        single_stock_type: SingleStockType,
        cash_credit_type: CashCreditType,
        base_date: str = "",
    ) -> DailyTradeJournal:
        """당일매매일지를 조회한다 (ka10170).

        Args:
            single_stock_type: 단주구분.
                ``"today_buy_sell"``: 당일매수에 대한 당일매도, ``"today_sell_all"``: 당일매도 전체.
            cash_credit_type: 현금신용구분.
                ``"all"``: 전체, ``"cash"``: 현금매매만, ``"credit"``: 신용매매만.
            base_date: 기준일자 (``YYYYMMDD`` 형식).
                공백이면 금일 데이터. 최근 2개월까지 제공.

        Returns:
            당일매매일지 ``DailyTradeJournal``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._ACNT_PATH,
            {
                "base_dt": base_date,
                "ottks_tp": _SINGLE_STOCK_CODE[single_stock_type],
                "ch_crd_tp": _CASH_CREDIT_CODE[cash_credit_type],
            },
            headers=self._headers("ka10170"),
        ))
        items = [
            DailyTradeJournalItem(
                stk_nm=item.get("stk_nm", ""),
                buy_avg_pric=item.get("buy_avg_pric", ""),
                buy_qty=item.get("buy_qty", ""),
                sel_avg_pric=item.get("sel_avg_pric", ""),
                sell_qty=item.get("sell_qty", ""),
                cmsn_alm_tax=item.get("cmsn_alm_tax", ""),
                pl_amt=item.get("pl_amt", ""),
                sell_amt=item.get("sell_amt", ""),
                buy_amt=item.get("buy_amt", ""),
                prft_rt=item.get("prft_rt", ""),
                stk_cd=item.get("stk_cd", ""),
            )
            for item in raw.get("tdy_trde_diary", [])
        ]
        return DailyTradeJournal(
            tot_sell_amt=raw.get("tot_sell_amt", ""),
            tot_buy_amt=raw.get("tot_buy_amt", ""),
            tot_cmsn_tax=raw.get("tot_cmsn_tax", ""),
            tot_exct_amt=raw.get("tot_exct_amt", ""),
            tot_pl_amt=raw.get("tot_pl_amt", ""),
            tot_prft_rt=raw.get("tot_prft_rt", ""),
            items=items,
        )
