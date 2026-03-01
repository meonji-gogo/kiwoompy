"""kiwoompy 공통 데이터 모델 — 타입 별칭 및 TR별 요청/응답 dataclass."""

from __future__ import annotations

from dataclasses import dataclass, field
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
# OAuth 인증 — au10001, au10002
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


@dataclass(frozen=True)
class RevokeTokenRequest:
    """접근토큰 폐기 요청 (au10002).

    Args:
        appkey: 키움증권 앱 키.
        secretkey: 키움증권 시크릿 키.
        token: 폐기할 접근토큰.
    """

    appkey: str
    secretkey: str
    token: str


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00001
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FxDepositItem:
    """외화예수금 항목 (kt00001 ``stk_entr_prst`` 배열 원소).

    Args:
        crnc_cd: 통화코드 (예: ``"USD"``).
        fx_entr: 외화예수금.
        pymn_alow_amt: 출금가능금액.
        ord_alow_amt_entr: 주문가능금액(예수금).
    """

    crnc_cd: str
    fx_entr: str
    fc_krw_repl_evlta: str      # 원화대용평가금
    fc_trst_profa: str          # 해외주식증거금
    pymn_alow_amt: str          # 출금가능금액
    pymn_alow_amt_entr: str     # 출금가능금액(예수금)
    ord_alow_amt_entr: str      # 주문가능금액(예수금)
    fc_uncla: str               # 외화미수(합계)
    fc_ch_uncla: str            # 외화현금미수금
    dly_amt: str                # 연체료
    d1_fx_entr: str             # d+1외화예수금
    d2_fx_entr: str             # d+2외화예수금
    d3_fx_entr: str             # d+3외화예수금
    d4_fx_entr: str             # d+4외화예수금


@dataclass(frozen=True)
class DepositDetail:
    """예수금상세현황 응답 (kt00001).

    Args:
        entr: 예수금 (단위: 원).
        pymn_alow_amt: 출금가능금액 (단위: 원).
        ord_alow_amt: 주문가능금액 (단위: 원).
        d1_entra: D+1 추정예수금 (단위: 원).
        d2_entra: D+2 추정예수금 (단위: 원).
        fx_deposits: 외화예수금 목록.
    """

    entr: str                   # 예수금
    profa_ch: str               # 주식증거금현금
    pymn_alow_amt: str          # 출금가능금액
    ord_alow_amt: str           # 주문가능금액
    d1_entra: str               # d+1추정예수금
    d1_pymn_alow_amt: str       # d+1출금가능금액
    d2_entra: str               # d+2추정예수금
    d2_pymn_alow_amt: str       # d+2출금가능금액
    repl_amt: str               # 대용금평가금액(합계)
    ch_uncla: str               # 현금미수금
    nrpy_loan: str              # 미상환융자금
    crd_grnt_rt: str            # 신용담보비율
    fx_deposits: list[FxDepositItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00002
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DailyEstimatedAssetItem:
    """일별추정예탁자산 항목 (kt00002 배열 원소).

    Args:
        dt: 일자 (``YYYYMMDD`` 형식).
        entr: 예수금 (단위: 원).
        prsm_dpst_aset_amt: 추정예탁자산 (단위: 원).
    """

    dt: str                             # 일자
    entr: str                           # 예수금
    grnt_use_amt: str                   # 담보대출금
    crd_loan: str                       # 신용융자금
    ls_grnt: str                        # 대주담보금
    repl_amt: str                       # 대용금
    prsm_dpst_aset_amt: str             # 추정예탁자산
    prsm_dpst_aset_amt_bncr_skip: str   # 추정예탁자산수익증권제외


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00003
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EstimatedAsset:
    """추정자산조회 응답 (kt00003).

    Args:
        prsm_dpst_aset_amt: 추정예탁자산 (단위: 원).
    """

    prsm_dpst_aset_amt: str


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00004
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AccountEvaluationItem:
    """종목별계좌평가현황 항목 (kt00004 배열 원소).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        rmnd_qty: 보유수량 (단위: 주).
        avg_prc: 평균단가 (단위: 원).
        cur_prc: 현재가 (단위: 원).
        evlt_amt: 평가금액 (단위: 원).
        pl_amt: 손익금액 (단위: 원).
        pl_rt: 손익율 (단위: %).
    """

    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    rmnd_qty: str   # 보유수량
    avg_prc: str    # 평균단가
    cur_prc: str    # 현재가
    evlt_amt: str   # 평가금액
    pl_amt: str     # 손익금액
    pl_rt: str      # 손익율
    loan_dt: str    # 대출일
    pur_amt: str    # 매입금액
    setl_remn: str  # 결제잔고
    pred_buyq: str  # 전일매수수량
    pred_sellq: str # 전일매도수량
    tdy_buyq: str   # 금일매수수량
    tdy_sellq: str  # 금일매도수량


@dataclass(frozen=True)
class AccountEvaluation:
    """계좌평가현황 응답 (kt00004).

    Args:
        acnt_nm: 계좌명.
        entr: 예수금 (단위: 원).
        aset_evlt_amt: 예탁자산평가액 (단위: 원).
        tot_pur_amt: 총매입금액 (단위: 원).
        prsm_dpst_aset_amt: 추정예탁자산 (단위: 원).
        tdy_lspft_rt: 당일손익율 (단위: %).
        holdings: 종목별 평가 목록.
    """

    acnt_nm: str            # 계좌명
    brch_nm: str            # 지점명
    entr: str               # 예수금
    d2_entra: str           # D+2추정예수금
    tot_est_amt: str        # 유가잔고평가액
    aset_evlt_amt: str      # 예탁자산평가액
    tot_pur_amt: str        # 총매입금액
    prsm_dpst_aset_amt: str # 추정예탁자산
    tdy_lspft: str          # 당일투자손익
    tdy_lspft_rt: str       # 당일손익율
    lspft_ratio: str        # 당월손익율
    lspft_rt: str           # 누적손익율
    holdings: list[AccountEvaluationItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00005
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExecutionBalanceItem:
    """종목별체결잔고 항목 (kt00005 배열 원소).

    Args:
        stk_cd: 종목번호.
        stk_nm: 종목명.
        cur_qty: 현재잔고 (단위: 주).
        cur_prc: 현재가 (단위: 원).
        buy_uv: 매입단가 (단위: 원).
        evlt_amt: 평가금액 (단위: 원).
        evltv_prft: 평가손익 (단위: 원).
        pl_rt: 손익률 (단위: %).
    """

    crd_tp: str     # 신용구분
    loan_dt: str    # 대출일
    expr_dt: str    # 만기일
    stk_cd: str     # 종목번호
    stk_nm: str     # 종목명
    setl_remn: str  # 결제잔고
    cur_qty: str    # 현재잔고
    cur_prc: str    # 현재가
    buy_uv: str     # 매입단가
    pur_amt: str    # 매입금액
    evlt_amt: str   # 평가금액
    evltv_prft: str # 평가손익
    pl_rt: str      # 손익률


@dataclass(frozen=True)
class ExecutionBalance:
    """체결잔고 응답 (kt00005).

    Args:
        entr: 예수금 (단위: 원).
        evlt_amt_tot: 평가금액합계 (단위: 원).
        tot_pl_tot: 총손익합계 (단위: 원).
        tot_pl_rt: 총손익률 (단위: %).
        holdings: 종목별 체결잔고 목록.
    """

    entr: str           # 예수금
    entr_d1: str        # 예수금D+1
    entr_d2: str        # 예수금D+2
    pymn_alow_amt: str  # 출금가능금액
    ord_alowa: str      # 주문가능현금
    evlt_amt_tot: str   # 평가금액합계
    tot_pl_tot: str     # 총손익합계
    tot_pl_rt: str      # 총손익률
    holdings: list[ExecutionBalanceItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00007
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OrderHistoryDetailItem:
    """계좌별주문체결내역상세 항목 (kt00007 배열 원소).

    Args:
        ord_no: 주문번호.
        stk_cd: 종목번호.
        stk_nm: 종목명.
        trde_tp: 매매구분.
        ord_qty: 주문수량 (단위: 주).
        cntr_qty: 체결수량 (단위: 주).
        cntr_uv: 체결단가 (단위: 원).
        ord_tm: 주문시간.
    """

    ord_no: str         # 주문번호
    stk_cd: str         # 종목번호
    trde_tp: str        # 매매구분
    crd_tp: str         # 신용구분
    ord_qty: str        # 주문수량
    ord_uv: str         # 주문단가
    cnfm_qty: str       # 확인수량
    acpt_tp: str        # 접수구분
    rsrv_tp: str        # 반대여부
    ord_tm: str         # 주문시간
    ori_ord: str        # 원주문
    stk_nm: str         # 종목명
    io_tp_nm: str       # 주문구분
    loan_dt: str        # 대출일
    cntr_qty: str       # 체결수량
    cntr_uv: str        # 체결단가
    ord_remnq: str      # 주문잔량
    comm_ord_tp: str    # 통신구분
    mdfy_cncl: str      # 정정취소
    cnfm_tm: str        # 확인시간
    dmst_stex_tp: str   # 국내거래소구분
    cond_uv: str        # 스톱가


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00008
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NextDaySettlementItem:
    """계좌별익일결제예정내역 항목 (kt00008 배열 원소).

    Args:
        stk_cd: 종목번호.
        stk_nm: 종목명.
        qty: 수량 (단위: 주).
        engg_amt: 약정금액 (단위: 원).
        exct_amt: 정산금액 (단위: 원).
        sell_tp: 매도수구분.
    """

    seq: str        # 일련번호
    stk_cd: str     # 종목번호
    loan_dt: str    # 대출일
    qty: str        # 수량
    engg_amt: str   # 약정금액
    cmsn: str       # 수수료
    incm_tax: str   # 소득세
    rstx: str       # 농특세
    stk_nm: str     # 종목명
    sell_tp: str    # 매도수구분
    unp: str        # 단가
    exct_amt: str   # 정산금액
    trde_tax: str   # 거래세
    resi_tax: str   # 주민세
    crd_tp: str     # 신용구분


@dataclass(frozen=True)
class NextDaySettlement:
    """계좌별익일결제예정내역 응답 (kt00008).

    Args:
        trde_dt: 매매일자.
        setl_dt: 결제일자.
        sell_amt_sum: 매도정산합 (단위: 원).
        buy_amt_sum: 매수정산합 (단위: 원).
        items: 결제예정내역 목록.
    """

    trde_dt: str        # 매매일자
    setl_dt: str        # 결제일자
    sell_amt_sum: str   # 매도정산합
    buy_amt_sum: str    # 매수정산합
    items: list[NextDaySettlementItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00009
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OrderExecutionStatusItem:
    """계좌별주문체결현황 항목 (kt00009 배열 원소).

    Args:
        ord_no: 주문번호.
        stk_cd: 종목번호.
        stk_nm: 종목명.
        trde_tp: 매매구분.
        ord_qty: 주문수량 (단위: 주).
        cntr_qty: 체결수량 (단위: 주).
        cntr_uv: 체결단가 (단위: 원).
    """

    stk_bond_tp: str    # 주식채권구분
    ord_no: str         # 주문번호
    stk_cd: str         # 종목번호
    trde_tp: str        # 매매구분
    io_tp_nm: str       # 주문유형구분
    ord_qty: str        # 주문수량
    ord_uv: str         # 주문단가
    cnfm_qty: str       # 확인수량
    rsrv_oppo: str      # 예약/반대
    cntr_no: str        # 체결번호
    acpt_tp: str        # 접수구분
    orig_ord_no: str    # 원주문번호
    stk_nm: str         # 종목명
    setl_tp: str        # 결제구분
    crd_deal_tp: str    # 신용거래구분
    cntr_qty: str       # 체결수량
    cntr_uv: str        # 체결단가
    comm_ord_tp: str    # 통신구분
    mdfy_cncl_tp: str   # 정정/취소구분
    cntr_tm: str        # 체결시간
    dmst_stex_tp: str   # 국내거래소구분
    cond_uv: str        # 스톱가


@dataclass(frozen=True)
class OrderExecutionStatus:
    """계좌별주문체결현황 응답 (kt00009).

    Args:
        sell_grntl_engg_amt: 매도약정금액 (단위: 원).
        buy_engg_amt: 매수약정금액 (단위: 원).
        engg_amt: 약정금액 (단위: 원).
        items: 주문체결현황 목록.
    """

    sell_grntl_engg_amt: str    # 매도약정금액
    buy_engg_amt: str           # 매수약정금액
    engg_amt: str               # 약정금액
    items: list[OrderExecutionStatusItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00010
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OrderableAmount:
    """주문인출가능금액 응답 (kt00010).

    Args:
        entr: 예수금 (단위: 원).
        ord_alowa: 주문가능현금 (단위: 원).
        wthd_alowa: 인출가능금액 (단위: 원).
        profa_20ord_alow_amt: 증거금20% 주문가능금액 (단위: 원).
        profa_20ord_alowq: 증거금20% 주문가능수량 (단위: 주).
    """

    profa_20ord_alow_amt: str       # 증거금20%주문가능금액
    profa_20ord_alowq: str          # 증거금20%주문가능수량
    profa_30ord_alow_amt: str       # 증거금30%주문가능금액
    profa_30ord_alowq: str          # 증거금30%주문가능수량
    profa_40ord_alow_amt: str       # 증거금40%주문가능금액
    profa_40ord_alowq: str          # 증거금40%주문가능수량
    profa_50ord_alow_amt: str       # 증거금50%주문가능금액
    profa_50ord_alowq: str          # 증거금50%주문가능수량
    profa_60ord_alow_amt: str       # 증거금60%주문가능금액
    profa_60ord_alowq: str          # 증거금60%주문가능수량
    profa_100ord_alow_amt: str      # 증거금100%주문가능금액
    profa_100ord_alowq: str         # 증거금100%주문가능수량
    entr: str                       # 예수금
    repl_amt: str                   # 대용금
    ord_alowa: str                  # 주문가능현금
    wthd_alowa: str                 # 인출가능금액
    nxdy_wthd_alowa: str            # 익일인출가능금액
    d2entra: str                    # D2추정예수금


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00011
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OrderableQuantity:
    """증거금율별주문가능수량 응답 (kt00011).

    Args:
        stk_profa_rt: 종목증거금율.
        profa_rt: 계좌증거금율.
        entr: 예수금 (단위: 원).
        ord_alowa: 주문가능현금 (단위: 원).
    """

    stk_profa_rt: str           # 종목증거금율
    profa_rt: str               # 계좌증거금율
    aplc_rt: str                # 적용증거금율
    profa_20ord_alow_amt: str   # 증거금20%주문가능금액
    profa_20ord_alowq: str      # 증거금20%주문가능수량
    profa_30ord_alow_amt: str   # 증거금30%주문가능금액
    profa_30ord_alowq: str      # 증거금30%주문가능수량
    profa_40ord_alow_amt: str   # 증거금40%주문가능금액
    profa_40ord_alowq: str      # 증거금40%주문가능수량
    profa_50ord_alow_amt: str   # 증거금50%주문가능금액
    profa_50ord_alowq: str      # 증거금50%주문가능수량
    profa_60ord_alow_amt: str   # 증거금60%주문가능금액
    profa_60ord_alowq: str      # 증거금60%주문가능수량
    profa_100ord_alow_amt: str  # 증거금100%주문가능금액
    profa_100ord_alowq: str     # 증거금100%주문가능수량
    entr: str                   # 예수금
    repl_amt: str               # 대용금
    ord_alowa: str              # 주문가능현금


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00012
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CreditOrderableQuantity:
    """신용보증금율별주문가능수량 응답 (kt00012).

    Args:
        stk_assr_rt: 종목보증금율.
        entr: 예수금 (단위: 원).
        ord_alowa: 주문가능현금 (단위: 원).
    """

    stk_assr_rt: str            # 종목보증금율
    stk_assr_rt_nm: str         # 종목보증금율명
    assr_30ord_alow_amt: str    # 보증금30%주문가능금액
    assr_30ord_alowq: str       # 보증금30%주문가능수량
    assr_40ord_alow_amt: str    # 보증금40%주문가능금액
    assr_40ord_alowq: str       # 보증금40%주문가능수량
    assr_50ord_alow_amt: str    # 보증금50%주문가능금액
    assr_50ord_alowq: str       # 보증금50%주문가능수량
    assr_60ord_alow_amt: str    # 보증금60%주문가능금액
    assr_60ord_alowq: str       # 보증금60%주문가능수량
    entr: str                   # 예수금
    repl_amt: str               # 대용금
    ord_alowa: str              # 주문가능현금
    out_alowa: str              # 미수가능금액
    min_amt: str                # 미수불가금액


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00013
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MarginDetail:
    """증거금세부내역 응답 (kt00013).

    Args:
        use_pos_ch: 사용가능현금 (단위: 원).
        use_pos_repl: 사용가능대용 (단위: 원).
        uncla: 미수금 (단위: 원).
    """

    tdy_reu_alowa: str          # 금일재사용가능금액
    tdy_reu_alowa_fin: str      # 금일재사용가능금액최종
    pred_reu_alowa: str         # 전일재사용가능금액
    pred_reu_alowa_fin: str     # 전일재사용가능금액최종
    use_pos_ch: str             # 사용가능현금
    use_pos_ch_fin: str         # 사용가능현금최종
    use_pos_repl: str           # 사용가능대용
    use_pos_repl_fin: str       # 사용가능대용최종
    uncla: str                  # 미수금
    ord_alow_20: str            # 20%주문가능금액
    ord_alow_30: str            # 30%주문가능금액
    ord_alow_40: str            # 40%주문가능금액
    ord_alow_50: str            # 50%주문가능금액
    ord_alow_60: str            # 60%주문가능금액
    ord_alow_100: str           # 100%주문가능금액
    d2vexct_entr: str           # D2가정산예수금
    d2ch_ord_alow_amt: str      # D2현금주문가능금액


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00015
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TransactionHistoryItem:
    """위탁종합거래내역 항목 (kt00015 배열 원소).

    Args:
        trde_dt: 거래일자.
        rmrk_nm: 적요명.
        trde_amt: 거래금액 (단위: 원).
        exct_amt: 정산금액 (단위: 원).
        entra_remn: 예수금잔고 (단위: 원).
        stk_cd: 종목코드.
        stk_nm: 종목명.
    """

    trde_dt: str            # 거래일자
    trde_no: str            # 거래번호
    rmrk_nm: str            # 적요명
    crd_deal_tp_nm: str     # 신용거래구분명
    exct_amt: str           # 정산금액
    entra_remn: str         # 예수금잔고
    crnc_cd: str            # 통화코드
    trde_kind_nm: str       # 거래종류명
    stk_nm: str             # 종목명
    trde_amt: str           # 거래금액
    io_tp_nm: str           # 입출구분명
    stk_cd: str             # 종목코드
    trde_qty_jwa_cnt: str   # 거래수량/좌수
    cmsn: str               # 수수료
    proc_tm: str            # 처리시간


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00016
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DailyAccountReturn:
    """일별계좌수익률상세현황 응답 (kt00016).

    Args:
        evltv_prft: 평가손익 (단위: 원).
        prft_rt: 수익률 (단위: %).
        tot_amt_fr: 순자산액계_초 (단위: 원).
        tot_amt_to: 순자산액계_말 (단위: 원).
    """

    mang_empno: str         # 관리사원번호
    mngr_nm: str            # 관리자명
    dept_nm: str            # 관리자지점
    entr_fr: str            # 예수금_초
    entr_to: str            # 예수금_말
    scrt_evlt_amt_fr: str   # 유가증권평가금액_초
    scrt_evlt_amt_to: str   # 유가증권평가금액_말
    tot_amt_fr: str         # 순자산액계_초
    tot_amt_to: str         # 순자산액계_말
    evltv_prft: str         # 평가손익
    prft_rt: str            # 수익률
    tern_rt: str            # 회전율
    termin_tot_trns: str    # 기간내총입금
    termin_tot_pymn: str    # 기간내총출금


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00017
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DailyAccountStatus:
    """계좌별당일현황 응답 (kt00017).

    Args:
        d2_entra: D+2추정예수금 (단위: 원).
        sell_amt: 매도금액 (단위: 원).
        buy_amt: 매수금액 (단위: 원).
        cmsn: 수수료 (단위: 원).
        tax: 세금 (단위: 원).
    """

    d2_entra: str                       # D+2추정예수금
    gnrl_stk_evlt_amt_d2: str           # 일반주식평가금액D+2
    crd_loan_d2: str                    # 신용융자금D+2
    ina_amt: str                        # 입금금액
    outa: str                           # 출금금액
    sell_amt: str                       # 매도금액
    buy_amt: str                        # 매수금액
    cmsn: str                           # 수수료
    tax: str                            # 세금
    dvida_amt: str                      # 배당금액


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — kt00018 (핵심: 계좌평가잔고내역)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class HoldingItem:
    """계좌평가잔고 종목 항목 (kt00018 배열 원소).

    Args:
        stk_cd: 종목번호.
        stk_nm: 종목명.
        rmnd_qty: 보유수량 (단위: 주).
        trde_able_qty: 매매가능수량 (단위: 주).
        cur_prc: 현재가 (단위: 원).
        pur_pric: 매입가 (단위: 원).
        pur_amt: 매입금액 (단위: 원).
        evlt_amt: 평가금액 (단위: 원).
        evltv_prft: 평가손익 (단위: 원).
        prft_rt: 수익률(%) (단위: %).
        poss_rt: 보유비중(%) (단위: %).
    """

    stk_cd: str         # 종목번호
    stk_nm: str         # 종목명
    evltv_prft: str     # 평가손익
    prft_rt: str        # 수익률(%)
    pur_pric: str       # 매입가
    pred_close_pric: str  # 전일종가
    rmnd_qty: str       # 보유수량
    trde_able_qty: str  # 매매가능수량
    cur_prc: str        # 현재가
    pred_buyq: str      # 전일매수수량
    pred_sellq: str     # 전일매도수량
    tdy_buyq: str       # 금일매수수량
    tdy_sellq: str      # 금일매도수량
    pur_amt: str        # 매입금액
    pur_cmsn: str       # 매입수수료
    evlt_amt: str       # 평가금액
    sell_cmsn: str      # 평가수수료
    tax: str            # 세금
    sum_cmsn: str       # 수수료합
    poss_rt: str        # 보유비중(%)
    crd_tp: str         # 신용구분
    crd_tp_nm: str      # 신용구분명
    crd_loan_dt: str    # 대출일


@dataclass(frozen=True)
class AccountBalance:
    """계좌평가잔고내역 응답 (kt00018).

    Args:
        tot_pur_amt: 총매입금액 (단위: 원).
        tot_evlt_amt: 총평가금액 (단위: 원).
        tot_evlt_pl: 총평가손익금액 (단위: 원).
        tot_prft_rt: 총수익률(%) (단위: %).
        prsm_dpst_aset_amt: 추정예탁자산 (단위: 원).
        holdings: 종목별 잔고 목록.
    """

    tot_pur_amt: str            # 총매입금액
    tot_evlt_amt: str           # 총평가금액
    tot_evlt_pl: str            # 총평가손익금액
    tot_prft_rt: str            # 총수익률(%)
    prsm_dpst_aset_amt: str     # 추정예탁자산
    tot_loan_amt: str           # 총대출금
    tot_crd_loan_amt: str       # 총융자금액
    tot_crd_ls_amt: str         # 총대주금액
    holdings: list[HoldingItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka00001
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AccountNumbers:
    """계좌번호조회 응답 (ka00001).

    Args:
        account_numbers: 계좌번호 목록.
    """

    account_numbers: list[str]


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka01690
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DailyBalanceReturnItem:
    """일별잔고수익률 종목 항목 (ka01690 배열 원소).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        rmnd_qty: 보유수량 (단위: 주).
        buy_uv: 매입단가 (단위: 원).
        evlt_amt: 평가금액 (단위: 원).
        evltv_prft: 평가손익 (단위: 원).
        prft_rt: 수익률 (단위: %).
    """

    cur_prc: str        # 현재가
    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    rmnd_qty: str       # 보유수량
    buy_uv: str         # 매입단가
    buy_wght: str       # 매수비중
    evltv_prft: str     # 평가손익
    prft_rt: str        # 수익률
    evlt_amt: str       # 평가금액
    evlt_wght: str      # 평가비중


@dataclass(frozen=True)
class DailyBalanceReturn:
    """일별잔고수익률 응답 (ka01690).

    Args:
        dt: 일자.
        tot_buy_amt: 총 매입가 (단위: 원).
        tot_evlt_amt: 총 평가금액 (단위: 원).
        tot_prft_rt: 수익률 (단위: %).
        day_bal_rt: 종목별 잔고수익률 목록.
    """

    dt: str             # 일자
    tot_buy_amt: str    # 총매입가
    tot_evlt_amt: str   # 총평가금액
    tot_evltv_prft: str # 총평가손익
    tot_prft_rt: str    # 수익률
    dbst_bal: str       # 예수금
    day_stk_asst: str   # 추정자산
    items: list[DailyBalanceReturnItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka10072 / ka10073
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RealizedProfitByDateItem:
    """일자별종목별실현손익 항목 (ka10072 배열 원소).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cntr_qty: 체결량 (단위: 주).
        buy_uv: 매입단가 (단위: 원).
        cntr_pric: 체결가 (단위: 원).
        tdy_sel_pl: 당일매도손익 (단위: 원).
        pl_rt: 손익율 (단위: %).
    """

    stk_nm: str         # 종목명
    cntr_qty: str       # 체결량
    buy_uv: str         # 매입단가
    cntr_pric: str      # 체결가
    tdy_sel_pl: str     # 당일매도손익
    pl_rt: str          # 손익율
    stk_cd: str         # 종목코드
    tdy_trde_cmsn: str  # 당일매매수수료
    tdy_trde_tax: str   # 당일매매세금
    wthd_alowa: str     # 인출가능금액
    loan_dt: str        # 대출일
    crd_tp: str         # 신용구분


@dataclass(frozen=True)
class RealizedProfitByPeriodItem:
    """일자별종목별실현손익 항목 (ka10073 배열 원소).

    Args:
        dt: 일자.
        stk_cd: 종목코드.
        stk_nm: 종목명.
        tdy_sel_pl: 당일매도손익 (단위: 원).
        pl_rt: 손익율 (단위: %).
    """

    dt: str             # 일자
    tdy_htssel_cmsn: str  # 당일hts매도수수료
    stk_nm: str         # 종목명
    cntr_qty: str       # 체결량
    buy_uv: str         # 매입단가
    cntr_pric: str      # 체결가
    tdy_sel_pl: str     # 당일매도손익
    pl_rt: str          # 손익율
    stk_cd: str         # 종목코드
    tdy_trde_cmsn: str  # 당일매매수수료
    tdy_trde_tax: str   # 당일매매세금
    wthd_alowa: str     # 인출가능금액
    loan_dt: str        # 대출일
    crd_tp: str         # 신용구분


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka10074
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DailyRealizedProfitItem:
    """일자별실현손익 항목 (ka10074 배열 원소).

    Args:
        dt: 일자.
        buy_amt: 매수금액 (단위: 원).
        sell_amt: 매도금액 (단위: 원).
        tdy_sel_pl: 당일매도손익 (단위: 원).
    """

    dt: str             # 일자
    buy_amt: str        # 매수금액
    sell_amt: str       # 매도금액
    tdy_sel_pl: str     # 당일매도손익
    tdy_trde_cmsn: str  # 당일매매수수료
    tdy_trde_tax: str   # 당일매매세금


@dataclass(frozen=True)
class DailyRealizedProfit:
    """일자별실현손익 응답 (ka10074).

    Args:
        tot_buy_amt: 총매수금액 (단위: 원).
        tot_sell_amt: 총매도금액 (단위: 원).
        rlzt_pl: 실현손익 (단위: 원).
        items: 일자별 실현손익 목록.
    """

    tot_buy_amt: str    # 총매수금액
    tot_sell_amt: str   # 총매도금액
    rlzt_pl: str        # 실현손익
    trde_cmsn: str      # 매매수수료
    trde_tax: str       # 매매세금
    items: list[DailyRealizedProfitItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka10075 (미체결)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class UnfilledOrderItem:
    """미체결 주문 항목 (ka10075 배열 원소).

    Args:
        ord_no: 주문번호.
        stk_cd: 종목코드.
        stk_nm: 종목명.
        ord_qty: 주문수량 (단위: 주).
        ord_pric: 주문가격 (단위: 원).
        oso_qty: 미체결수량 (단위: 주).
        io_tp_nm: 주문구분.
        trde_tp: 매매구분.
        ord_stt: 주문상태.
    """

    acnt_no: str        # 계좌번호
    ord_no: str         # 주문번호
    stk_cd: str         # 종목코드
    ord_stt: str        # 주문상태
    stk_nm: str         # 종목명
    ord_qty: str        # 주문수량
    ord_pric: str       # 주문가격
    oso_qty: str        # 미체결수량
    orig_ord_no: str    # 원주문번호
    io_tp_nm: str       # 주문구분
    trde_tp: str        # 매매구분
    tm: str             # 시간
    cntr_pric: str      # 체결가
    cntr_qty: str       # 체결량
    cur_prc: str        # 현재가
    stex_tp: str        # 거래소구분
    stex_tp_txt: str    # 거래소구분텍스트
    sor_yn: str         # SOR 여부


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka10076 (체결)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FilledOrderItem:
    """체결 주문 항목 (ka10076 배열 원소).

    Args:
        ord_no: 주문번호.
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cntr_pric: 체결가 (단위: 원).
        cntr_qty: 체결량 (단위: 주).
        oso_qty: 미체결수량 (단위: 주).
        ord_stt: 주문상태.
    """

    ord_no: str         # 주문번호
    stk_nm: str         # 종목명
    io_tp_nm: str       # 주문구분
    ord_pric: str       # 주문가격
    ord_qty: str        # 주문수량
    cntr_pric: str      # 체결가
    cntr_qty: str       # 체결량
    oso_qty: str        # 미체결수량
    tdy_trde_cmsn: str  # 당일매매수수료
    tdy_trde_tax: str   # 당일매매세금
    ord_stt: str        # 주문상태
    trde_tp: str        # 매매구분
    orig_ord_no: str    # 원주문번호
    ord_tm: str         # 주문시간
    stk_cd: str         # 종목코드
    stex_tp: str        # 거래소구분
    stex_tp_txt: str    # 거래소구분텍스트
    sor_yn: str         # SOR 여부


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka10077
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DailyRealizedProfitDetailItem:
    """당일실현손익상세 항목 (ka10077 배열 원소).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cntr_qty: 체결량 (단위: 주).
        tdy_sel_pl: 당일매도손익 (단위: 원).
        pl_rt: 손익율 (단위: %).
    """

    stk_nm: str         # 종목명
    cntr_qty: str       # 체결량
    buy_uv: str         # 매입단가
    cntr_pric: str      # 체결가
    tdy_sel_pl: str     # 당일매도손익
    pl_rt: str          # 손익율
    tdy_trde_cmsn: str  # 당일매매수수료
    tdy_trde_tax: str   # 당일매매세금
    stk_cd: str         # 종목코드


@dataclass(frozen=True)
class DailyRealizedProfitDetail:
    """당일실현손익상세 응답 (ka10077).

    Args:
        tdy_rlzt_pl: 당일실현손익 (단위: 원).
        items: 당일실현손익 상세 목록.
    """

    tdy_rlzt_pl: str
    items: list[DailyRealizedProfitDetailItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka10085
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AccountReturnItem:
    """계좌수익률 항목 (ka10085 배열 원소).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (단위: 원).
        pur_pric: 매입가 (단위: 원).
        rmnd_qty: 보유수량 (단위: 주).
        tdy_sel_pl: 당일매도손익 (단위: 원).
    """

    dt: str             # 일자
    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pur_pric: str       # 매입가
    pur_amt: str        # 매입금액
    rmnd_qty: str       # 보유수량
    tdy_sel_pl: str     # 당일매도손익
    tdy_trde_cmsn: str  # 당일매매수수료
    tdy_trde_tax: str   # 당일매매세금
    crd_tp: str         # 신용구분
    loan_dt: str        # 대출일
    setl_remn: str      # 결제잔고
    clrn_alow_qty: str  # 청산가능수량
    crd_amt: str        # 신용금액
    crd_int: str        # 신용이자
    expr_dt: str        # 만기일


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka10088
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SplitOrderDetailItem:
    """미체결 분할주문 상세 항목 (ka10088 배열 원소).

    Args:
        ord_no: 주문번호.
        stk_cd: 종목코드.
        stk_nm: 종목명.
        ord_qty: 주문수량 (단위: 주).
        osop_qty: 미체결수량 (단위: 주).
        ord_stt: 주문상태.
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    ord_no: str         # 주문번호
    ord_qty: str        # 주문수량
    ord_pric: str       # 주문가격
    osop_qty: str       # 미체결수량
    io_tp_nm: str       # 주문구분
    trde_tp: str        # 매매구분
    sell_tp: str        # 매도/수 구분
    cntr_qty: str       # 체결량
    ord_stt: str        # 주문상태
    cur_prc: str        # 현재가
    stex_tp: str        # 거래소구분
    stex_tp_txt: str    # 거래소구분텍스트


# ---------------------------------------------------------------------------
# 계좌·잔고 조회 — ka10170
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DailyTradeJournalItem:
    """당일매매일지 항목 (ka10170 배열 원소).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        buy_qty: 매수수량 (단위: 주).
        sell_qty: 매도수량 (단위: 주).
        pl_amt: 손익금액 (단위: 원).
        prft_rt: 수익률 (단위: %).
    """

    stk_nm: str         # 종목명
    buy_avg_pric: str   # 매수평균가
    buy_qty: str        # 매수수량
    sel_avg_pric: str   # 매도평균가
    sell_qty: str       # 매도수량
    cmsn_alm_tax: str   # 수수료_제세금
    pl_amt: str         # 손익금액
    sell_amt: str       # 매도금액
    buy_amt: str        # 매수금액
    prft_rt: str        # 수익률
    stk_cd: str         # 종목코드


@dataclass(frozen=True)
class DailyTradeJournal:
    """당일매매일지 응답 (ka10170).

    Args:
        tot_sell_amt: 총매도금액 (단위: 원).
        tot_buy_amt: 총매수금액 (단위: 원).
        tot_pl_amt: 총손익금액 (단위: 원).
        tot_prft_rt: 총수익률 (단위: %).
        items: 당일매매일지 목록.
    """

    tot_sell_amt: str   # 총매도금액
    tot_buy_amt: str    # 총매수금액
    tot_cmsn_tax: str   # 총수수료_세금
    tot_exct_amt: str   # 총정산금액
    tot_pl_amt: str     # 총손익금액
    tot_prft_rt: str    # 총수익률
    items: list[DailyTradeJournalItem] = field(default_factory=list)


# ---------------------------------------------------------------------------
# 주식 주문 — kt10000 / kt10001 (매수/매도)
# ---------------------------------------------------------------------------

type OrderTradeType = Literal[
    "limit",            # 보통(지정가)
    "market",           # 시장가
    "conditional",      # 조건부지정가
    "best",             # 최유리지정가
    "priority",         # 최우선지정가
    "limit_ioc",        # 보통(IOC)
    "market_ioc",       # 시장가(IOC)
    "best_ioc",         # 최유리(IOC)
    "limit_fok",        # 보통(FOK)
    "market_fok",       # 시장가(FOK)
    "best_fok",         # 최유리(FOK)
    "stop",             # 스톱지정가
    "mid",              # 중간가
    "mid_ioc",          # 중간가(IOC)
    "mid_fok",          # 중간가(FOK)
    "pre_market",       # 장시작전시간외
    "after_hours",      # 시간외단일가
    "post_market",      # 장마감후시간외
]
"""매매구분 (사람이 읽기 쉬운 키 → API 코드로 자동 변환됨).

- ``"limit"``: 보통(지정가) — API ``"0"``
- ``"market"``: 시장가 — API ``"3"``
- ``"conditional"``: 조건부지정가 — API ``"5"``
- ``"best"``: 최유리지정가 — API ``"6"``
- ``"priority"``: 최우선지정가 — API ``"7"``
- ``"limit_ioc"``: 보통(IOC) — API ``"10"``
- ``"market_ioc"``: 시장가(IOC) — API ``"13"``
- ``"best_ioc"``: 최유리(IOC) — API ``"16"``
- ``"limit_fok"``: 보통(FOK) — API ``"20"``
- ``"market_fok"``: 시장가(FOK) — API ``"23"``
- ``"best_fok"``: 최유리(FOK) — API ``"26"``
- ``"stop"``: 스톱지정가 — API ``"28"``
- ``"mid"``: 중간가 — API ``"29"``
- ``"mid_ioc"``: 중간가(IOC) — API ``"30"``
- ``"mid_fok"``: 중간가(FOK) — API ``"31"``
- ``"pre_market"``: 장시작전시간외 — API ``"61"``
- ``"after_hours"``: 시간외단일가 — API ``"62"``
- ``"post_market"``: 장마감후시간외 — API ``"81"``
"""

type OrderExchange = Literal["KRX", "NXT", "SOR"]
"""주문 국내거래소구분.

- ``"KRX"``: 한국거래소
- ``"NXT"``: 넥스트트레이드
- ``"SOR"``: 최선주문집행
"""


@dataclass(frozen=True)
class OrderResponse:
    """주식 매수/매도 주문 응답 (kt10000, kt10001).

    Args:
        ord_no: 주문번호.
        dmst_stex_tp: 국내거래소구분.
    """

    ord_no: str         # 주문번호
    dmst_stex_tp: str   # 국내거래소구분


# ---------------------------------------------------------------------------
# 주식 주문 — kt10002 (정정)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ModifyOrderResponse:
    """주식 정정주문 응답 (kt10002, kt10008).

    Args:
        ord_no: 주문번호 (새로 발급된 정정 주문번호).
        base_orig_ord_no: 모주문번호 (최초 원주문번호).
        mdfy_qty: 정정수량 (단위: 주).
        dmst_stex_tp: 국내거래소구분.
    """

    ord_no: str             # 주문번호
    base_orig_ord_no: str   # 모주문번호
    mdfy_qty: str           # 정정수량
    dmst_stex_tp: str       # 국내거래소구분


# ---------------------------------------------------------------------------
# 주식 주문 — kt10003 (취소)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CancelOrderResponse:
    """주식 취소주문 응답 (kt10003, kt10009).

    Args:
        ord_no: 주문번호 (새로 발급된 취소 주문번호).
        base_orig_ord_no: 모주문번호 (최초 원주문번호).
        cncl_qty: 취소수량 (단위: 주).
    """

    ord_no: str             # 주문번호
    base_orig_ord_no: str   # 모주문번호
    cncl_qty: str           # 취소수량


# ---------------------------------------------------------------------------
# 4단계 — 국내주식 시세·종목정보 공통 Literal 타입
# ---------------------------------------------------------------------------

type DisplayType = Literal["qty", "amount"]
"""일별주가 표시구분.

- ``"qty"``: 수량 — API ``"0"``
- ``"amount"``: 금액(백만원) — API ``"1"``
"""

type NewStockRightsType = Literal["all", "rights_cert", "rights_deed"]
"""신주인수권구분.

- ``"all"``: 전체 — API ``"00"``
- ``"rights_cert"``: 신주인수권증권 — API ``"05"``
- ``"rights_deed"``: 신주인수권증서 — API ``"07"``
"""

type InstitutionTradeType = Literal["sell", "buy"]
"""기관 매매구분 (순매도/순매수).

- ``"sell"``: 순매도 — API ``"1"``
- ``"buy"``: 순매수 — API ``"2"``
"""

type EstimatedPriceType = Literal["buy", "sell"]
"""추정단가구분.

- ``"buy"``: 매수단가 — API ``"1"``
- ``"sell"``: 매도단가 — API ``"2"``
"""

type CreditQueryType = Literal["loan", "short"]
"""신용매매동향 조회구분.

- ``"loan"``: 융자 — API ``"1"``
- ``"short"``: 대주 — API ``"2"``
"""

type HighLowSelectType = Literal["high", "low"]
"""신고저구분.

- ``"high"``: 신고가 — API ``"1"``
- ``"low"``: 신저가 — API ``"2"``
"""

type PERType = Literal["low_pbr", "high_pbr", "low_per", "high_per", "low_roe", "high_roe"]
"""고저PER 구분.

- ``"low_pbr"``: 저PBR — API ``"1"``
- ``"high_pbr"``: 고PBR — API ``"2"``
- ``"low_per"``: 저PER — API ``"3"``
- ``"high_per"``: 고PER — API ``"4"``
- ``"low_roe"``: 저ROE — API ``"5"``
- ``"high_roe"``: 고ROE — API ``"6"``
"""

type TodayPrevType = Literal["today", "prev"]
"""당일전일구분.

- ``"today"``: 당일 — API ``"1"``
- ``"prev"``: 전일 — API ``"2"``
"""

type TickMinType = Literal["tick", "minute"]
"""틱/분 구분.

- ``"tick"``: 틱 — API ``"0"``
- ``"minute"``: 분 — API ``"1"``
"""

type StkMarketType = Literal[
    "kospi", "kosdaq", "kotc", "konex", "etn", "loss_etn", "gold",
    "vol_etn", "infra", "elw", "mutual_fund", "rights", "reit",
    "etf", "high_yield"
]
"""종목정보 리스트 시장구분.

- ``"kospi"``: 코스피 — API ``"0"``
- ``"kosdaq"``: 코스닥 — API ``"10"``
- ``"kotc"``: K-OTC — API ``"30"``
- ``"konex"``: 코넥스 — API ``"50"``
- ``"etn"``: ETN — API ``"60"``
- ``"loss_etn"``: 손실제한 ETN — API ``"70"``
- ``"gold"``: 금현물 — API ``"80"``
- ``"vol_etn"``: 변동성 ETN — API ``"90"``
- ``"infra"``: 인프라투융자 — API ``"2"``
- ``"elw"``: ELW — API ``"3"``
- ``"mutual_fund"``: 뮤추얼펀드 — API ``"4"``
- ``"rights"``: 신주인수권 — API ``"5"``
- ``"reit"``: 리츠종목 — API ``"6"``
- ``"rights_deed"``: 신주인수권증서 — API ``"7"``
- ``"etf"``: ETF — API ``"8"``
- ``"high_yield"``: 하이일드펀드 — API ``"9"``
"""

type SectorMarketType = Literal["kospi", "kosdaq", "kospi200", "kospi100", "krx100"]
"""업종코드 리스트 시장구분.

- ``"kospi"``: 코스피(거래소) — API ``"0"``
- ``"kosdaq"``: 코스닥 — API ``"1"``
- ``"kospi200"``: KOSPI200 — API ``"2"``
- ``"kospi100"``: KOSPI100 — API ``"4"``
- ``"krx100"``: KRX100(통합지수) — API ``"7"``
"""

type MrkcondExchangeType = Literal["krx", "nxt", "all"]
"""시세·종목정보 거래소구분.

- ``"krx"``: KRX — API ``"1"``
- ``"nxt"``: NXT — API ``"2"``
- ``"all"``: 통합 — API ``"3"``
"""

type MrktType3 = Literal["all", "kospi", "kosdaq"]
"""시장구분 3자리 코드 (전체/코스피/코스닥).

- ``"all"``: 전체 — API ``"000"``
- ``"kospi"``: 코스피 — API ``"001"``
- ``"kosdaq"``: 코스닥 — API ``"101"``
"""

type MrktType3Ext = Literal["all", "kospi", "kosdaq", "kospi200"]
"""시장구분 3자리 (가격급등락용, KOSPI200 포함).

- ``"all"``: 전체 — API ``"000"``
- ``"kospi"``: 코스피 — API ``"001"``
- ``"kosdaq"``: 코스닥 — API ``"101"``
- ``"kospi200"``: 코스피200 — API ``"201"``
"""

type IntraAmtQtyType = Literal["amount_qty", "amount", "qty"]
"""금액수량구분 (장중투자자별).

- ``"amount_qty"``: 금액&수량 — API ``"1"``
"""

type AfterAmtQtyType = Literal["amount", "qty"]
"""금액수량구분 (장마감후투자자별).

- ``"amount"``: 금액 — API ``"1"``
- ``"qty"``: 수량 — API ``"2"``
"""

type AfterTradeType = Literal["net_buy", "buy", "sell"]
"""장마감후 매매구분.

- ``"net_buy"``: 순매수 — API ``"0"``
- ``"buy"``: 매수 — API ``"1"``
- ``"sell"``: 매도 — API ``"2"``
"""

type InvestorType = Literal[
    "foreign", "institution", "trust", "insurance", "bank",
    "pension", "gov", "other_corp"
]
"""투자자별 (장중투자자별).

- ``"foreign"``: 외국인 — API ``"6"``
- ``"institution"``: 기관계 — API ``"7"``
- ``"trust"``: 투신 — API ``"1"``
- ``"insurance"``: 보험 — API ``"0"``
- ``"bank"``: 은행 — API ``"2"``
- ``"pension"``: 연기금 — API ``"3"``
- ``"gov"``: 국가 — API ``"4"``
- ``"other_corp"``: 기타법인 — API ``"5"``
"""

type InvestorType2 = Literal[
    "individual", "foreign", "financial_inv", "trust", "private_fund",
    "other_fin", "bank", "insurance", "pension", "gov", "other_corp", "institution"
]
"""투자자구분 (투자자별일별매매종목).

- ``"individual"``: 개인 — API ``"8000"``
- ``"foreign"``: 외국인 — API ``"9000"``
- ``"financial_inv"``: 금융투자 — API ``"1000"``
- ``"trust"``: 투신 — API ``"3000"``
- ``"private_fund"``: 사모펀드 — API ``"3100"``
- ``"other_fin"``: 기타금융 — API ``"5000"``
- ``"bank"``: 은행 — API ``"4000"``
- ``"insurance"``: 보험 — API ``"2000"``
- ``"pension"``: 연기금 — API ``"6000"``
- ``"gov"``: 국가 — API ``"7000"``
- ``"other_corp"``: 기타법인 — API ``"7100"``
- ``"institution"``: 기관계 — API ``"9999"``
"""

type AmtQtyType = Literal["amount", "qty"]
"""금액수량구분 (종목별투자자기관별).

- ``"amount"``: 금액 — API ``"1"``
- ``"qty"``: 수량 — API ``"2"``
"""

type InvestorTradeType = Literal["net_buy", "buy", "sell"]
"""종목별투자자 매매구분.

- ``"net_buy"``: 순매수 — API ``"0"``
- ``"buy"``: 매수 — API ``"1"``
- ``"sell"``: 매도 — API ``"2"``
"""

type UnitType = Literal["thousand", "single"]
"""단위구분.

- ``"thousand"``: 천주 — API ``"1000"``
- ``"single"``: 단주 — API ``"1"``
"""


# ---------------------------------------------------------------------------
# 4단계 — 국내주식 시세 응답 모델 (mrkcond)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OrderbookLevel:
    """호가 단일 레벨 (매도/매수 각 호가·잔량·직전대비).

    Args:
        price: 호가 (단위: 원).
        qty: 잔량 (단위: 주).
        qty_change: 잔량직전대비.
    """

    price: str      # 호가 (원)
    qty: str        # 잔량 (주)
    qty_change: str # 잔량직전대비


@dataclass(frozen=True)
class Orderbook:
    """주식호가 응답 (ka10004).

    Args:
        base_time: 호가잔량기준시간 (HHMMSS).
        sell_levels: 매도호가 1~10차선 리스트 (인덱스 0=최우선).
        buy_levels: 매수호가 1~10차선 리스트 (인덱스 0=최우선).
        tot_sell_qty: 총매도잔량.
        tot_buy_qty: 총매수잔량.
        tot_sell_qty_change: 총매도잔량직전대비.
        tot_buy_qty_change: 총매수잔량직전대비.
        ovt_sell_qty: 시간외매도잔량.
        ovt_buy_qty: 시간외매수잔량.
        ovt_sell_qty_change: 시간외매도잔량대비.
        ovt_buy_qty_change: 시간외매수잔량대비.
    """

    base_time: str                      # 호가잔량기준시간
    sell_levels: list[OrderbookLevel]   # 매도호가 1~10 (인덱스 0=최우선)
    buy_levels: list[OrderbookLevel]    # 매수호가 1~10 (인덱스 0=최우선)
    tot_sell_qty: str                   # 총매도잔량
    tot_buy_qty: str                    # 총매수잔량
    tot_sell_qty_change: str            # 총매도잔량직전대비
    tot_buy_qty_change: str             # 총매수잔량직전대비
    ovt_sell_qty: str                   # 시간외매도잔량
    ovt_buy_qty: str                    # 시간외매수잔량
    ovt_sell_qty_change: str            # 시간외매도잔량대비
    ovt_buy_qty_change: str             # 시간외매수잔량대비


@dataclass(frozen=True)
class StockPeriodItem:
    """주식일주월시분 단일 항목 (ka10005).

    Args:
        date: 날짜 (YYYYMMDD).
        open_pric: 시가 (원).
        high_pric: 고가 (원).
        low_pric: 저가 (원).
        close_pric: 종가 (원).
        pre: 대비 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        trde_prica: 거래대금 (백만원).
        for_poss: 외인보유 (%).
        for_wght: 외인비중 (%).
        for_netprps: 외인순매수 (주).
        orgn_netprps: 기관순매수 (주).
        ind_netprps: 개인순매수 (주).
        crd_remn_rt: 신용잔고율 (%).
        frgn: 외국계.
        prm: 프로그램.
    """

    date: str           # 날짜
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    close_pric: str     # 종가
    pre: str            # 대비
    flu_rt: str         # 등락률
    trde_qty: str       # 거래량
    trde_prica: str     # 거래대금
    for_poss: str       # 외인보유
    for_wght: str       # 외인비중
    for_netprps: str    # 외인순매수
    orgn_netprps: str   # 기관순매수
    ind_netprps: str    # 개인순매수
    crd_remn_rt: str    # 신용잔고율
    frgn: str           # 외국계
    prm: str            # 프로그램


@dataclass(frozen=True)
class StockPeriods:
    """주식일주월시분 응답 (ka10005).

    Args:
        items: 기간별 OHLCV 리스트.
    """

    items: list[StockPeriodItem]


@dataclass(frozen=True)
class StockMinutes:
    """주식시분 응답 (ka10006).

    Args:
        date: 날짜 (YYYYMMDD).
        open_pric: 시가 (원).
        high_pric: 고가 (원).
        low_pric: 저가 (원).
        close_pric: 종가/현재가 (원).
        pre: 대비 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        trde_prica: 거래대금 (백만원).
        cntr_str: 체결강도.
    """

    date: str       # 날짜
    open_pric: str  # 시가
    high_pric: str  # 고가
    low_pric: str   # 저가
    close_pric: str # 종가
    pre: str        # 대비
    flu_rt: str     # 등락률
    trde_qty: str   # 거래량
    trde_prica: str # 거래대금
    cntr_str: str   # 체결강도


@dataclass(frozen=True)
class MarketSummary:
    """시세표성정보 응답 (ka10007). 종목의 현재가·호가·예상체결 등 종합 시세.

    Args:
        stk_nm: 종목명.
        stk_cd: 종목코드.
        date: 날짜 (YYYYMMDD).
        tm: 시간 (HHMMSS).
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        open_pric: 시가 (원).
        high_pric: 고가 (원).
        low_pric: 저가 (원).
        trde_qty: 거래량 (주).
        trde_prica: 거래대금 (백만원).
        pred_close_pric: 전일종가 (원).
        upl_pric: 상한가 (원).
        lst_pric: 하한가 (원).
        exp_cntr_pric: 예상체결가 (원).
        exp_cntr_qty: 예상체결량 (주).
        tot_buy_req: 총매수잔량.
        tot_sel_req: 총매도잔량.
    """

    stk_nm: str         # 종목명
    stk_cd: str         # 종목코드
    date: str           # 날짜
    tm: str             # 시간
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    trde_qty: str       # 거래량
    trde_prica: str     # 거래대금
    pred_close_pric: str    # 전일종가
    upl_pric: str           # 상한가
    lst_pric: str           # 하한가
    exp_cntr_pric: str      # 예상체결가
    exp_cntr_qty: str       # 예상체결량
    tot_buy_req: str        # 총매수잔량
    tot_sel_req: str        # 총매도잔량


@dataclass(frozen=True)
class DailyPriceItem:
    """일별주가 단일 항목 (ka10086).

    Args:
        date: 날짜 (YYYYMMDD).
        open_pric: 시가 (원).
        high_pric: 고가 (원).
        low_pric: 저가 (원).
        close_pric: 종가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        for_netprps: 외인순매수 (주).
        orgn_netprps: 기관순매수 (주).
        ind_netprps: 개인순매수 (주).
        for_poss: 외인보유 (%).
        for_wght: 외인비중 (%).
        crd_remn_rt: 신용잔고율 (%).
    """

    date: str           # 날짜
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    close_pric: str     # 종가
    flu_rt: str         # 등락률
    trde_qty: str       # 거래량
    for_netprps: str    # 외인순매수
    orgn_netprps: str   # 기관순매수
    ind_netprps: str    # 개인순매수
    for_poss: str       # 외인보유
    for_wght: str       # 외인비중
    crd_remn_rt: str    # 신용잔고율


@dataclass(frozen=True)
class DailyPrices:
    """일별주가 응답 (ka10086).

    Args:
        items: 일별 OHLCV 리스트.
    """

    items: list[DailyPriceItem]


@dataclass(frozen=True)
class AfterhoursOrderbook:
    """시간외단일가 호가 응답 (ka10087).

    Args:
        base_time: 호가잔량기준시간 (HHMMSS).
        ovt_cur_prc: 시간외단일가 현재가 (원).
        ovt_flu_rt: 시간외단일가 등락률 (%).
        ovt_acc_trde_qty: 시간외단일가 누적거래량 (주).
        ovt_sell_tot: 시간외단일가 매도호가총잔량.
        ovt_buy_tot: 시간외단일가 매수호가총잔량.
        sel_bid_tot: 매도호가총잔량.
        buy_bid_tot: 매수호가총잔량.
    """

    base_time: str          # 호가잔량기준시간
    ovt_cur_prc: str        # 시간외단일가 현재가
    ovt_flu_rt: str         # 시간외단일가 등락률
    ovt_acc_trde_qty: str   # 시간외단일가 누적거래량
    ovt_sell_tot: str       # 시간외단일가 매도호가총잔량
    ovt_buy_tot: str        # 시간외단일가 매수호가총잔량
    sel_bid_tot: str        # 매도호가총잔량
    buy_bid_tot: str        # 매수호가총잔량


@dataclass(frozen=True)
class NewStockRightsItem:
    """신주인수권 시세 단일 항목 (ka10011).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        pred_pre: 전일대비 (원).
        flu_rt: 등락률 (%).
        acc_trde_qty: 누적거래량 (주).
        open_pric: 시가 (원).
        high_pric: 고가 (원).
        low_pric: 저가 (원).
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락률
    acc_trde_qty: str   # 누적거래량
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가


@dataclass(frozen=True)
class NewStockRightsPrices:
    """신주인수권전체시세 응답 (ka10011).

    Args:
        items: 신주인수권 시세 리스트.
    """

    items: list[NewStockRightsItem]


@dataclass(frozen=True)
class DailyInstitutionStockItem:
    """일별기관매매종목 단일 항목 (ka10044).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        netprps_qty: 순매수수량 (주).
        netprps_amt: 순매수금액 (백만원).
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    netprps_qty: str    # 순매수수량
    netprps_amt: str    # 순매수금액


@dataclass(frozen=True)
class DailyInstitutionStocks:
    """일별기관매매종목 응답 (ka10044).

    Args:
        items: 기관매매종목 리스트.
    """

    items: list[DailyInstitutionStockItem]


@dataclass(frozen=True)
class StockInstitutionTrendItem:
    """종목별기관매매추이 단일 항목 (ka10045).

    Args:
        dt: 일자 (YYYYMMDD).
        close_pric: 종가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        orgn_dt_acc: 기관기간누적.
        orgn_daly_nettrde_qty: 기관일별순매매수량.
        for_dt_acc: 외인기간누적.
        for_daly_nettrde_qty: 외인일별순매매수량.
        limit_exh_rt: 한도소진율 (%).
    """

    dt: str                     # 일자
    close_pric: str             # 종가
    flu_rt: str                 # 등락률
    trde_qty: str               # 거래량
    orgn_dt_acc: str            # 기관기간누적
    orgn_daly_nettrde_qty: str  # 기관일별순매매수량
    for_dt_acc: str             # 외인기간누적
    for_daly_nettrde_qty: str   # 외인일별순매매수량
    limit_exh_rt: str           # 한도소진율


@dataclass(frozen=True)
class StockInstitutionTrend:
    """종목별기관매매추이 응답 (ka10045).

    Args:
        orgn_prsm_avg_pric: 기관추정평균가 (원).
        for_prsm_avg_pric: 외인추정평균가 (원).
        items: 일별 추이 리스트.
    """

    orgn_prsm_avg_pric: str
    for_prsm_avg_pric: str
    items: list[StockInstitutionTrendItem]


@dataclass(frozen=True)
class ExecutionStrengthItem:
    """체결강도추이 단일 항목 (ka10046, ka10047).

    Args:
        time_or_dt: 시간(HHMMSS) 또는 일자(YYYYMMDD).
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        cntr_str: 체결강도.
        cntr_str_5: 체결강도 5분/5일.
        cntr_str_20: 체결강도 20분/20일.
        cntr_str_60: 체결강도 60분/60일.
    """

    time_or_dt: str     # 시간 또는 일자
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    trde_qty: str       # 거래량
    cntr_str: str       # 체결강도
    cntr_str_5: str     # 체결강도 5분/5일
    cntr_str_20: str    # 체결강도 20분/20일
    cntr_str_60: str    # 체결강도 60분/60일


@dataclass(frozen=True)
class ExecutionStrength:
    """체결강도추이 응답 (ka10046, ka10047).

    Args:
        items: 체결강도 시계열 리스트.
    """

    items: list[ExecutionStrengthItem]


@dataclass(frozen=True)
class IntradayInvestorItem:
    """장중투자자별매매 단일 항목 (ka10063).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        acc_trde_qty: 누적거래량 (주).
        netprps_qty: 순매수수량 (주).
        buy_qty: 매수수량 (주).
        sell_qty: 매도수량 (주).
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    acc_trde_qty: str   # 누적거래량
    netprps_qty: str    # 순매수수량
    buy_qty: str        # 매수수량
    sell_qty: str       # 매도수량


@dataclass(frozen=True)
class IntradayInvestorTrading:
    """장중투자자별매매 응답 (ka10063).

    Args:
        items: 종목별 투자자 매매 리스트.
    """

    items: list[IntradayInvestorItem]


@dataclass(frozen=True)
class AfterCloseInvestorItem:
    """장마감후투자자별매매 단일 항목 (ka10066).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        ind_invsr: 개인투자자.
        frgnr_invsr: 외국인투자자.
        orgn: 기관계.
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    trde_qty: str       # 거래량
    ind_invsr: str      # 개인투자자
    frgnr_invsr: str    # 외국인투자자
    orgn: str           # 기관계


@dataclass(frozen=True)
class AfterCloseInvestorTrading:
    """장마감후투자자별매매 응답 (ka10066).

    Args:
        items: 종목별 투자자 매매 리스트.
    """

    items: list[AfterCloseInvestorItem]


@dataclass(frozen=True)
class BrokerStockTrendItem:
    """증권사별종목매매동향 단일 항목 (ka10078).

    Args:
        dt: 일자 (YYYYMMDD).
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        acc_trde_qty: 누적거래량 (주).
        netprps_qty: 순매수수량 (주).
        buy_qty: 매수수량 (주).
        sell_qty: 매도수량 (주).
    """

    dt: str             # 일자
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    acc_trde_qty: str   # 누적거래량
    netprps_qty: str    # 순매수수량
    buy_qty: str        # 매수수량
    sell_qty: str       # 매도수량


@dataclass(frozen=True)
class BrokerStockTrend:
    """증권사별종목매매동향 응답 (ka10078).

    Args:
        items: 일별 매매동향 리스트.
    """

    items: list[BrokerStockTrendItem]


# ---------------------------------------------------------------------------
# 4단계 — 국내주식 종목정보 응답 모델 (stkinfo)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class StockInfo:
    """주식기본정보 응답 (ka10001).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        open_pric: 시가 (원).
        high_pric: 고가 (원).
        low_pric: 저가 (원).
        upl_pric: 상한가 (원).
        lst_pric: 하한가 (원).
        mac: 시가총액 (억원).
        per: PER.
        pbr: PBR.
        eps: EPS (원).
        roe: ROE (%).
        flo_stk: 상장주식수 (천주).
        cap: 자본금 (억원).
        oyr_hgst: 연중최고 (원).
        oyr_lwst: 연중최저 (원).
    """

    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    cur_prc: str    # 현재가
    flu_rt: str     # 등락률
    trde_qty: str   # 거래량
    open_pric: str  # 시가
    high_pric: str  # 고가
    low_pric: str   # 저가
    upl_pric: str   # 상한가
    lst_pric: str   # 하한가
    mac: str        # 시가총액
    per: str        # PER
    pbr: str        # PBR
    eps: str        # EPS
    roe: str        # ROE
    flo_stk: str    # 상장주식수
    cap: str        # 자본금
    oyr_hgst: str   # 연중최고
    oyr_lwst: str   # 연중최저


@dataclass(frozen=True)
class BrokerEntry:
    """거래원 단일 항목 (ka10002).

    Args:
        name: 거래원명.
        code: 거래원 코드.
        qty: 거래량 (주).
    """

    name: str   # 거래원명
    code: str   # 거래원 코드
    qty: str    # 거래량


@dataclass(frozen=True)
class StockBrokers:
    """주식거래원 응답 (ka10002).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        sell_brokers: 매도거래원 1~5위 리스트.
        buy_brokers: 매수거래원 1~5위 리스트.
    """

    stk_cd: str                 # 종목코드
    stk_nm: str                 # 종목명
    cur_prc: str                # 현재가
    sell_brokers: list[BrokerEntry]  # 매도거래원 상위 5
    buy_brokers: list[BrokerEntry]   # 매수거래원 상위 5


@dataclass(frozen=True)
class ExecutionInfoItem:
    """체결정보 단일 항목 (ka10003).

    Args:
        tm: 시간 (HHMMSS).
        cur_prc: 현재가 (원).
        cntr_trde_qty: 체결거래량 (주).
        acc_trde_qty: 누적거래량 (주).
        cntr_str: 체결강도.
        stex_tp: 거래소구분.
    """

    tm: str             # 시간
    cur_prc: str        # 현재가
    cntr_trde_qty: str  # 체결거래량
    acc_trde_qty: str   # 누적거래량
    cntr_str: str       # 체결강도
    stex_tp: str        # 거래소구분


@dataclass(frozen=True)
class ExecutionInfo:
    """체결정보 응답 (ka10003).

    Args:
        items: 체결 리스트.
    """

    items: list[ExecutionInfoItem]


@dataclass(frozen=True)
class CreditTradingItem:
    """신용매매동향 단일 항목 (ka10013).

    Args:
        dt: 일자 (YYYYMMDD).
        cur_prc: 현재가 (원).
        trde_qty: 거래량 (주).
        new: 신규.
        rpya: 상환.
        remn: 잔고.
        remn_rt: 잔고율 (%).
    """

    dt: str         # 일자
    cur_prc: str    # 현재가
    trde_qty: str   # 거래량
    new: str        # 신규
    rpya: str       # 상환
    remn: str       # 잔고
    remn_rt: str    # 잔고율


@dataclass(frozen=True)
class CreditTradingTrend:
    """신용매매동향 응답 (ka10013).

    Args:
        items: 일별 신용매매동향 리스트.
    """

    items: list[CreditTradingItem]


@dataclass(frozen=True)
class DailyTradingDetailItem:
    """일별거래상세 단일 항목 (ka10015).

    Args:
        dt: 일자 (YYYYMMDD).
        close_pric: 종가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        trde_prica: 거래대금 (백만원).
        cntr_str: 체결강도.
        for_netprps: 외인순매수 (주).
        orgn_netprps: 기관순매수 (주).
        ind_netprps: 개인순매수 (주).
    """

    dt: str             # 일자
    close_pric: str     # 종가
    flu_rt: str         # 등락률
    trde_qty: str       # 거래량
    trde_prica: str     # 거래대금
    cntr_str: str       # 체결강도
    for_netprps: str    # 외인순매수
    orgn_netprps: str   # 기관순매수
    ind_netprps: str    # 개인순매수


@dataclass(frozen=True)
class DailyTradingDetail:
    """일별거래상세 응답 (ka10015).

    Args:
        items: 일별 거래상세 리스트.
    """

    items: list[DailyTradingDetailItem]


@dataclass(frozen=True)
class HighLowStockItem:
    """신고저가 단일 항목 (ka10016).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        high_pric: 고가 (원).
        low_pric: 저가 (원).
    """

    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    cur_prc: str    # 현재가
    flu_rt: str     # 등락률
    trde_qty: str   # 거래량
    high_pric: str  # 고가
    low_pric: str   # 저가


@dataclass(frozen=True)
class HighLowStocks:
    """신고저가 응답 (ka10016).

    Args:
        items: 신고저가 종목 리스트.
    """

    items: list[HighLowStockItem]


@dataclass(frozen=True)
class LimitStockItem:
    """상하한가 단일 항목 (ka10017).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        sel_bid: 매도호가 (원).
        buy_bid: 매수호가 (원).
        cnt: 연속횟수.
    """

    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    cur_prc: str    # 현재가
    flu_rt: str     # 등락률
    trde_qty: str   # 거래량
    sel_bid: str    # 매도호가
    buy_bid: str    # 매수호가
    cnt: str        # 횟수


@dataclass(frozen=True)
class LimitStocks:
    """상하한가 응답 (ka10017).

    Args:
        items: 상하한가 종목 리스트.
    """

    items: list[LimitStockItem]


@dataclass(frozen=True)
class NearHighLowItem:
    """고저가근접 단일 항목 (ka10018).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        tdy_high_pric: 당일고가 (원).
        tdy_low_pric: 당일저가 (원).
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    trde_qty: str       # 거래량
    tdy_high_pric: str  # 당일고가
    tdy_low_pric: str   # 당일저가


@dataclass(frozen=True)
class NearHighLow:
    """고저가근접 응답 (ka10018).

    Args:
        items: 고저가근접 종목 리스트.
    """

    items: list[NearHighLowItem]


@dataclass(frozen=True)
class PriceSurgeItem:
    """가격급등락 단일 항목 (ka10019).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        base_pric: 기준가 (원).
        jmp_rt: 급등률 (%).
        trde_qty: 거래량 (주).
    """

    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    cur_prc: str    # 현재가
    flu_rt: str     # 등락률
    base_pric: str  # 기준가
    jmp_rt: str     # 급등률
    trde_qty: str   # 거래량


@dataclass(frozen=True)
class PriceSurgeStocks:
    """가격급등락 응답 (ka10019).

    Args:
        items: 급등락 종목 리스트.
    """

    items: list[PriceSurgeItem]


@dataclass(frozen=True)
class VolumeUpdatedItem:
    """거래량갱신 단일 항목 (ka10024).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        prev_trde_qty: 이전거래량 (주).
        now_trde_qty: 현재거래량 (주).
    """

    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    cur_prc: str            # 현재가
    flu_rt: str             # 등락률
    prev_trde_qty: str      # 이전거래량
    now_trde_qty: str       # 현재거래량


@dataclass(frozen=True)
class VolumeUpdatedStocks:
    """거래량갱신 응답 (ka10024).

    Args:
        items: 거래량갱신 종목 리스트.
    """

    items: list[VolumeUpdatedItem]


@dataclass(frozen=True)
class SupplyConcentrationItem:
    """매물대집중 단일 항목 (ka10025).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        pric_strt: 가격대시작 (원).
        pric_end: 가격대끝 (원).
        prps_qty: 매물량 (주).
        prps_rt: 매물비 (%).
    """

    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    cur_prc: str    # 현재가
    flu_rt: str     # 등락률
    pric_strt: str  # 가격대시작
    pric_end: str   # 가격대끝
    prps_qty: str   # 매물량
    prps_rt: str    # 매물비


@dataclass(frozen=True)
class SupplyConcentration:
    """매물대집중 응답 (ka10025).

    Args:
        items: 매물대집중 종목 리스트.
    """

    items: list[SupplyConcentrationItem]


@dataclass(frozen=True)
class HighLowPERItem:
    """고저PER 단일 항목 (ka10026).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        per: PER 값.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        now_trde_qty: 현재거래량 (주).
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    per: str            # PER
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    now_trde_qty: str   # 현재거래량


@dataclass(frozen=True)
class HighLowPER:
    """고저PER 응답 (ka10026).

    Args:
        items: 고저PER 종목 리스트.
    """

    items: list[HighLowPERItem]


@dataclass(frozen=True)
class OpenPriceChangeItem:
    """시가대비등락률 단일 항목 (ka10028).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        open_pric: 시가 (원).
        open_pric_pre: 시가대비 (%).
        now_trde_qty: 현재거래량 (주).
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    open_pric: str      # 시가
    open_pric_pre: str  # 시가대비
    now_trde_qty: str   # 현재거래량


@dataclass(frozen=True)
class OpenPriceChange:
    """시가대비등락률 응답 (ka10028).

    Args:
        items: 시가대비등락률 종목 리스트.
    """

    items: list[OpenPriceChangeItem]


@dataclass(frozen=True)
class BrokerSupplyItem:
    """거래원매물대분석 단일 항목 (ka10043).

    Args:
        dt: 일자 (YYYYMMDD).
        close_pric: 종가 (원).
        sel_qty: 매도량 (주).
        buy_qty: 매수량 (주).
        netprps_qty: 순매수수량 (주).
        trde_wght: 거래비중 (%).
    """

    dt: str             # 일자
    close_pric: str     # 종가
    sel_qty: str        # 매도량
    buy_qty: str        # 매수량
    netprps_qty: str    # 순매수수량
    trde_wght: str      # 거래비중


@dataclass(frozen=True)
class BrokerSupplyAnalysis:
    """거래원매물대분석 응답 (ka10043).

    Args:
        items: 일별 분석 리스트.
    """

    items: list[BrokerSupplyItem]


@dataclass(frozen=True)
class BrokerInstantVolumeItem:
    """거래원순간거래량 단일 항목 (ka10052).

    Args:
        tm: 시간 (HHMMSS).
        stk_cd: 종목코드.
        stk_nm: 종목명.
        trde_ori_nm: 거래원명.
        tp: 구분 (매도/매수).
        mont_trde_qty: 순간거래량 (주).
        acc_netprps: 누적순매수 (주).
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
    """

    tm: str             # 시간
    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    trde_ori_nm: str    # 거래원명
    tp: str             # 구분
    mont_trde_qty: str  # 순간거래량
    acc_netprps: str    # 누적순매수
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률


@dataclass(frozen=True)
class BrokerInstantVolume:
    """거래원순간거래량 응답 (ka10052).

    Args:
        items: 순간거래량 리스트.
    """

    items: list[BrokerInstantVolumeItem]


@dataclass(frozen=True)
class VIStockItem:
    """변동성완화장치 발동종목 단일 항목 (ka10054).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        acc_trde_qty: 누적거래량 (주).
        motn_pric: 발동가격 (원).
        viaplc_tp: VI적용구분 (동적/정적/동적+정적).
        vimotn_cnt: VI발동횟수.
        stex_tp: 거래소구분.
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    acc_trde_qty: str   # 누적거래량
    motn_pric: str      # 발동가격
    viaplc_tp: str      # VI적용구분
    vimotn_cnt: str     # VI발동횟수
    stex_tp: str        # 거래소구분


@dataclass(frozen=True)
class VIStocks:
    """변동성완화장치 발동종목 응답 (ka10054).

    Args:
        items: VI 발동종목 리스트.
    """

    items: list[VIStockItem]


@dataclass(frozen=True)
class TodayPrevExecutionQtyItem:
    """당일전일체결량 단일 항목 (ka10055).

    Args:
        cntr_tm: 체결시간 (HHMMSS).
        cntr_pric: 체결가 (원).
        flu_rt: 등락률 (%).
        cntr_qty: 체결량 (주).
        acc_trde_qty: 누적거래량 (주).
        acc_trde_prica: 누적거래대금 (백만원).
    """

    cntr_tm: str            # 체결시간
    cntr_pric: str          # 체결가
    flu_rt: str             # 등락률
    cntr_qty: str           # 체결량
    acc_trde_qty: str       # 누적거래량
    acc_trde_prica: str     # 누적거래대금


@dataclass(frozen=True)
class TodayPrevExecutionQty:
    """당일전일체결량 응답 (ka10055).

    Args:
        items: 체결량 리스트.
    """

    items: list[TodayPrevExecutionQtyItem]


@dataclass(frozen=True)
class InvestorDailyStockItem:
    """투자자별일별매매종목 단일 항목 (ka10058).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        netslmt_qty: 순매도수량 (주).
        netslmt_amt: 순매도금액 (백만원).
        cur_prc: 현재가 (원).
        pre_rt: 대비율 (%).
    """

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    netslmt_qty: str    # 순매도수량
    netslmt_amt: str    # 순매도금액
    cur_prc: str        # 현재가
    pre_rt: str         # 대비율


@dataclass(frozen=True)
class InvestorDailyStocks:
    """투자자별일별매매종목 응답 (ka10058).

    Args:
        items: 종목별 리스트.
    """

    items: list[InvestorDailyStockItem]


@dataclass(frozen=True)
class StockInvestorItem:
    """종목별투자자기관별 단일 항목 (ka10059).

    Args:
        dt: 일자 (YYYYMMDD).
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        acc_trde_qty: 누적거래량 (주).
        ind_invsr: 개인투자자.
        frgnr_invsr: 외국인투자자.
        orgn: 기관계.
        fnnc_invt: 금융투자.
        bank: 은행.
        penfnd_etc: 연기금등.
    """

    dt: str             # 일자
    cur_prc: str        # 현재가
    flu_rt: str         # 등락률
    acc_trde_qty: str   # 누적거래량
    ind_invsr: str      # 개인투자자
    frgnr_invsr: str    # 외국인투자자
    orgn: str           # 기관계
    fnnc_invt: str      # 금융투자
    bank: str           # 은행
    penfnd_etc: str     # 연기금등


@dataclass(frozen=True)
class StockInvestorByDay:
    """종목별투자자기관별 응답 (ka10059).

    Args:
        items: 일별 투자자 리스트.
    """

    items: list[StockInvestorItem]


@dataclass(frozen=True)
class StockInvestorTotal:
    """종목별투자자기관별합계 응답 (ka10061).

    Args:
        ind_invsr: 개인투자자.
        frgnr_invsr: 외국인투자자.
        orgn: 기관계.
        fnnc_invt: 금융투자.
        bank: 은행.
        penfnd_etc: 연기금등.
        samo_fund: 사모펀드.
        natn: 국가.
        etc_corp: 기타법인.
    """

    ind_invsr: str      # 개인투자자
    frgnr_invsr: str    # 외국인투자자
    orgn: str           # 기관계
    fnnc_invt: str      # 금융투자
    bank: str           # 은행
    penfnd_etc: str     # 연기금등
    samo_fund: str      # 사모펀드
    natn: str           # 국가
    etc_corp: str       # 기타법인


@dataclass(frozen=True)
class TodayPrevExecutionItem:
    """당일전일체결 단일 항목 (ka10084).

    Args:
        tm: 시간 (HHMMSS).
        cur_prc: 현재가 (원).
        cntr_trde_qty: 체결거래량 (주).
        acc_trde_qty: 누적거래량 (주).
        cntr_str: 체결강도.
        stex_tp: 거래소구분.
    """

    tm: str             # 시간
    cur_prc: str        # 현재가
    cntr_trde_qty: str  # 체결거래량
    acc_trde_qty: str   # 누적거래량
    cntr_str: str       # 체결강도
    stex_tp: str        # 거래소구분


@dataclass(frozen=True)
class TodayPrevExecution:
    """당일전일체결 응답 (ka10084).

    Args:
        items: 체결 리스트.
    """

    items: list[TodayPrevExecutionItem]


@dataclass(frozen=True)
class WatchlistStockItem:
    """관심종목정보 단일 항목 (ka10095).

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        cur_prc: 현재가 (원).
        flu_rt: 등락률 (%).
        trde_qty: 거래량 (주).
        trde_prica: 거래대금 (백만원).
        open_pric: 시가 (원).
        high_pric: 고가 (원).
        low_pric: 저가 (원).
        upl_pric: 상한가 (원).
        lst_pric: 하한가 (원).
    """

    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    cur_prc: str    # 현재가
    flu_rt: str     # 등락률
    trde_qty: str   # 거래량
    trde_prica: str # 거래대금
    open_pric: str  # 시가
    high_pric: str  # 고가
    low_pric: str   # 저가
    upl_pric: str   # 상한가
    lst_pric: str   # 하한가


@dataclass(frozen=True)
class WatchlistInfo:
    """관심종목정보 응답 (ka10095).

    Args:
        items: 관심종목 리스트.
    """

    items: list[WatchlistStockItem]


@dataclass(frozen=True)
class StockListItem:
    """종목정보 리스트 단일 항목 (ka10099).

    Args:
        code: 종목코드 (단축코드).
        name: 종목명.
        list_count: 상장주식수.
        reg_day: 상장일 (YYYYMMDD).
        last_price: 전일종가 (원).
        state: 종목상태.
        market_name: 시장명.
        up_name: 업종명.
        nxt_enable: NXT가능여부 (Y/N).
    """

    code: str           # 종목코드
    name: str           # 종목명
    list_count: str     # 상장주식수
    reg_day: str        # 상장일
    last_price: str     # 전일종가
    state: str          # 종목상태
    market_name: str    # 시장명
    up_name: str        # 업종명
    nxt_enable: str     # NXT가능여부


@dataclass(frozen=True)
class StockList:
    """종목정보 리스트 응답 (ka10099).

    Args:
        items: 종목 리스트.
    """

    items: list[StockListItem]


@dataclass(frozen=True)
class StockDetail:
    """종목정보 조회 응답 (ka10100).

    Args:
        code: 종목코드 (단축코드).
        name: 종목명.
        list_count: 상장주식수.
        reg_day: 상장일 (YYYYMMDD).
        last_price: 전일종가 (원).
        state: 종목상태.
        market_code: 시장구분코드.
        market_name: 시장명.
        up_name: 업종명.
        up_size_name: 회사크기분류.
        nxt_enable: NXT가능여부 (Y/N).
    """

    code: str           # 종목코드
    name: str           # 종목명
    list_count: str     # 상장주식수
    reg_day: str        # 상장일
    last_price: str     # 전일종가
    state: str          # 종목상태
    market_code: str    # 시장구분코드
    market_name: str    # 시장명
    up_name: str        # 업종명
    up_size_name: str   # 회사크기분류
    nxt_enable: str     # NXT가능여부


@dataclass(frozen=True)
class SectorItem:
    """업종코드 단일 항목 (ka10101).

    Args:
        market_code: 시장구분코드.
        code: 업종코드.
        name: 업종명.
        group: 그룹.
    """

    market_code: str    # 시장구분코드
    code: str           # 업종코드
    name: str           # 업종명
    group: str          # 그룹


@dataclass(frozen=True)
class SectorList:
    """업종코드 리스트 응답 (ka10101).

    Args:
        items: 업종코드 리스트.
    """

    items: list[SectorItem]


@dataclass(frozen=True)
class BrokerItem:
    """회원사 단일 항목 (ka10102).

    Args:
        code: 회원사 코드.
        name: 회원사명.
        gb: 구분.
    """

    code: str   # 회원사 코드
    name: str   # 회원사명
    gb: str     # 구분


@dataclass(frozen=True)
class BrokerList:
    """회원사 리스트 응답 (ka10102).

    Args:
        items: 회원사 리스트.
    """

    items: list[BrokerItem]


# ---------------------------------------------------------------------------
# 5단계 — 순위정보 공통 Literal 타입
# ---------------------------------------------------------------------------

type RkinfoStexType = Literal["krx", "nxt", "all"]
"""순위정보 거래소구분.

- ``"krx"``: KRX — API ``"1"``
- ``"nxt"``: NXT — API ``"2"``
- ``"all"``: 통합 — API ``"3"``
"""

type RkinfoBidTradeType = Literal["buy", "sell"]
"""호가잔량급증 매매구분 (ka10021).

- ``"buy"``: 매수잔량 — API ``"1"``
- ``"sell"``: 매도잔량 — API ``"2"``
"""

type RkinfoMarketType = Literal["all", "kospi", "kosdaq"]
"""순위정보 시장구분.

- ``"all"``: 전체 — API ``"000"``
- ``"kospi"``: 코스피 — API ``"001"``
- ``"kosdaq"``: 코스닥 — API ``"101"``
"""

type RkinfoBidSortType = Literal["net_buy_qty", "net_sell_qty", "buy_ratio", "sell_ratio"]
"""호가잔량상위 정렬구분 (ka10020).

- ``"net_buy_qty"``: 순매수잔량순 — API ``"1"``
- ``"net_sell_qty"``: 순매도잔량순 — API ``"2"``
- ``"buy_ratio"``: 매수비율순 — API ``"3"``
- ``"sell_ratio"``: 매도비율순 — API ``"4"``
"""

type RkinfoSurgeSort2Type = Literal["surge_qty", "surge_ratio"]
"""급증 정렬구분 (ka10021/ka10022).

- ``"surge_qty"``: 급증량 — API ``"1"``
- ``"surge_ratio"``: 급증률 — API ``"2"``
"""

type RkinfoPriceChangeSortType = Literal["rise_ratio", "rise_gap", "fall_ratio", "fall_gap", "flat"]
"""전일대비등락률상위 정렬구분 (ka10027).

- ``"rise_ratio"``: 상승률 — API ``"1"``
- ``"rise_gap"``: 상승폭 — API ``"2"``
- ``"fall_ratio"``: 하락률 — API ``"3"``
- ``"fall_gap"``: 하락폭 — API ``"4"``
- ``"flat"``: 보합 — API ``"5"``
"""

type RkinfoBaseDateType = Literal["today", "prev"]
"""기준일구분.

- ``"today"``: 당일기준 — API ``"0"``
- ``"prev"``: 전일기준 — API ``"1"``
"""

type RkinfoSortCndType = Literal["qty", "amount"]
"""동일순매매 정렬조건 (ka10062).

- ``"qty"``: 수량 — API ``"1"``
- ``"amount"``: 금액 — API ``"2"``
"""

type RkinfoOrgType = Literal[
    "foreign", "foreign_corp", "financial_inv", "trust",
    "other_finance", "bank", "insurance", "pension",
    "gov", "other_corp", "institution",
]
"""장중투자자별 기관구분 (ka10065).

- ``"foreign"``: 외국인 — API ``"9000"``
- ``"foreign_corp"``: 외국계 — API ``"9100"``
- ``"financial_inv"``: 금융투자 — API ``"1000"``
- ``"trust"``: 투신 — API ``"3000"``
- ``"other_finance"``: 기타금융 — API ``"5000"``
- ``"bank"``: 은행 — API ``"4000"``
- ``"insurance"``: 보험 — API ``"2000"``
- ``"pension"``: 연기금 — API ``"6000"``
- ``"gov"``: 국가 — API ``"7000"``
- ``"other_corp"``: 기타법인 — API ``"7100"``
- ``"institution"``: 기관계 — API ``"9999"``
"""


# ---------------------------------------------------------------------------
# 5단계 — 순위정보 응답 모델
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BidQtyUpperItem:
    """호가잔량상위 단일 항목 (ka10020)."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    trde_qty: str       # 거래량
    tot_sel_req: str    # 총매도잔량
    tot_buy_req: str    # 총매수잔량
    netprps_req: str    # 순매수잔량
    buy_rt: str         # 매수비율


@dataclass(frozen=True)
class BidQtyUpper:
    """호가잔량상위 응답 (ka10020).

    Args:
        items: 호가잔량상위 종목 리스트.
    """

    items: list[BidQtyUpperItem]


@dataclass(frozen=True)
class BidQtySurgeItem:
    """호가잔량급증 단일 항목 (ka10021)."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    base_rt: str        # 기준률 (응답필드명 int)
    now: str            # 현재
    sdnin_qty: str      # 급증수량
    sdnin_rt: str       # 급증률
    tot_buy_qty: str    # 총매수량


@dataclass(frozen=True)
class BidQtySurge:
    """호가잔량급증 응답 (ka10021).

    Args:
        items: 호가잔량급증 종목 리스트.
    """

    items: list[BidQtySurgeItem]


@dataclass(frozen=True)
class QtyRatioSurgeItem:
    """잔량율급증 단일 항목 (ka10022)."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    base_rt: str        # 기준률 (응답필드명 int)
    now_rt: str         # 현재비율
    sdnin_rt: str       # 급증률
    tot_sel_req: str    # 총매도잔량
    tot_buy_req: str    # 총매수잔량


@dataclass(frozen=True)
class QtyRatioSurge:
    """잔량율급증 응답 (ka10022).

    Args:
        items: 잔량율급증 종목 리스트.
    """

    items: list[QtyRatioSurgeItem]


@dataclass(frozen=True)
class TradeQtySurgeItem:
    """거래량급증 단일 항목 (ka10023)."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락률
    prev_trde_qty: str  # 이전거래량
    now_trde_qty: str   # 현재거래량
    sdnin_qty: str      # 급증량
    sdnin_rt: str       # 급증률


@dataclass(frozen=True)
class TradeQtySurge:
    """거래량급증 응답 (ka10023).

    Args:
        items: 거래량급증 종목 리스트.
    """

    items: list[TradeQtySurgeItem]


@dataclass(frozen=True)
class PriceChangeUpperItem:
    """전일대비등락률상위 단일 항목 (ka10027)."""

    stk_cls: str        # 종목분류
    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락률
    sel_req: str        # 매도잔량
    buy_req: str        # 매수잔량
    now_trde_qty: str   # 현재거래량
    cntr_str: str       # 체결강도
    cnt: str            # 횟수


@dataclass(frozen=True)
class PriceChangeUpper:
    """전일대비등락률상위 응답 (ka10027).

    Args:
        items: 등락률상위 종목 리스트.
    """

    items: list[PriceChangeUpperItem]


@dataclass(frozen=True)
class ExpectedTradeUpperItem:
    """예상체결등락률상위 단일 항목 (ka10029)."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    exp_cntr_pric: str  # 예상체결가
    base_pric: str      # 기준가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락률
    exp_cntr_qty: str   # 예상체결량
    sel_req: str        # 매도잔량
    sel_bid: str        # 매도호가
    buy_bid: str        # 매수호가
    buy_req: str        # 매수잔량


@dataclass(frozen=True)
class ExpectedTradeUpper:
    """예상체결등락률상위 응답 (ka10029).

    Args:
        items: 예상체결등락률상위 종목 리스트.
    """

    items: list[ExpectedTradeUpperItem]


@dataclass(frozen=True)
class DailyTradeQtyUpperItem:
    """당일거래량상위 단일 항목 (ka10030)."""

    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    cur_prc: str            # 현재가
    pred_pre_sig: str       # 전일대비기호
    pred_pre: str           # 전일대비
    flu_rt: str             # 등락률
    trde_qty: str           # 거래량
    pred_rt: str            # 전일비
    trde_tern_rt: str       # 거래회전율
    trde_amt: str           # 거래금액
    opmr_trde_qty: str      # 장중거래량
    opmr_pred_rt: str       # 장중전일비
    opmr_trde_rt: str       # 장중거래회전율
    opmr_trde_amt: str      # 장중거래금액
    af_mkrt_trde_qty: str   # 장후거래량
    af_mkrt_pred_rt: str    # 장후전일비
    af_mkrt_trde_rt: str    # 장후거래회전율
    af_mkrt_trde_amt: str   # 장후거래금액
    bf_mkrt_trde_qty: str   # 장전거래량
    bf_mkrt_pred_rt: str    # 장전전일비
    bf_mkrt_trde_rt: str    # 장전거래회전율
    bf_mkrt_trde_amt: str   # 장전거래금액


@dataclass(frozen=True)
class DailyTradeQtyUpper:
    """당일거래량상위 응답 (ka10030).

    Args:
        items: 당일거래량상위 종목 리스트.
    """

    items: list[DailyTradeQtyUpperItem]


@dataclass(frozen=True)
class PrevTradeQtyUpperItem:
    """전일거래량상위 단일 항목 (ka10031)."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    trde_qty: str       # 거래량


@dataclass(frozen=True)
class PrevTradeQtyUpper:
    """전일거래량상위 응답 (ka10031).

    Args:
        items: 전일거래량상위 종목 리스트.
    """

    items: list[PrevTradeQtyUpperItem]


@dataclass(frozen=True)
class TradeAmtUpperItem:
    """거래대금상위 단일 항목 (ka10032)."""

    stk_cd: str         # 종목코드
    now_rank: str       # 현재순위
    pred_rank: str      # 전일순위
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락률
    sel_bid: str        # 매도호가
    buy_bid: str        # 매수호가
    now_trde_qty: str   # 현재거래량
    pred_trde_qty: str  # 전일거래량
    trde_prica: str     # 거래대금


@dataclass(frozen=True)
class TradeAmtUpper:
    """거래대금상위 응답 (ka10032).

    Args:
        items: 거래대금상위 종목 리스트.
    """

    items: list[TradeAmtUpperItem]


@dataclass(frozen=True)
class CreditRatioUpperItem:
    """신용비율상위 단일 항목 (ka10033)."""

    stk_infr: str       # 종목정보
    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락률
    crd_rt: str         # 신용비율
    sel_req: str        # 매도잔량
    buy_req: str        # 매수잔량
    now_trde_qty: str   # 현재거래량


@dataclass(frozen=True)
class CreditRatioUpper:
    """신용비율상위 응답 (ka10033).

    Args:
        items: 신용비율상위 종목 리스트.
    """

    items: list[CreditRatioUpperItem]


@dataclass(frozen=True)
class ForeignPeriodTradeUpperItem:
    """외인기간별매매상위 단일 항목 (ka10034)."""

    rank: str               # 순위
    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    cur_prc: str            # 현재가
    pred_pre_sig: str       # 전일대비기호
    pred_pre: str           # 전일대비
    sel_bid: str            # 매도호가
    buy_bid: str            # 매수호가
    trde_qty: str           # 거래량
    netprps_qty: str        # 순매수량
    gain_pos_stkcnt: str    # 취득가능주식수


@dataclass(frozen=True)
class ForeignPeriodTradeUpper:
    """외인기간별매매상위 응답 (ka10034).

    Args:
        items: 외인기간별매매상위 종목 리스트.
    """

    items: list[ForeignPeriodTradeUpperItem]


@dataclass(frozen=True)
class ForeignConsecTradeUpperItem:
    """외인연속순매매상위 단일 항목 (ka10035)."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    dm1: str            # D-1
    dm2: str            # D-2
    dm3: str            # D-3
    tot: str            # 합계
    limit_exh_rt: str   # 한도소진율
    pred_pre_1: str     # 전일대비1
    pred_pre_2: str     # 전일대비2
    pred_pre_3: str     # 전일대비3


@dataclass(frozen=True)
class ForeignConsecTradeUpper:
    """외인연속순매매상위 응답 (ka10035).

    Args:
        items: 외인연속순매매상위 종목 리스트.
    """

    items: list[ForeignConsecTradeUpperItem]


@dataclass(frozen=True)
class ForeignLimitExhaustUpperItem:
    """외인한도소진율증가상위 단일 항목 (ka10036)."""

    rank: str               # 순위
    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    cur_prc: str            # 현재가
    pred_pre_sig: str       # 전일대비기호
    pred_pre: str           # 전일대비
    trde_qty: str           # 거래량
    poss_stkcnt: str        # 보유주식수
    gain_pos_stkcnt: str    # 취득가능주식수
    base_limit_exh_rt: str  # 기준한도소진율
    limit_exh_rt: str       # 한도소진율
    exh_rt_incrs: str       # 소진율증가


@dataclass(frozen=True)
class ForeignLimitExhaustUpper:
    """외인한도소진율증가상위 응답 (ka10036).

    Args:
        items: 외인한도소진율증가상위 종목 리스트.
    """

    items: list[ForeignLimitExhaustUpperItem]


@dataclass(frozen=True)
class ForeignBrokerTradeUpperItem:
    """외국계창구매매상위 단일 항목 (ka10037)."""

    rank: str               # 순위
    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    cur_prc: str            # 현재가
    pred_pre_sig: str       # 전일대비기호
    pred_pre: str           # 전일대비
    flu_rt: str             # 등락율
    sel_trde_qty: str       # 매도거래량
    buy_trde_qty: str       # 매수거래량
    netprps_trde_qty: str   # 순매수거래량
    netprps_prica: str      # 순매수대금
    trde_qty: str           # 거래량
    trde_prica: str         # 거래대금


@dataclass(frozen=True)
class ForeignBrokerTradeUpper:
    """외국계창구매매상위 응답 (ka10037).

    Args:
        items: 외국계창구매매상위 종목 리스트.
    """

    items: list[ForeignBrokerTradeUpperItem]


@dataclass(frozen=True)
class StockBrokerRankItem:
    """종목별증권사순위 단일 항목 (ka10038)."""

    rank: str               # 순위
    mmcm_nm: str            # 회원사명
    buy_qty: str            # 매수수량
    sell_qty: str           # 매도수량
    acc_netprps_qty: str    # 누적순매수수량


@dataclass(frozen=True)
class StockBrokerRank:
    """종목별증권사순위 응답 (ka10038).

    Args:
        rank_1: 순위1 (순매수/순매도 1위 수량).
        rank_2: 순위2.
        rank_3: 순위3.
        prid_trde_qty: 기간중거래량.
        items: 증권사순위 리스트.
    """

    rank_1: str
    rank_2: str
    rank_3: str
    prid_trde_qty: str
    items: list[StockBrokerRankItem]


@dataclass(frozen=True)
class BrokerTradeUpperItem:
    """증권사별매매상위 단일 항목 (ka10039)."""

    rank: str               # 순위
    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    prid_stkpc_flu: str     # 기간중주가등락
    flu_rt: str             # 등락율
    prid_trde_qty: str      # 기간중거래량
    netprps: str            # 순매수
    buy_trde_qty: str       # 매수거래량
    sel_trde_qty: str       # 매도거래량
    netprps_amt: str        # 순매수금액
    buy_amt: str            # 매수금액
    sell_amt: str           # 매도금액


@dataclass(frozen=True)
class BrokerTradeUpper:
    """증권사별매매상위 응답 (ka10039).

    Args:
        items: 증권사별매매상위 종목 리스트.
    """

    items: list[BrokerTradeUpperItem]


@dataclass(frozen=True)
class DailyMainBrokerEntry:
    """당일주요거래원 매도/매수 이탈 단일 항목 (ka10040)."""

    sel_scesn_tm: str           # 매도이탈시간
    sell_qty: str               # 매도수량
    sel_upper_scesn_ori: str    # 매도상위이탈원
    buy_scesn_tm: str           # 매수이탈시간
    buy_qty: str                # 매수수량
    buy_upper_scesn_ori: str    # 매수상위이탈원
    qry_dt: str                 # 조회일자
    qry_tm: str                 # 조회시간


@dataclass(frozen=True)
class DailyMainBroker:
    """당일주요거래원 응답 (ka10040).

    매도/매수 거래원 상위 5개를 번호별 필드로 제공하고,
    당일주요거래원 이탈 리스트를 별도로 포함합니다.

    Args:
        sel_trde_ori_1 ~ 5: 매도거래원명 1~5위.
        sel_trde_ori_qty_1 ~ 5: 매도거래원수량 1~5위.
        buy_trde_ori_1 ~ 5: 매수거래원명 1~5위.
        buy_trde_ori_qty_1 ~ 5: 매수거래원수량 1~5위.
        frgn_sel_prsm_sum: 외국계매도추정합.
        frgn_buy_prsm_sum: 외국계매수추정합.
        items: 당일주요거래원 이탈 리스트.
    """

    sel_trde_ori_1: str
    sel_trde_ori_qty_1: str
    sel_trde_ori_irds_1: str
    buy_trde_ori_1: str
    buy_trde_ori_qty_1: str
    buy_trde_ori_irds_1: str
    sel_trde_ori_2: str
    sel_trde_ori_qty_2: str
    sel_trde_ori_irds_2: str
    buy_trde_ori_2: str
    buy_trde_ori_qty_2: str
    buy_trde_ori_irds_2: str
    sel_trde_ori_3: str
    sel_trde_ori_qty_3: str
    sel_trde_ori_irds_3: str
    buy_trde_ori_3: str
    buy_trde_ori_qty_3: str
    buy_trde_ori_irds_3: str
    sel_trde_ori_4: str
    sel_trde_ori_qty_4: str
    sel_trde_ori_irds_4: str
    buy_trde_ori_4: str
    buy_trde_ori_qty_4: str
    buy_trde_ori_irds_4: str
    sel_trde_ori_5: str
    sel_trde_ori_qty_5: str
    sel_trde_ori_irds_5: str
    buy_trde_ori_5: str
    buy_trde_ori_qty_5: str
    buy_trde_ori_irds_5: str
    frgn_sel_prsm_sum: str
    frgn_sel_prsm_sum_chang: str
    frgn_buy_prsm_sum: str
    frgn_buy_prsm_sum_chang: str
    items: list[DailyMainBrokerEntry]


@dataclass(frozen=True)
class NetBuyBrokerRankItem:
    """순매수거래원순위 단일 항목 (ka10042)."""

    rank: str       # 순위
    mmcm_cd: str    # 회원사코드
    mmcm_nm: str    # 회원사명


@dataclass(frozen=True)
class NetBuyBrokerRank:
    """순매수거래원순위 응답 (ka10042).

    Args:
        items: 순매수거래원순위 리스트.
    """

    items: list[NetBuyBrokerRankItem]


@dataclass(frozen=True)
class DailyTopExitItem:
    """당일상위이탈원 단일 항목 (ka10053)."""

    sel_scesn_tm: str           # 매도이탈시간
    sell_qty: str               # 매도수량
    sel_upper_scesn_ori: str    # 매도상위이탈원
    buy_scesn_tm: str           # 매수이탈시간
    buy_qty: str                # 매수수량
    buy_upper_scesn_ori: str    # 매수상위이탈원
    qry_dt: str                 # 조회일자
    qry_tm: str                 # 조회시간


@dataclass(frozen=True)
class DailyTopExit:
    """당일상위이탈원 응답 (ka10053).

    Args:
        items: 당일상위이탈원 리스트.
    """

    items: list[DailyTopExitItem]


@dataclass(frozen=True)
class SameNetTradeRankItem:
    """동일순매매순위 단일 항목 (ka10062)."""

    stk_cd: str                 # 종목코드
    rank: str                   # 순위
    stk_nm: str                 # 종목명
    cur_prc: str                # 현재가
    pre_sig: str                # 대비기호
    pred_pre: str               # 전일대비
    flu_rt: str                 # 등락율
    acc_trde_qty: str           # 누적거래량
    orgn_nettrde_qty: str       # 기관순매매수량
    orgn_nettrde_amt: str       # 기관순매매금액
    orgn_nettrde_avg_pric: str  # 기관순매매평균가
    for_nettrde_qty: str        # 외인순매매수량
    for_nettrde_amt: str        # 외인순매매금액
    for_nettrde_avg_pric: str   # 외인순매매평균가
    nettrde_qty: str            # 순매매수량
    nettrde_amt: str            # 순매매금액


@dataclass(frozen=True)
class SameNetTradeRank:
    """동일순매매순위 응답 (ka10062).

    Args:
        items: 동일순매매순위 종목 리스트.
    """

    items: list[SameNetTradeRankItem]


@dataclass(frozen=True)
class InvestorTradeUpperItem:
    """장중투자자별매매상위 단일 항목 (ka10065)."""

    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    sel_qty: str    # 매도량
    buy_qty: str    # 매수량
    netslmt: str    # 순매도


@dataclass(frozen=True)
class InvestorTradeUpper:
    """장중투자자별매매상위 응답 (ka10065).

    Args:
        items: 장중투자자별매매상위 종목 리스트.
    """

    items: list[InvestorTradeUpperItem]


@dataclass(frozen=True)
class AfterHoursRankItem:
    """시간외단일가등락율순위 단일 항목 (ka10098)."""

    rank: str                   # 순위
    stk_cd: str                 # 종목코드
    stk_nm: str                 # 종목명
    cur_prc: str                # 현재가
    pred_pre_sig: str           # 전일대비기호
    pred_pre: str               # 전일대비
    flu_rt: str                 # 등락률
    sel_tot_req: str            # 매도총잔량
    buy_tot_req: str            # 매수총잔량
    acc_trde_qty: str           # 누적거래량
    acc_trde_prica: str         # 누적거래대금
    tdy_close_pric: str         # 당일종가
    tdy_close_pric_flu_rt: str  # 당일종가등락률


@dataclass(frozen=True)
class AfterHoursRank:
    """시간외단일가등락율순위 응답 (ka10098).

    Args:
        items: 시간외단일가등락율순위 종목 리스트.
    """

    items: list[AfterHoursRankItem]


@dataclass(frozen=True)
class ForeignInstitutionTradeUpperItem:
    """외국인기관매매상위 단일 항목 (ka90009)."""

    for_netslmt_stk_cd: str     # 외인순매도종목코드
    for_netslmt_stk_nm: str     # 외인순매도종목명
    for_netslmt_amt: str        # 외인순매도금액
    for_netslmt_qty: str        # 외인순매도수량
    for_netprps_stk_cd: str     # 외인순매수종목코드
    for_netprps_stk_nm: str     # 외인순매수종목명
    for_netprps_amt: str        # 외인순매수금액
    for_netprps_qty: str        # 외인순매수수량
    orgn_netslmt_stk_cd: str    # 기관순매도종목코드
    orgn_netslmt_stk_nm: str    # 기관순매도종목명
    orgn_netslmt_amt: str       # 기관순매도금액
    orgn_netslmt_qty: str       # 기관순매도수량
    orgn_netprps_stk_cd: str    # 기관순매수종목코드
    orgn_netprps_stk_nm: str    # 기관순매수종목명
    orgn_netprps_amt: str       # 기관순매수금액
    orgn_netprps_qty: str       # 기관순매수수량


@dataclass(frozen=True)
class ForeignInstitutionTradeUpper:
    """외국인기관매매상위 응답 (ka90009).

    Args:
        items: 외국인기관매매상위 리스트.
    """

    items: list[ForeignInstitutionTradeUpperItem]


# ---------------------------------------------------------------------------
# 6단계 — 차트 공통 Literal 타입
# ---------------------------------------------------------------------------

type ChartTickScope = Literal["1", "3", "5", "10", "30"]
"""주식/업종 틱 범위.

- ``"1"``: 1틱
- ``"3"``: 3틱
- ``"5"``: 5틱
- ``"10"``: 10틱
- ``"30"``: 30틱
"""

type ChartMinScope = Literal["1", "3", "5", "10", "15", "30", "45", "60"]
"""주식 분봉 범위.

- ``"1"``: 1분
- ``"3"``: 3분
- ``"5"``: 5분
- ``"10"``: 10분
- ``"15"``: 15분
- ``"30"``: 30분
- ``"45"``: 45분
- ``"60"``: 60분
"""

type ChartAdjustedPrice = Literal["adjusted", "raw"]
"""수정주가구분.

- ``"adjusted"``: 수정주가 반영 — API ``"1"``
- ``"raw"``: 미반영 — API ``"0"``
"""

type ChartAmtQtyType = Literal["amount", "qty"]
"""금액수량구분 (투자자 차트).

- ``"amount"``: 금액 — API ``"1"``
- ``"qty"``: 수량 — API ``"2"``
"""

type ChartTradeType = Literal["net_buy", "buy", "sell"]
"""매매구분 (투자자 차트).

- ``"net_buy"``: 순매수 — API ``"0"``
- ``"buy"``: 매수 — API ``"1"``
- ``"sell"``: 매도 — API ``"2"``
"""

type ChartUnitType = Literal["thousand", "single"]
"""단위구분 (종목별투자자기관별차트).

- ``"thousand"``: 천주 — API ``"1000"``
- ``"single"``: 단주 — API ``"1"``
"""

type ChartSectorMarket = Literal["kospi", "kosdaq", "kospi200"]
"""업종차트 시장구분.

- ``"kospi"``: 코스피 — API ``"0"``
- ``"kosdaq"``: 코스닥 — API ``"1"``
- ``"kospi200"``: 코스피200 — API ``"2"``
"""


# ---------------------------------------------------------------------------
# 6단계 — 차트 응답 모델
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class StockCandleItem:
    """주식 캔들 단일 항목 (틱·분봉 공통)."""

    cur_prc: str        # 현재가 (종가)
    trde_qty: str       # 거래량
    cntr_tm: str        # 체결시간 (YYYYMMDDHHMMSS)
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    pred_pre: str       # 전일대비
    pred_pre_sig: str   # 전일대비기호 (1:상한가 2:상승 3:보합 4:하한가 5:하락)


@dataclass(frozen=True)
class StockTickChart:
    """주식틱차트조회 응답 (ka10079).

    Args:
        stk_cd: 종목코드.
        last_tic_cnt: 마지막틱갯수.
        items: 틱 캔들 리스트.
    """

    stk_cd: str
    last_tic_cnt: str
    items: list[StockCandleItem]


@dataclass(frozen=True)
class StockMinChartItem:
    """주식분봉차트 단일 항목 (ka10080)."""

    cur_prc: str        # 현재가 (종가)
    trde_qty: str       # 거래량
    cntr_tm: str        # 체결시간
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    pred_pre: str       # 전일대비
    pred_pre_sig: str   # 전일대비기호
    acc_trde_qty: str   # 누적거래량


@dataclass(frozen=True)
class StockMinChart:
    """주식분봉차트조회 응답 (ka10080).

    Args:
        stk_cd: 종목코드.
        items: 분봉 캔들 리스트.
    """

    stk_cd: str
    items: list[StockMinChartItem]


@dataclass(frozen=True)
class StockDayChartItem:
    """주식일봉차트 단일 항목 (ka10081)."""

    cur_prc: str        # 현재가
    trde_qty: str       # 거래량
    trde_prica: str     # 거래대금
    dt: str             # 일자 (YYYYMMDD)
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    pred_pre: str       # 전일대비
    pred_pre_sig: str   # 전일대비기호
    trde_tern_rt: str   # 거래회전율


@dataclass(frozen=True)
class StockDayChart:
    """주식일봉차트조회 응답 (ka10081).

    Args:
        stk_cd: 종목코드.
        items: 일봉 캔들 리스트.
    """

    stk_cd: str
    items: list[StockDayChartItem]


@dataclass(frozen=True)
class StockWeekChartItem:
    """주식주봉차트 단일 항목 (ka10082)."""

    cur_prc: str        # 현재가
    trde_qty: str       # 거래량
    trde_prica: str     # 거래대금
    dt: str             # 일자
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    pred_pre: str       # 전일대비
    pred_pre_sig: str   # 전일대비기호
    trde_tern_rt: str   # 거래회전율


@dataclass(frozen=True)
class StockWeekChart:
    """주식주봉차트조회 응답 (ka10082).

    Args:
        stk_cd: 종목코드.
        items: 주봉 캔들 리스트.
    """

    stk_cd: str
    items: list[StockWeekChartItem]


@dataclass(frozen=True)
class StockMonthChartItem:
    """주식월봉차트 단일 항목 (ka10083)."""

    cur_prc: str        # 현재가
    trde_qty: str       # 거래량
    trde_prica: str     # 거래대금
    dt: str             # 일자
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    pred_pre: str       # 전일대비
    pred_pre_sig: str   # 전일대비기호
    trde_tern_rt: str   # 거래회전율


@dataclass(frozen=True)
class StockMonthChart:
    """주식월봉차트조회 응답 (ka10083).

    Args:
        stk_cd: 종목코드.
        items: 월봉 캔들 리스트.
    """

    stk_cd: str
    items: list[StockMonthChartItem]


@dataclass(frozen=True)
class StockYearChartItem:
    """주식년봉차트 단일 항목 (ka10094)."""

    cur_prc: str        # 현재가
    trde_qty: str       # 거래량
    trde_prica: str     # 거래대금
    dt: str             # 일자
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가


@dataclass(frozen=True)
class StockYearChart:
    """주식년봉차트조회 응답 (ka10094).

    Args:
        stk_cd: 종목코드.
        items: 년봉 캔들 리스트.
    """

    stk_cd: str
    items: list[StockYearChartItem]


@dataclass(frozen=True)
class InvestorChartItem:
    """종목별투자자기관별차트 단일 항목 (ka10060)."""

    dt: str             # 일자
    cur_prc: str        # 현재가
    pred_pre: str       # 전일대비
    acc_trde_prica: str # 누적거래대금
    ind_invsr: str      # 개인투자자
    frgnr_invsr: str    # 외국인투자자
    orgn: str           # 기관계
    fnnc_invt: str      # 금융투자
    insrnc: str         # 보험
    invtrt: str         # 투신
    etc_fnnc: str       # 기타금융
    bank: str           # 은행
    penfnd_etc: str     # 연기금등
    samo_fund: str      # 사모펀드
    natn: str           # 국가
    etc_corp: str       # 기타법인
    natfor: str         # 내외국인


@dataclass(frozen=True)
class InvestorChart:
    """종목별투자자기관별차트 응답 (ka10060).

    Args:
        items: 투자자기관별 차트 리스트.
    """

    items: list[InvestorChartItem]


@dataclass(frozen=True)
class IntraInvestorChartItem:
    """장중투자자별매매차트 단일 항목 (ka10064)."""

    tm: str             # 시간 (HHMMSS)
    frgnr_invsr: str    # 외국인투자자
    orgn: str           # 기관계
    invtrt: str         # 투신
    insrnc: str         # 보험
    bank: str           # 은행
    penfnd_etc: str     # 연기금등
    etc_corp: str       # 기타법인
    natn: str           # 국가


@dataclass(frozen=True)
class IntraInvestorChart:
    """장중투자자별매매차트 응답 (ka10064).

    Args:
        items: 장중투자자 매매 차트 리스트.
    """

    items: list[IntraInvestorChartItem]


@dataclass(frozen=True)
class SectorCandleItem:
    """업종 캔들 단일 항목 (틱·분봉 공통)."""

    cur_prc: str        # 현재가 (지수값 × 100, 소수점 제거)
    trde_qty: str       # 거래량
    cntr_tm: str        # 체결시간
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    pred_pre: str       # 전일대비
    pred_pre_sig: str   # 전일대비기호


@dataclass(frozen=True)
class SectorTickChart:
    """업종틱차트조회 응답 (ka20004).

    Args:
        inds_cd: 업종코드.
        items: 틱 캔들 리스트.
    """

    inds_cd: str
    items: list[SectorCandleItem]


@dataclass(frozen=True)
class SectorMinChartItem:
    """업종분봉차트 단일 항목 (ka20005)."""

    cur_prc: str        # 현재가
    trde_qty: str       # 거래량
    cntr_tm: str        # 체결시간
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    acc_trde_qty: str   # 누적거래량
    pred_pre: str       # 전일대비
    pred_pre_sig: str   # 전일대비기호


@dataclass(frozen=True)
class SectorMinChart:
    """업종분봉조회 응답 (ka20005).

    Args:
        inds_cd: 업종코드.
        items: 분봉 캔들 리스트.
    """

    inds_cd: str
    items: list[SectorMinChartItem]


@dataclass(frozen=True)
class SectorDayChartItem:
    """업종 일/주/월/년봉 단일 항목 (ka20006/07/08/19 공통)."""

    cur_prc: str        # 현재가
    trde_qty: str       # 거래량
    dt: str             # 일자
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    trde_prica: str     # 거래대금


@dataclass(frozen=True)
class SectorDayChart:
    """업종일봉조회 응답 (ka20006).

    Args:
        inds_cd: 업종코드.
        items: 일봉 리스트.
    """

    inds_cd: str
    items: list[SectorDayChartItem]


@dataclass(frozen=True)
class SectorWeekChart:
    """업종주봉조회 응답 (ka20007).

    Args:
        inds_cd: 업종코드.
        items: 주봉 리스트.
    """

    inds_cd: str
    items: list[SectorDayChartItem]


@dataclass(frozen=True)
class SectorMonthChart:
    """업종월봉조회 응답 (ka20008).

    Args:
        inds_cd: 업종코드.
        items: 월봉 리스트.
    """

    inds_cd: str
    items: list[SectorDayChartItem]


@dataclass(frozen=True)
class SectorYearChart:
    """업종년봉조회 응답 (ka20019).

    Args:
        inds_cd: 업종코드.
        items: 년봉 리스트.
    """

    inds_cd: str
    items: list[SectorDayChartItem]


# ---------------------------------------------------------------------------
# 7단계 — 업종·기관/외국인·공매도·대차거래 공통 Literal 타입
# ---------------------------------------------------------------------------

type SectMrktType = Literal["kospi", "kosdaq", "kospi200"]
"""업종 시장구분.

- ``"kospi"``: 코스피 (0)
- ``"kosdaq"``: 코스닥 (1)
- ``"kospi200"``: 코스피200 (2)
"""

type SectAmtQtyType = Literal["amount", "qty"]
"""업종별 금액수량구분.

- ``"amount"``: 금액 (0)
- ``"qty"``: 수량 (1)
"""

type SectExchangeType = Literal["krx", "nxt", "all"]
"""업종 거래소구분.

- ``"krx"``: KRX (1)
- ``"nxt"``: NXT (2)
- ``"all"``: 통합 (3)
"""

type FrgnDuration = Literal["1", "3", "5", "10", "20", "120", "custom"]
"""기관/외국인 연속매매 기간.

- ``"1"``: 최근 1일
- ``"3"``: 3일
- ``"5"``: 5일
- ``"10"``: 10일
- ``"20"``: 20일
- ``"120"``: 120일
- ``"custom"``: 시작일자/종료일자로 직접 지정 (``"0"`` 전달)
"""

type FrgnStockSectType = Literal["stock", "sector"]
"""기관/외국인 종목업종구분.

- ``"stock"``: 종목(주식) (0)
- ``"sector"``: 업종 (1)
"""

type SlbMrktType = Literal["kospi", "kosdaq"]
"""대차거래 시장구분.

- ``"kospi"``: 코스피 (001)
- ``"kosdaq"``: 코스닥 (101)
"""


# ---------------------------------------------------------------------------
# 7단계 — 업종 응답 모델
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SectorProgram:
    """업종프로그램요청 응답 (ka10010)."""

    dfrt_trst_sell_qty: str         # 차익위탁매도수량
    dfrt_trst_sell_amt: str         # 차익위탁매도금액
    dfrt_trst_buy_qty: str          # 차익위탁매수수량
    dfrt_trst_buy_amt: str          # 차익위탁매수금액
    dfrt_trst_netprps_qty: str      # 차익위탁순매수수량
    dfrt_trst_netprps_amt: str      # 차익위탁순매수금액
    ndiffpro_trst_sell_qty: str     # 비차익위탁매도수량
    ndiffpro_trst_sell_amt: str     # 비차익위탁매도금액
    ndiffpro_trst_buy_qty: str      # 비차익위탁매수수량
    ndiffpro_trst_buy_amt: str      # 비차익위탁매수금액
    ndiffpro_trst_netprps_qty: str  # 비차익위탁순매수수량
    ndiffpro_trst_netprps_amt: str  # 비차익위탁순매수금액
    all_dfrt_trst_sell_qty: str     # 전체차익위탁매도수량
    all_dfrt_trst_sell_amt: str     # 전체차익위탁매도금액
    all_dfrt_trst_buy_qty: str      # 전체차익위탁매수수량
    all_dfrt_trst_buy_amt: str      # 전체차익위탁매수금액
    all_dfrt_trst_netprps_qty: str  # 전체차익위탁순매수수량
    all_dfrt_trst_netprps_amt: str  # 전체차익위탁순매수금액


@dataclass(frozen=True)
class SectorInvestorNetBuyItem:
    """업종별투자자순매수 단일 항목."""

    inds_cd: str                    # 업종코드
    inds_nm: str                    # 업종명
    cur_prc: str                    # 현재가
    pre_smbol: str                  # 대비부호
    pred_pre: str                   # 전일대비
    flu_rt: str                     # 등락율
    trde_qty: str                   # 거래량
    sc_netprps: str                 # 증권순매수
    insrnc_netprps: str             # 보험순매수
    invtrt_netprps: str             # 투신순매수
    bank_netprps: str               # 은행순매수
    jnsinkm_netprps: str            # 종신금순매수
    endw_netprps: str               # 기금순매수
    etc_corp_netprps: str           # 기타법인순매수
    ind_netprps: str                # 개인순매수
    frgnr_netprps: str              # 외국인순매수
    native_trmt_frgnr_netprps: str  # 내국인대우외국인순매수
    natn_netprps: str               # 국가순매수
    samo_fund_netprps: str          # 사모펀드순매수
    orgn_netprps: str               # 기관계순매수


@dataclass(frozen=True)
class SectorInvestorNetBuy:
    """업종별투자자순매수요청 응답 (ka10051).

    Args:
        items: 업종별순매수 리스트.
    """

    items: list[SectorInvestorNetBuyItem]


@dataclass(frozen=True)
class SectorPriceTmItem:
    """업종현재가 시간별 단일 항목."""

    tm_n: str           # 시간
    cur_prc_n: str      # 현재가
    pred_pre_sig_n: str # 전일대비기호
    pred_pre_n: str     # 전일대비
    flu_rt_n: str       # 등락률
    trde_qty_n: str     # 거래량
    acc_trde_qty_n: str # 누적거래량


@dataclass(frozen=True)
class SectorPrice:
    """업종현재가요청 응답 (ka20001).

    Args:
        cur_prc: 현재가.
        items: 시간별 현재가 리스트.
    """

    cur_prc: str                # 현재가
    pred_pre_sig: str           # 전일대비기호
    pred_pre: str               # 전일대비
    flu_rt: str                 # 등락률
    trde_qty: str               # 거래량
    trde_prica: str             # 거래대금
    trde_frmatn_stk_num: str    # 거래형성종목수
    trde_frmatn_rt: str         # 거래형성비율
    open_pric: str              # 시가
    high_pric: str              # 고가
    low_pric: str               # 저가
    upl: str                    # 상한
    rising: str                 # 상승
    stdns: str                  # 보합
    fall: str                   # 하락
    lst: str                    # 하한
    wk52_hgst_pric: str         # 52주최고가
    wk52_hgst_pric_dt: str      # 52주최고가일
    wk52_hgst_pric_pre_rt: str  # 52주최고가대비율
    wk52_lwst_pric: str         # 52주최저가
    wk52_lwst_pric_dt: str      # 52주최저가일
    wk52_lwst_pric_pre_rt: str  # 52주최저가대비율
    items: list[SectorPriceTmItem]  # 시간별 현재가 리스트


@dataclass(frozen=True)
class SectorStockPriceItem:
    """업종별주가 단일 항목."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pred_pre_sig: str   # 전일대비기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락률
    now_trde_qty: str   # 현재거래량
    sel_bid: str        # 매도호가
    buy_bid: str        # 매수호가
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가


@dataclass(frozen=True)
class SectorStockPrices:
    """업종별주가요청 응답 (ka20002).

    Args:
        items: 업종별주가 리스트.
    """

    items: list[SectorStockPriceItem]


@dataclass(frozen=True)
class AllSectorIndexItem:
    """전업종지수 단일 항목."""

    stk_cd: str     # 업종코드
    stk_nm: str     # 업종명
    cur_prc: str    # 현재가
    pre_sig: str    # 대비기호
    pred_pre: str   # 전일대비
    flu_rt: str     # 등락률
    trde_qty: str   # 거래량
    wght: str       # 비중
    trde_prica: str # 거래대금
    upl: str        # 상한
    rising: str     # 상승
    stdns: str      # 보합
    fall: str       # 하락
    lst: str        # 하한
    flo_stk_num: str  # 상장종목수


@dataclass(frozen=True)
class AllSectorIndex:
    """전업종지수요청 응답 (ka20003).

    Args:
        items: 전업종지수 리스트.
    """

    items: list[AllSectorIndexItem]


@dataclass(frozen=True)
class SectorDailyPriceItem:
    """업종현재가 일별 단일 항목."""

    dt_n: str           # 일자
    cur_prc_n: str      # 현재가
    pred_pre_sig_n: str # 전일대비기호
    pred_pre_n: str     # 전일대비
    flu_rt_n: str       # 등락률
    acc_trde_qty_n: str # 누적거래량


@dataclass(frozen=True)
class SectorDailyPrice:
    """업종현재가일별요청 응답 (ka20009).

    Args:
        cur_prc: 현재가.
        items: 일별 현재가 리스트.
    """

    cur_prc: str                # 현재가
    pred_pre_sig: str           # 전일대비기호
    pred_pre: str               # 전일대비
    flu_rt: str                 # 등락률
    trde_qty: str               # 거래량
    trde_prica: str             # 거래대금
    trde_frmatn_stk_num: str    # 거래형성종목수
    trde_frmatn_rt: str         # 거래형성비율
    open_pric: str              # 시가
    high_pric: str              # 고가
    low_pric: str               # 저가
    upl: str                    # 상한
    rising: str                 # 상승
    stdns: str                  # 보합
    fall: str                   # 하락
    lst: str                    # 하한
    wk52_hgst_pric: str         # 52주최고가
    wk52_hgst_pric_dt: str      # 52주최고가일
    wk52_hgst_pric_pre_rt: str  # 52주최고가대비율
    wk52_lwst_pric: str         # 52주최저가
    wk52_lwst_pric_dt: str      # 52주최저가일
    wk52_lwst_pric_pre_rt: str  # 52주최저가대비율
    items: list[SectorDailyPriceItem]  # 일별 현재가 리스트


# ---------------------------------------------------------------------------
# 7단계 — 기관/외국인 응답 모델
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ForeignTradeItem:
    """주식외국인 종목별 매매동향 단일 항목."""

    dt: str             # 일자
    close_pric: str     # 종가
    pred_pre: str       # 전일대비
    trde_qty: str       # 거래량
    chg_qty: str        # 변동수량
    poss_stkcnt: str    # 보유주식수
    wght: str           # 비중
    gain_pos_stkcnt: str  # 취득가능주식수
    frgnr_limit: str    # 외국인한도
    frgnr_limit_irds: str  # 외국인한도증감
    limit_exh_rt: str   # 한도소진률


@dataclass(frozen=True)
class ForeignTrade:
    """주식외국인종목별매매동향 응답 (ka10008).

    Args:
        items: 외국인 매매동향 리스트.
    """

    items: list[ForeignTradeItem]


@dataclass(frozen=True)
class InstitutionTrade:
    """주식기관요청 응답 (ka10009)."""

    date: str               # 날짜
    close_pric: str         # 종가
    pre: str                # 대비
    orgn_dt_acc: str        # 기관기간누적
    orgn_daly_nettrde: str  # 기관일별순매매
    frgnr_daly_nettrde: str # 외국인일별순매매
    frgnr_qota_rt: str      # 외국인지분율


@dataclass(frozen=True)
class InstFrgnConsecutiveItem:
    """기관외국인연속매매현황 단일 항목."""

    rank: str                   # 순위
    stk_cd: str                 # 종목코드
    stk_nm: str                 # 종목명
    prid_stkpc_flu_rt: str      # 기간중주가등락률
    orgn_nettrde_amt: str       # 기관순매매금액
    orgn_nettrde_qty: str       # 기관순매매량
    orgn_cont_netprps_dys: str  # 기관계연속순매수일수
    orgn_cont_netprps_qty: str  # 기관계연속순매수량
    orgn_cont_netprps_amt: str  # 기관계연속순매수금액
    frgnr_nettrde_qty: str      # 외국인순매매량
    frgnr_nettrde_amt: str      # 외국인순매매액
    frgnr_cont_netprps_dys: str # 외국인연속순매수일수
    frgnr_cont_netprps_qty: str # 외국인연속순매수량
    frgnr_cont_netprps_amt: str # 외국인연속순매수금액
    nettrde_qty: str            # 순매매량
    nettrde_amt: str            # 순매매액
    tot_cont_netprps_dys: str   # 합계연속순매수일수
    tot_cont_nettrde_qty: str   # 합계연속순매매수량
    tot_cont_netprps_amt: str   # 합계연속순매수금액


@dataclass(frozen=True)
class InstFrgnConsecutiveTrade:
    """기관외국인연속매매현황요청 응답 (ka10131).

    Args:
        items: 기관외국인연속매매현황 리스트.
    """

    items: list[InstFrgnConsecutiveItem]


# ---------------------------------------------------------------------------
# 7단계 — 공매도·대차거래 응답 모델
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ShortSellItem:
    """공매도추이 단일 항목."""

    dt: str                 # 일자
    close_pric: str         # 종가
    pred_pre_sig: str       # 전일대비기호
    pred_pre: str           # 전일대비
    flu_rt: str             # 등락율
    trde_qty: str           # 거래량
    shrts_qty: str          # 공매도량
    ovr_shrts_qty: str      # 누적공매도량
    trde_wght: str          # 매매비중
    shrts_trde_prica: str   # 공매도거래대금
    shrts_avg_pric: str     # 공매도평균가


@dataclass(frozen=True)
class ShortSellTrend:
    """공매도추이요청 응답 (ka10014).

    Args:
        items: 공매도추이 리스트.
    """

    items: list[ShortSellItem]


@dataclass(frozen=True)
class StockLoanItem:
    """대차거래추이 단일 항목."""

    dt: str                 # 일자
    dbrt_trde_cntrcnt: str  # 대차거래체결주수
    dbrt_trde_rpy: str      # 대차거래상환주수
    dbrt_trde_irds: str     # 대차거래증감
    rmnd: str               # 잔고주수
    remn_amt: str           # 잔고금액


@dataclass(frozen=True)
class StockLoanTrend:
    """대차거래추이요청 응답 (ka10068).

    Args:
        items: 대차거래추이 리스트.
    """

    items: list[StockLoanItem]


@dataclass(frozen=True)
class StockLoanTop10Item:
    """대차거래상위10종목 단일 항목."""

    stk_nm: str             # 종목명
    stk_cd: str             # 종목코드
    dbrt_trde_cntrcnt: str  # 대차거래체결주수
    dbrt_trde_rpy: str      # 대차거래상환주수
    rmnd: str               # 잔고주수
    remn_amt: str           # 잔고금액


@dataclass(frozen=True)
class StockLoanTop10:
    """대차거래상위10종목요청 응답 (ka10069).

    Args:
        dbrt_trde_cntrcnt_sum: 대차거래체결주수합.
        items: 대차거래상위10종목 리스트.
    """

    dbrt_trde_cntrcnt_sum: str  # 대차거래체결주수합
    dbrt_trde_rpy_sum: str      # 대차거래상환주수합
    rmnd_sum: str               # 잔고주수합
    remn_amt_sum: str           # 잔고금액합
    dbrt_trde_cntrcnt_rt: str   # 대차거래체결주수비율
    dbrt_trde_rpy_rt: str       # 대차거래상환주수비율
    rmnd_rt: str                # 잔고주수비율
    remn_amt_rt: str            # 잔고금액비율
    items: list[StockLoanTop10Item]


@dataclass(frozen=True)
class StockLoanByStockItem:
    """대차거래추이(종목별) 단일 항목."""

    dt: str                 # 일자
    dbrt_trde_cntrcnt: str  # 대차거래체결주수
    dbrt_trde_rpy: str      # 대차거래상환주수
    dbrt_trde_irds: str     # 대차거래증감
    rmnd: str               # 잔고주수
    remn_amt: str           # 잔고금액


@dataclass(frozen=True)
class StockLoanByStock:
    """대차거래추이요청(종목별) 응답 (ka20068).

    Args:
        items: 대차거래추이(종목별) 리스트.
    """

    items: list[StockLoanByStockItem]


@dataclass(frozen=True)
class StockLoanHistoryItem:
    """대차거래내역 단일 항목."""

    stk_nm: str             # 종목명
    stk_cd: str             # 종목코드
    dbrt_trde_cntrcnt: str  # 대차거래체결주수
    dbrt_trde_rpy: str      # 대차거래상환주수
    rmnd: str               # 잔고주수
    remn_amt: str           # 잔고금액


@dataclass(frozen=True)
class StockLoanHistory:
    """대차거래내역요청 응답 (ka90012).

    Args:
        items: 대차거래내역 리스트.
    """

    items: list[StockLoanHistoryItem]


# ---------------------------------------------------------------------------
# 8단계 — ETF·ELW·테마·프로그램매매 공통 Literal 타입
# ---------------------------------------------------------------------------

type EtfDuration = Literal["1w", "1m", "6m", "1y"]
"""ETF 기간구분.

- ``"1w"``: 1주 (0)
- ``"1m"``: 1달 (1)
- ``"6m"``: 6개월 (2)
- ``"1y"``: 1년 (3)
"""

type ElwFlucType = Literal["surge", "plunge"]
"""ELW 등락구분.

- ``"surge"``: 급등 (1)
- ``"plunge"``: 급락 (2)
"""

type ElwRightType = Literal["all", "call", "put", "dc", "dp", "ex", "early_call", "early_put"]
"""ELW 권리구분.

- ``"all"``: 전체 (000)
- ``"call"``: 콜 (001)
- ``"put"``: 풋 (002)
- ``"dc"``: DC (003)
- ``"dp"``: DP (004)
- ``"ex"``: EX (005)
- ``"early_call"``: 조기종료콜 (006)
- ``"early_put"``: 조기종료풋 (007)
"""

type ElwSortType = Literal["rise_rate", "rise_gap", "fall_rate", "fall_gap", "volume", "amount", "expire"]
"""ELW 정렬구분.

- ``"rise_rate"``: 상승율순 (1)
- ``"rise_gap"``: 상승폭순 (2)
- ``"fall_rate"``: 하락율순 (3)
- ``"fall_gap"``: 하락폭순 (4)
- ``"volume"``: 거래량순 (5)
- ``"amount"``: 거래대금순 (6)
- ``"expire"``: 잔존일순 (7)
"""

type ThemeSearchType = Literal["all", "theme", "stock"]
"""테마 검색구분.

- ``"all"``: 전체검색 (0)
- ``"theme"``: 테마검색 (1)
- ``"stock"``: 종목검색 (2)
"""


# ---------------------------------------------------------------------------
# 8단계 — ETF 응답 모델
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EtfReturnItem:
    """ETF수익율 단일 항목."""

    etfprft_rt: str         # ETF수익률
    cntr_prft_rt: str       # 체결수익률
    for_netprps_qty: str    # 외인순매수수량
    orgn_netprps_qty: str   # 기관순매수수량


@dataclass(frozen=True)
class EtfReturn:
    """ETF수익율요청 응답 (ka40001).

    Args:
        items: ETF수익율 리스트.
    """

    items: list[EtfReturnItem]


@dataclass(frozen=True)
class EtfInfo:
    """ETF종목정보요청 응답 (ka40002).

    Args:
        stk_nm: 종목명.
        etfobjt_idex_nm: ETF대상지수명.
        wonju_pric: 원주가격.
        etftxon_type: ETF과세유형.
        etntxon_type: ETN과세유형.
    """

    stk_nm: str             # 종목명
    etfobjt_idex_nm: str    # ETF대상지수명
    wonju_pric: str         # 원주가격
    etftxon_type: str       # ETF과세유형
    etntxon_type: str       # ETN과세유형


@dataclass(frozen=True)
class EtfDailyTrendItem:
    """ETF일별추이 단일 항목."""

    cntr_dt: str            # 체결일자
    cur_prc: str            # 현재가
    pre_sig: str            # 대비기호
    pred_pre: str           # 전일대비
    pre_rt: str             # 대비율
    trde_qty: str           # 거래량
    nav: str                # NAV
    acc_trde_prica: str     # 누적거래대금
    navidex_dispty_rt: str  # NAV/지수괴리율
    navetfdispty_rt: str    # NAV/ETF괴리율
    trace_eor_rt: str       # 추적오차율
    trace_cur_prc: str      # 추적현재가
    trace_pred_pre: str     # 추적전일대비
    trace_pre_sig: str      # 추적대비기호


@dataclass(frozen=True)
class EtfDailyTrend:
    """ETF일별추이요청 응답 (ka40003).

    Args:
        items: ETF일별추이 리스트.
    """

    items: list[EtfDailyTrendItem]


@dataclass(frozen=True)
class EtfAllQuoteItem:
    """ETF전체시세 단일 항목."""

    stk_cd: str             # 종목코드
    stk_cls: str            # 종목분류
    stk_nm: str             # 종목명
    close_pric: str         # 종가
    pre_sig: str            # 대비기호
    pred_pre: str           # 전일대비
    pre_rt: str             # 대비율
    trde_qty: str           # 거래량
    nav: str                # NAV
    trace_eor_rt: str       # 추적오차율
    txbs: str               # 과표기준
    dvid_bf_base: str       # 배당전기준
    pred_dvida: str         # 전일배당금
    trace_idex_nm: str      # 추적지수명
    drng: str               # 배수
    trace_idex_cd: str      # 추적지수코드
    trace_idex: str         # 추적지수
    trace_flu_rt: str       # 추적등락율


@dataclass(frozen=True)
class EtfAllQuote:
    """ETF전체시세요청 응답 (ka40004).

    Args:
        items: ETF전체시세 리스트.
    """

    items: list[EtfAllQuoteItem]


@dataclass(frozen=True)
class EtfTimeTrendItem:
    """ETF시간대별추이 단일 항목 (ka40006)."""

    tm: str                         # 시간
    close_pric: str                 # 종가
    pre_sig: str                    # 대비기호
    pred_pre: str                   # 전일대비
    flu_rt: str                     # 등락율
    trde_qty: str                   # 거래량
    nav: str                        # NAV
    trde_prica: str                 # 거래대금
    navidex: str                    # NAV지수
    navetf: str                     # NAVETF
    trace: str                      # 추적
    trace_idex: str                 # 추적지수
    trace_idex_pred_pre: str        # 추적지수전일대비
    trace_idex_pred_pre_sig: str    # 추적지수전일대비기호


@dataclass(frozen=True)
class EtfTimeTrend:
    """ETF시간대별추이요청 응답 (ka40006).

    Args:
        stk_nm: 종목명.
        etfobjt_idex_nm: ETF대상지수명.
        wonju_pric: 원주가격.
        etftxon_type: ETF과세유형.
        etntxon_type: ETN과세유형.
        items: ETF시간대별추이 리스트.
    """

    stk_nm: str          # 종목명
    etfobjt_idex_nm: str # ETF대상지수명
    wonju_pric: str      # 원주가격
    etftxon_type: str    # ETF과세유형
    etntxon_type: str    # ETN과세유형
    items: list[EtfTimeTrendItem]


@dataclass(frozen=True)
class EtfTimeFillItem:
    """ETF시간대별체결 단일 항목 (ka40007)."""

    cntr_tm: str    # 체결시간
    cur_prc: str    # 현재가
    pre_sig: str    # 대비기호
    pred_pre: str   # 전일대비
    trde_qty: str   # 거래량
    stex_tp: str    # 거래소구분


@dataclass(frozen=True)
class EtfTimeFill:
    """ETF시간대별체결요청 응답 (ka40007).

    Args:
        stk_cls: 종목분류.
        stk_nm: 종목명.
        etfobjt_idex_nm: ETF대상지수명.
        etfobjt_idex_cd: ETF대상지수코드.
        objt_idex_pre_rt: 대상지수대비율.
        wonju_pric: 원주가격.
        items: ETF시간대별체결 리스트.
    """

    stk_cls: str            # 종목분류
    stk_nm: str             # 종목명
    etfobjt_idex_nm: str    # ETF대상지수명
    etfobjt_idex_cd: str    # ETF대상지수코드
    objt_idex_pre_rt: str   # 대상지수대비율
    wonju_pric: str         # 원주가격
    items: list[EtfTimeFillItem]


@dataclass(frozen=True)
class EtfDailyFillItem:
    """ETF일자별체결 단일 항목 (ka40008)."""

    dt: str                 # 일자
    cur_prc_n: str          # 현재가n
    pre_sig_n: str          # 대비기호n
    pred_pre_n: str         # 전일대비n
    acc_trde_qty: str       # 누적거래량
    for_netprps_qty: str    # 외인순매수수량
    orgn_netprps_qty: str   # 기관순매수수량


@dataclass(frozen=True)
class EtfDailyFill:
    """ETF일자별체결요청 응답 (ka40008).

    Args:
        cntr_tm: 체결시간.
        cur_prc: 현재가.
        pre_sig: 대비기호.
        pred_pre: 전일대비.
        trde_qty: 거래량.
        items: ETF일자별체결 리스트.
    """

    cntr_tm: str    # 체결시간
    cur_prc: str    # 현재가
    pre_sig: str    # 대비기호
    pred_pre: str   # 전일대비
    trde_qty: str   # 거래량
    items: list[EtfDailyFillItem]


@dataclass(frozen=True)
class EtfNavItem:
    """ETFNAV 단일 항목 (ka40009)."""

    nav: str            # NAV
    navpred_pre: str    # NAV전일대비
    navflu_rt: str      # NAV등락율
    trace_eor_rt: str   # 추적오차율
    dispty_rt: str      # 괴리율
    stkcnt: str         # 주식수
    base_pric: str      # 기준가
    for_rmnd_qty: str   # 외인보유수량
    repl_pric: str      # 대용가
    conv_pric: str      # 환산가격
    drstk: str          # DR/주
    wonju_pric: str     # 원주가격


@dataclass(frozen=True)
class EtfNav:
    """ETF시간대별체결요청 응답 (ka40009).

    Args:
        items: ETFNAV 리스트.
    """

    items: list[EtfNavItem]


@dataclass(frozen=True)
class EtfTimeTrend2Item:
    """ETF시간대별추이 단일 항목 (ka40010)."""

    cur_prc: str        # 현재가
    pre_sig: str        # 대비기호
    pred_pre: str       # 전일대비
    trde_qty: str       # 거래량
    for_netprps: str    # 외인순매수


@dataclass(frozen=True)
class EtfTimeTrend2:
    """ETF시간대별추이요청 응답 (ka40010).

    Args:
        items: ETF시간대별추이 리스트.
    """

    items: list[EtfTimeTrend2Item]


# ---------------------------------------------------------------------------
# 8단계 — ELW 응답 모델
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ElwDailySensItem:
    """ELW일별민감도지표 단일 항목."""

    dt: str     # 일자
    iv: str     # IV
    delta: str  # 델타
    gam: str    # 감마
    theta: str  # 쎄타
    vega: str   # 베가
    law: str    # 로
    lp: str     # LP


@dataclass(frozen=True)
class ElwDailySens:
    """ELW일별민감도지표요청 응답 (ka10048).

    Args:
        items: ELW일별민감도지표 리스트.
    """

    items: list[ElwDailySensItem]


@dataclass(frozen=True)
class ElwSensItem:
    """ELW민감도지표 단일 항목."""

    cntr_tm: str        # 체결시간
    cur_prc: str        # 현재가
    elwtheory_pric: str # ELW이론가
    iv: str             # IV
    delta: str          # 델타
    gam: str            # 감마
    theta: str          # 쎄타
    vega: str           # 베가
    law: str            # 로
    lp: str             # LP


@dataclass(frozen=True)
class ElwSens:
    """ELW민감도지표요청 응답 (ka10050).

    Args:
        items: ELW민감도지표 리스트.
    """

    items: list[ElwSensItem]


@dataclass(frozen=True)
class ElwPriceSurgeItem:
    """ELW가격급등락 단일 항목."""

    stk_cd: str                 # 종목코드
    rank: str                   # 순위
    stk_nm: str                 # 종목명
    pre_sig: str                # 대비기호
    pred_pre: str               # 전일대비
    trde_end_elwbase_pric: str  # 거래종료ELW기준가
    cur_prc: str                # 현재가
    base_pre: str               # 기준대비
    trde_qty: str               # 거래량
    jmp_rt: str                 # 급등율


@dataclass(frozen=True)
class ElwPriceSurge:
    """ELW가격급등락요청 응답 (ka30001).

    Args:
        base_pric_tm: 기준가시간.
        items: ELW가격급등락 리스트.
    """

    base_pric_tm: str   # 기준가시간
    items: list[ElwPriceSurgeItem]


@dataclass(frozen=True)
class ElwBrokerNetTradeItem:
    """거래원별ELW순매매상위 단일 항목."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    stkpc_flu: str      # 주가등락
    flu_rt: str         # 등락율
    trde_qty: str       # 거래량
    netprps: str        # 순매수
    buy_trde_qty: str   # 매수거래량
    sel_trde_qty: str   # 매도거래량


@dataclass(frozen=True)
class ElwBrokerNetTrade:
    """거래원별ELW순매매상위요청 응답 (ka30002).

    Args:
        items: 거래원별ELW순매매상위 리스트.
    """

    items: list[ElwBrokerNetTradeItem]


@dataclass(frozen=True)
class ElwLpDailyItem:
    """ELWLP보유일별추이 단일 항목."""

    dt: str         # 일자
    cur_prc: str    # 현재가
    pre_tp: str     # 대비구분
    pred_pre: str   # 전일대비
    flu_rt: str     # 등락율
    trde_qty: str   # 거래량
    trde_prica: str # 거래대금
    chg_qty: str    # 변동수량
    lprmnd_qty: str # LP보유수량
    wght: str       # 비중


@dataclass(frozen=True)
class ElwLpDaily:
    """ELWLP보유일별추이요청 응답 (ka30003).

    Args:
        items: ELWLP보유일별추이 리스트.
    """

    items: list[ElwLpDailyItem]


@dataclass(frozen=True)
class ElwGapItem:
    """ELW괴리율 단일 항목."""

    stk_cd: str         # 종목코드
    isscomp_nm: str     # 발행사명
    sqnc: str           # 회차
    base_aset_nm: str   # 기초자산명
    rght_tp: str        # 권리구분
    dispty_rt: str      # 괴리율
    basis: str          # 베이시스
    srvive_dys: str     # 잔존일수
    theory_pric: str    # 이론가
    cur_prc: str        # 현재가
    pre_tp: str         # 대비구분
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락율
    trde_qty: str       # 거래량
    stk_nm: str         # 종목명


@dataclass(frozen=True)
class ElwGap:
    """ELW괴리율요청 응답 (ka30004).

    Args:
        items: ELW괴리율 리스트.
    """

    items: list[ElwGapItem]


@dataclass(frozen=True)
class ElwSearchItem:
    """ELW조건검색 단일 항목."""

    stk_cd: str                             # 종목코드
    isscomp_nm: str                         # 발행사명
    sqnc: str                               # 회차
    base_aset_nm: str                       # 기초자산명
    rght_tp: str                            # 권리구분
    expr_dt: str                            # 만기일
    cur_prc: str                            # 현재가
    pre_tp: str                             # 대비구분
    pred_pre: str                           # 전일대비
    flu_rt: str                             # 등락율
    trde_qty: str                           # 거래량
    trde_qty_pre: str                       # 거래량대비
    trde_prica: str                         # 거래대금
    pred_trde_qty: str                      # 전일거래량
    sel_bid: str                            # 매도호가
    buy_bid: str                            # 매수호가
    prty: str                               # 패리티
    gear_rt: str                            # 기어링비율
    pl_qutr_rt: str                         # 손익분기율
    cfp: str                                # 자본지지점
    theory_pric: str                        # 이론가
    innr_vltl: str                          # 내재변동성
    delta: str                              # 델타
    lvrg: str                               # 레버리지
    exec_pric: str                          # 행사가격
    cnvt_rt: str                            # 전환비율
    lpposs_rt: str                          # LP보유비율
    pl_qutr_pt: str                         # 손익분기점
    fin_trde_dt: str                        # 최종거래일
    flo_dt: str                             # 상장일
    lpinitlast_suply_dt: str               # LP초종공급일
    stk_nm: str                             # 종목명
    srvive_dys: str                         # 잔존일수
    dispty_rt: str                          # 괴리율
    lpmmcm_nm: str                          # LP회원사명
    lpmmcm_nm_1: str                        # LP회원사명1
    lpmmcm_nm_2: str                        # LP회원사명2
    xraymont_cntr_qty_arng_trde_tp: str    # Xray순간체결량정리매매구분
    xraymont_cntr_qty_profa_100tp: str     # Xray순간체결량증거금100구분


@dataclass(frozen=True)
class ElwSearch:
    """ELW조건검색요청 응답 (ka30005).

    Args:
        items: ELW조건검색 리스트.
    """

    items: list[ElwSearchItem]


@dataclass(frozen=True)
class ElwFlucRankItem:
    """ELW등락율순위 단일 항목."""

    rank: str       # 순위
    stk_cd: str     # 종목코드
    stk_nm: str     # 종목명
    cur_prc: str    # 현재가
    pre_sig: str    # 대비기호
    pred_pre: str   # 전일대비
    flu_rt: str     # 등락률
    sel_req: str    # 매도잔량
    buy_req: str    # 매수잔량
    trde_qty: str   # 거래량
    trde_prica: str # 거래대금


@dataclass(frozen=True)
class ElwFlucRank:
    """ELW등락율순위요청 응답 (ka30009).

    Args:
        items: ELW등락율순위 리스트.
    """

    items: list[ElwFlucRankItem]


@dataclass(frozen=True)
class ElwBalRankItem:
    """ELW잔량순위 단일 항목."""

    stk_cd: str         # 종목코드
    rank: str           # 순위
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pre_sig: str        # 대비기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락률
    trde_qty: str       # 거래량
    sel_req: str        # 매도잔량
    buy_req: str        # 매수잔량
    netprps_req: str    # 순매수잔량
    trde_prica: str     # 거래대금


@dataclass(frozen=True)
class ElwBalRank:
    """ELW잔량순위요청 응답 (ka30010).

    Args:
        items: ELW잔량순위 리스트.
    """

    items: list[ElwBalRankItem]


@dataclass(frozen=True)
class ElwAccessRateItem:
    """ELW근접율 단일 항목."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    pre_sig: str        # 대비기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락율
    acc_trde_qty: str   # 누적거래량
    alacc_rt: str       # 근접율


@dataclass(frozen=True)
class ElwAccessRate:
    """ELW근접율요청 응답 (ka30011).

    Args:
        items: ELW근접율 리스트.
    """

    items: list[ElwAccessRateItem]


@dataclass(frozen=True)
class ElwDetail:
    """ELW종목상세정보요청 응답 (ka30012)."""

    aset_cd: str                    # 자산코드
    cur_prc: str                    # 현재가
    pred_pre_sig: str               # 전일대비기호
    pred_pre: str                   # 전일대비
    flu_rt: str                     # 등락율
    lpmmcm_nm: str                  # LP회원사명
    lpmmcm_nm_1: str                # LP회원사명1
    lpmmcm_nm_2: str                # LP회원사명2
    elwrght_cntn: str               # ELW권리내용
    elwexpr_evlt_pric: str          # ELW만기평가가격
    elwtheory_pric: str             # ELW이론가
    dispty_rt: str                  # 괴리율
    elwinnr_vltl: str               # ELW내재변동성
    exp_rght_pric: str              # 예상권리가
    elwpl_qutr_rt: str              # ELW손익분기율
    elwexec_pric: str               # ELW행사가
    elwcnvt_rt: str                 # ELW전환비율
    elwcmpn_rt: str                 # ELW보상율
    elwpric_rising_part_rt: str     # ELW가격상승참여율
    elwrght_type: str               # ELW권리유형
    elwsrvive_dys: str              # ELW잔존일수
    stkcnt: str                     # 주식수
    elwlpord_pos: str               # ELWLP주문가능
    lpposs_rt: str                  # LP보유비율
    lprmnd_qty: str                 # LP보유수량
    elwspread: str                  # ELW스프레드
    elwprty: str                    # ELW패리티
    elwgear: str                    # ELW기어링
    elwflo_dt: str                  # ELW상장일
    elwfin_trde_dt: str             # ELW최종거래일
    expr_dt: str                    # 만기일
    exec_dt: str                    # 행사일
    lpsuply_end_dt: str             # LP공급종료일
    elwpay_dt: str                  # ELW지급일
    elwinvt_ix_comput: str          # ELW투자지표산출
    elwpay_agnt: str                # ELW지급대리인
    elwappr_way: str                # ELW결재방법
    elwrght_exec_way: str           # ELW권리행사방식
    elwpblicte_orgn: str            # ELW발행기관
    dcsn_pay_amt: str               # 확정지급액
    kobarr: str                     # KO베리어
    iv: str                         # IV
    clsprd_end_elwocr: str          # 종기종료ELW발생
    bsis_aset_1: str                # 기초자산1
    bsis_aset_comp_rt_1: str        # 기초자산구성비율1
    bsis_aset_2: str                # 기초자산2
    bsis_aset_comp_rt_2: str        # 기초자산구성비율2
    bsis_aset_3: str                # 기초자산3
    bsis_aset_comp_rt_3: str        # 기초자산구성비율3
    bsis_aset_4: str                # 기초자산4
    bsis_aset_comp_rt_4: str        # 기초자산구성비율4
    bsis_aset_5: str                # 기초자산5
    bsis_aset_comp_rt_5: str        # 기초자산구성비율5
    fr_dt: str                      # 평가시작일자
    to_dt: str                      # 평가종료일자
    fr_tm: str                      # 평가시작시간
    evlt_end_tm: str                # 평가종료시간
    evlt_pric: str                  # 평가가격
    evlt_fnsh_yn: str               # 평가완료여부
    all_hgst_pric: str              # 전체최고가
    all_lwst_pric: str              # 전체최저가
    imaf_hgst_pric: str             # 직후최고가
    imaf_lwst_pric: str             # 직후최저가
    sndhalf_mrkt_hgst_pric: str     # 후반장최고가
    sndhalf_mrkt_lwst_pric: str     # 후반장최저가


# ---------------------------------------------------------------------------
# 8단계 — 테마 응답 모델
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ThemeGroupItem:
    """테마그룹별 단일 항목."""

    thema_grp_cd: str   # 테마그룹코드
    thema_nm: str       # 테마명
    stk_num: str        # 종목수
    flu_sig: str        # 등락기호
    flu_rt: str         # 등락율
    rising_stk_num: str # 상승종목수
    fall_stk_num: str   # 하락종목수
    dt_prft_rt: str     # 기간수익률
    main_stk: str       # 주요종목


@dataclass(frozen=True)
class ThemeGroup:
    """테마그룹별요청 응답 (ka90001).

    Args:
        items: 테마그룹별 리스트.
    """

    items: list[ThemeGroupItem]


@dataclass(frozen=True)
class ThemeStockItem:
    """테마구성종목 단일 항목."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    cur_prc: str        # 현재가
    flu_sig: str        # 등락기호
    pred_pre: str       # 전일대비
    flu_rt: str         # 등락율
    acc_trde_qty: str   # 누적거래량
    sel_bid: str        # 매도호가
    sel_req: str        # 매도잔량
    buy_bid: str        # 매수호가
    buy_req: str        # 매수잔량
    dt_prft_rt_n: str   # 기간수익률n


@dataclass(frozen=True)
class ThemeStocks:
    """테마구성종목요청 응답 (ka90002).

    Args:
        flu_rt: 등락률.
        dt_prft_rt: 기간수익률.
        items: 테마구성종목 리스트.
    """

    flu_rt: str     # 등락률
    dt_prft_rt: str # 기간수익률
    items: list[ThemeStockItem]


# ---------------------------------------------------------------------------
# 8단계 — 프로그램매매 응답 모델
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProgramTop50Item:
    """프로그램순매수상위50 단일 항목."""

    rank: str               # 순위
    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    cur_prc: str            # 현재가
    flu_sig: str            # 등락기호
    pred_pre: str           # 전일대비
    flu_rt: str             # 등락율
    acc_trde_qty: str       # 누적거래량
    prm_sell_amt: str       # 프로그램매도금액
    prm_buy_amt: str        # 프로그램매수금액
    prm_netprps_amt: str    # 프로그램순매수금액


@dataclass(frozen=True)
class ProgramTop50:
    """프로그램순매수상위50요청 응답 (ka90003).

    Args:
        items: 프로그램순매수상위50 리스트.
    """

    items: list[ProgramTop50Item]


@dataclass(frozen=True)
class StockProgramStatusItem:
    """종목별프로그램매매현황 단일 항목."""

    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    cur_prc: str            # 현재가
    flu_sig: str            # 등락기호
    pred_pre: str           # 전일대비
    buy_cntr_qty: str       # 매수체결수량
    buy_cntr_amt: str       # 매수체결금액
    sel_cntr_qty: str       # 매도체결수량
    sel_cntr_amt: str       # 매도체결금액
    netprps_prica: str      # 순매수대금
    all_trde_rt: str        # 전체거래비율


@dataclass(frozen=True)
class StockProgramStatus:
    """종목별프로그램매매현황요청 응답 (ka90004).

    Args:
        tot_1: 매수체결수량합계.
        tot_2: 매수체결금액합계.
        tot_3: 매도체결수량합계.
        tot_4: 매도체결금액합계.
        tot_5: 순매수대금합계.
        tot_6: 합계6.
        items: 종목별프로그램매매현황 리스트.
    """

    tot_1: str  # 매수체결수량합계
    tot_2: str  # 매수체결금액합계
    tot_3: str  # 매도체결수량합계
    tot_4: str  # 매도체결금액합계
    tot_5: str  # 순매수대금합계
    tot_6: str  # 합계6
    items: list[StockProgramStatusItem]


@dataclass(frozen=True)
class ProgramTrendItem:
    """프로그램매매추이 단일 항목."""

    cntr_tm: str                    # 체결시간
    dfrt_trde_sel: str              # 차익거래매도
    dfrt_trde_buy: str              # 차익거래매수
    dfrt_trde_netprps: str          # 차익거래순매수
    ndiffpro_trde_sel: str          # 비차익거래매도
    ndiffpro_trde_buy: str          # 비차익거래매수
    ndiffpro_trde_netprps: str      # 비차익거래순매수
    dfrt_trde_sell_qty: str         # 차익거래매도수량
    dfrt_trde_buy_qty: str          # 차익거래매수수량
    dfrt_trde_netprps_qty: str      # 차익거래순매수수량
    ndiffpro_trde_sell_qty: str     # 비차익거래매도수량
    ndiffpro_trde_buy_qty: str      # 비차익거래매수수량
    ndiffpro_trde_netprps_qty: str  # 비차익거래순매수수량
    all_sel: str                    # 전체매도
    all_buy: str                    # 전체매수
    all_netprps: str                # 전체순매수
    kospi200: str                   # KOSPI200
    basis: str                      # BASIS


@dataclass(frozen=True)
class ProgramTrend:
    """프로그램매매추이요청 응답 (ka90005, ka90010).

    Args:
        items: 프로그램매매추이 리스트.
    """

    items: list[ProgramTrendItem]


@dataclass(frozen=True)
class ProgramArbitrageBalItem:
    """프로그램매매차익잔고추이 단일 항목."""

    dt: str                         # 일자
    buy_dfrt_trde_qty: str          # 매수차익거래수량
    buy_dfrt_trde_amt: str          # 매수차익거래금액
    buy_dfrt_trde_irds_amt: str     # 매수차익거래증감액
    sel_dfrt_trde_qty: str          # 매도차익거래수량
    sel_dfrt_trde_amt: str          # 매도차익거래금액
    sel_dfrt_trde_irds_amt: str     # 매도차익거래증감액


@dataclass(frozen=True)
class ProgramArbitrageBal:
    """프로그램매매차익잔고추이요청 응답 (ka90006).

    Args:
        items: 프로그램매매차익잔고추이 리스트.
    """

    items: list[ProgramArbitrageBalItem]


@dataclass(frozen=True)
class ProgramAccTrendItem:
    """프로그램매매누적추이 단일 항목."""

    dt: str                 # 일자
    kospi200: str           # KOSPI200
    basis: str              # BASIS
    dfrt_trde_tdy: str      # 차익거래당일
    dfrt_trde_acc: str      # 차익거래누적
    ndiffpro_trde_tdy: str  # 비차익거래당일
    ndiffpro_trde_acc: str  # 비차익거래누적
    all_tdy: str            # 전체당일
    all_acc: str            # 전체누적


@dataclass(frozen=True)
class ProgramAccTrend:
    """프로그램매매누적추이요청 응답 (ka90007).

    Args:
        items: 프로그램매매누적추이 리스트.
    """

    items: list[ProgramAccTrendItem]


@dataclass(frozen=True)
class StockTimeProgramItem:
    """종목시간별프로그램매매추이 단일 항목."""

    tm: str                         # 시간
    cur_prc: str                    # 현재가
    pre_sig: str                    # 대비기호
    pred_pre: str                   # 전일대비
    flu_rt: str                     # 등락율
    trde_qty: str                   # 거래량
    prm_sell_amt: str               # 프로그램매도금액
    prm_buy_amt: str                # 프로그램매수금액
    prm_netprps_amt: str            # 프로그램순매수금액
    prm_netprps_amt_irds: str       # 프로그램순매수금액증감
    prm_sell_qty: str               # 프로그램매도수량
    prm_buy_qty: str                # 프로그램매수수량
    prm_netprps_qty: str            # 프로그램순매수수량
    prm_netprps_qty_irds: str       # 프로그램순매수수량증감
    base_pric_tm: str               # 기준가시간
    dbrt_trde_rpy_sum: str          # 대차거래상환주수합
    remn_rcvord_sum: str            # 잔고수주합
    stex_tp: str                    # 거래소구분


@dataclass(frozen=True)
class StockTimeProgram:
    """종목시간별프로그램매매추이요청 응답 (ka90008).

    Args:
        items: 종목시간별프로그램매매추이 리스트.
    """

    items: list[StockTimeProgramItem]


@dataclass(frozen=True)
class StockDailyProgramItem:
    """종목일별프로그램매매추이 단일 항목."""

    dt: str                         # 일자
    cur_prc: str                    # 현재가
    pre_sig: str                    # 대비기호
    pred_pre: str                   # 전일대비
    flu_rt: str                     # 등락율
    trde_qty: str                   # 거래량
    prm_sell_amt: str               # 프로그램매도금액
    prm_buy_amt: str                # 프로그램매수금액
    prm_netprps_amt: str            # 프로그램순매수금액
    prm_netprps_amt_irds: str       # 프로그램순매수금액증감
    prm_sell_qty: str               # 프로그램매도수량
    prm_buy_qty: str                # 프로그램매수수량
    prm_netprps_qty: str            # 프로그램순매수수량
    prm_netprps_qty_irds: str       # 프로그램순매수수량증감
    base_pric_tm: str               # 기준가시간
    dbrt_trde_rpy_sum: str          # 대차거래상환주수합
    remn_rcvord_sum: str            # 잔고수주합
    stex_tp: str                    # 거래소구분


@dataclass(frozen=True)
class StockDailyProgram:
    """종목일별프로그램매매추이요청 응답 (ka90013).

    Args:
        items: 종목일별프로그램매매추이 리스트.
    """

    items: list[StockDailyProgramItem]


# ============================================================
# 9단계 — 금현물 (ka50xxx, ka52xxx, kt50xxx)
# ============================================================

type GoldStockCode = Literal["M04020000", "M04020100"]
"""금현물 종목코드.

- ``"M04020000"``: 금 99.99_1kg
- ``"M04020100"``: 미니금 99.99_100g
"""

type GoldOrderTradeType = Literal["normal", "normal_ioc", "normal_fok"]
"""금현물 매매구분.

- ``"normal"``: 보통 (00)
- ``"normal_ioc"``: 보통(IOC) (10)
- ``"normal_fok"``: 보통(FOK) (20)
"""


# ── ka50010: 금현물체결추이 ───────────────────────────────────

@dataclass(frozen=True)
class GoldContractTrendItem:
    """금현물체결추이 단일 항목."""

    cntr_pric: str          # 체결가
    pred_pre: str           # 전일 대비
    flu_rt: str             # 등락율
    trde_qty: str           # 누적 거래량
    acc_trde_prica: str     # 누적 거래대금
    cntr_trde_qty: str      # 거래량(체결량)
    tm: str                 # 체결시간 (HHMMSS)
    pre_sig: str            # 전일대비기호
    pri_sel_bid_unit: str   # 매도호가
    pri_buy_bid_unit: str   # 매수호가
    trde_pre: str           # 전일 거래량 대비 비율
    trde_tern_rt: str       # 전일 거래량 대비 순간 거래량 비율
    cntr_str: str           # 체결강도


@dataclass(frozen=True)
class GoldContractTrend:
    """금현물체결추이요청 응답 (ka50010).

    Args:
        items: 금현물체결추이 리스트.
    """

    items: list[GoldContractTrendItem]


# ── ka50012: 금현물일별추이 ───────────────────────────────────

@dataclass(frozen=True)
class GoldDailyTrendItem:
    """금현물일별추이 단일 항목."""

    cur_prc: str        # 종가
    pred_pre: str       # 전일 대비
    flu_rt: str         # 등락율
    trde_qty: str       # 누적 거래량
    acc_trde_prica: str # 누적 거래대금 (백만)
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    dt: str             # 일자 (YYYYMMDD)
    pre_sig: str        # 전일대비기호
    orgn_netprps: str   # 기관 순매수 수량
    for_netprps: str    # 외국인 순매수 수량
    ind_netprps: str    # 순매매량(개인)


@dataclass(frozen=True)
class GoldDailyTrend:
    """금현물일별추이요청 응답 (ka50012).

    Args:
        items: 금현물일별추이 리스트.
    """

    items: list[GoldDailyTrendItem]


# ── ka50087: 금현물예상체결 ───────────────────────────────────

@dataclass(frozen=True)
class GoldExpectedContractItem:
    """금현물예상체결 단일 항목."""

    exp_cntr_pric: str      # 예상 체결가
    exp_pred_pre: str       # 예상 체결가 전일대비
    exp_flu_rt: str         # 예상 체결가 등락율
    exp_acc_trde_qty: str   # 예상 체결 수량(누적)
    exp_cntr_trde_qty: str  # 예상 체결 수량
    exp_tm: str             # 예상 체결 시간 (HHMMSS)
    exp_pre_sig: str        # 예상 체결가 전일대비기호
    stex_tp: str            # 거래소 구분


@dataclass(frozen=True)
class GoldExpectedContract:
    """금현물예상체결요청 응답 (ka50087).

    Args:
        items: 금현물예상체결 리스트.
    """

    items: list[GoldExpectedContractItem]


# ── ka50100: 금현물 시세정보 ─────────────────────────────────

@dataclass(frozen=True)
class GoldMarketInfo:
    """금현물 시세정보 응답 (ka50100)."""

    pred_pre_sig: str       # 전일대비기호
    pred_pre: str           # 전일대비
    flu_rt: str             # 등락율
    trde_qty: str           # 거래량
    open_pric: str          # 시가
    high_pric: str          # 고가
    low_pric: str           # 저가
    pred_rt: str            # 전일비
    upl_pric: str           # 상한가
    lst_pric: str           # 하한가
    pred_close_pric: str    # 전일종가


# ── ka50101: 금현물 호가 ──────────────────────────────────────

@dataclass(frozen=True)
class GoldBidItem:
    """금현물 호가 단일 항목."""

    cntr_pric: str          # 체결가
    pred_pre: str           # 전일 대비(원)
    flu_rt: str             # 등락율
    trde_qty: str           # 누적 거래량
    acc_trde_prica: str     # 누적 거래대금
    cntr_trde_qty: str      # 거래량(체결량)
    tm: str                 # 체결시간 (HHMMSS)
    pre_sig: str            # 전일대비기호
    pri_sel_bid_unit: str   # 매도호가
    pri_buy_bid_unit: str   # 매수호가
    trde_pre: str           # 전일 거래량 대비 비율
    trde_tern_rt: str       # 전일 거래량 대비 순간 거래량 비율
    cntr_str: str           # 체결강도
    lpmmcm_nm_1: str        # K.O 접근도
    stex_tp: str            # 거래소구분


@dataclass(frozen=True)
class GoldBid:
    """금현물 호가 응답 (ka50101).

    Args:
        items: 금현물 호가 리스트.
    """

    items: list[GoldBidItem]


# ── ka52301: 금현물투자자현황 ────────────────────────────────

@dataclass(frozen=True)
class GoldInvestorStatusItem:
    """금현물투자자현황 단일 항목."""

    stk_nm: str                     # 투자자 구분명
    stk_cd: str                     # 투자자 코드
    all_dfrt_trst_sell_qty: str     # 투자자별 매도 수량(천)
    sell_qty_irds: str              # 투자자별 매도 수량 증감(천)
    all_dfrt_trst_sell_amt: str     # 투자자별 매도 금액(억)
    sell_amt_irds: str              # 투자자별 매도 금액 증감(억)
    all_dfrt_trst_buy_qty: str      # 투자자별 매수 수량(천)
    buy_qty_irds: str               # 투자자별 매수 수량 증감(천)
    all_dfrt_trst_buy_amt: str      # 투자자별 매수 금액(억)
    buy_amt_irds: str               # 투자자별 매수 금액 증감(억)
    all_dfrt_trst_netprps_qty: str  # 투자자별 순매수 수량(천)
    netprps_qty_irds: str           # 투자자별 순매수 수량 증감(천)
    all_dfrt_trst_netprps_amt: str  # 투자자별 순매수 금액(억)
    netprps_amt_irds: str           # 투자자별 순매수 금액 증감(억)
    sell_uv: str                    # 투자자별 매도 단가
    buy_uv: str                     # 투자자별 매수 단가
    acc_netprps_amt: str            # 누적 순매수 금액(억)
    acc_netprps_qty: str            # 누적 순매수 수량(천)


@dataclass(frozen=True)
class GoldInvestorStatus:
    """금현물투자자현황 응답 (ka52301).

    Args:
        items: 투자자현황 리스트.
    """

    items: list[GoldInvestorStatusItem]


# ── ka50079: 금현물틱차트 ────────────────────────────────────

@dataclass(frozen=True)
class GoldTickChartItem:
    """금현물틱차트 단일 항목."""

    cur_prc: str        # 현재가
    pred_pre: str       # 전일대비
    trde_qty: str       # 거래량
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    cntr_tm: str        # 체결시간 (YYYYMMDDHHmmss)
    dt: str             # 일자
    pred_pre_sig: str   # 전일대비기호


@dataclass(frozen=True)
class GoldTickChart:
    """금현물틱차트조회요청 응답 (ka50079).

    Args:
        items: 금현물틱차트 리스트.
    """

    items: list[GoldTickChartItem]


# ── ka50080: 금현물분봉차트 ─────────────────────────────────

@dataclass(frozen=True)
class GoldMinuteChartItem:
    """금현물분봉차트 단일 항목."""

    cur_prc: str        # 현재가
    pred_pre: str       # 전일대비
    acc_trde_qty: str   # 누적거래량
    trde_qty: str       # 거래량
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    cntr_tm: str        # 체결시간 (YYYYMMDDHHmmss)
    dt: str             # 일자
    pred_pre_sig: str   # 전일대비기호


@dataclass(frozen=True)
class GoldMinuteChart:
    """금현물분봉차트조회요청 응답 (ka50080).

    Args:
        items: 금현물분봉차트 리스트.
    """

    items: list[GoldMinuteChartItem]


# ── ka50081: 금현물일봉차트 ─────────────────────────────────

@dataclass(frozen=True)
class GoldDailyChartItem:
    """금현물일봉차트 단일 항목."""

    cur_prc: str        # 현재가(종가)
    acc_trde_qty: str   # 누적 거래량
    acc_trde_prica: str # 누적 거래대금
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    dt: str             # 일자 (YYYYMMDD)
    pred_pre_sig: str   # 전일대비기호


@dataclass(frozen=True)
class GoldDailyChart:
    """금현물일봉차트조회요청 응답 (ka50081).

    Args:
        items: 금현물일봉차트 리스트.
    """

    items: list[GoldDailyChartItem]


# ── ka50082: 금현물주봉차트 ─────────────────────────────────

@dataclass(frozen=True)
class GoldWeeklyChartItem:
    """금현물주봉차트 단일 항목."""

    cur_prc: str        # 현재가(종가)
    acc_trde_qty: str   # 누적 거래량
    acc_trde_prica: str # 누적 거래대금
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    dt: str             # 일자 (YYYYMMDDHHmmss)


@dataclass(frozen=True)
class GoldWeeklyChart:
    """금현물주봉차트조회요청 응답 (ka50082).

    Args:
        items: 금현물주봉차트 리스트.
    """

    items: list[GoldWeeklyChartItem]


# ── ka50083: 금현물월봉차트 ─────────────────────────────────

@dataclass(frozen=True)
class GoldMonthlyChartItem:
    """금현물월봉차트 단일 항목."""

    cur_prc: str        # 현재가(종가)
    acc_trde_qty: str   # 누적 거래량
    acc_trde_prica: str # 누적 거래대금
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    dt: str             # 일자 (YYYYMMDDHHmmss)


@dataclass(frozen=True)
class GoldMonthlyChart:
    """금현물월봉차트조회요청 응답 (ka50083).

    Args:
        items: 금현물월봉차트 리스트.
    """

    items: list[GoldMonthlyChartItem]


# ── ka50091: 금현물당일틱차트 ───────────────────────────────

@dataclass(frozen=True)
class GoldDailyTickChartItem:
    """금현물당일틱차트 단일 항목."""

    cntr_pric: str      # 체결가
    pred_pre: str       # 전일 대비(원)
    trde_qty: str       # 거래량(체결량)
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    cntr_tm: str        # 체결시간 (YYYYMMDDHHmmss)
    dt: str             # 일자
    pred_pre_sig: str   # 전일대비기호


@dataclass(frozen=True)
class GoldDailyTickChart:
    """금현물당일틱차트조회요청 응답 (ka50091).

    Args:
        items: 금현물당일틱차트 리스트.
    """

    items: list[GoldDailyTickChartItem]


# ── ka50092: 금현물당일분봉차트 ─────────────────────────────

@dataclass(frozen=True)
class GoldDailyMinuteChartItem:
    """금현물당일분봉차트 단일 항목."""

    cntr_pric: str      # 체결가
    pred_pre: str       # 전일 대비(원)
    acc_trde_qty: str   # 누적 거래량
    acc_trde_prica: str # 누적 거래대금
    trde_qty: str       # 거래량(체결량)
    open_pric: str      # 시가
    high_pric: str      # 고가
    low_pric: str       # 저가
    cntr_tm: str        # 체결시간 (YYYYMMDDHHmmss)
    dt: str             # 일자
    pred_pre_sig: str   # 전일대비기호


@dataclass(frozen=True)
class GoldDailyMinuteChart:
    """금현물당일분봉차트조회요청 응답 (ka50092).

    Args:
        items: 금현물당일분봉차트 리스트.
    """

    items: list[GoldDailyMinuteChartItem]


# ── kt50000/kt50001: 금현물 매수/매도주문 응답 ───────────────

@dataclass(frozen=True)
class GoldOrderResponse:
    """금현물 매수/매도주문 응답 (kt50000, kt50001).

    Args:
        ord_no: 주문번호.
    """

    ord_no: str     # 주문번호


# ── kt50002: 금현물 정정주문 응답 ────────────────────────────

@dataclass(frozen=True)
class GoldModifyOrderResponse:
    """금현물 정정주문 응답 (kt50002).

    Args:
        ord_no: 주문번호.
        base_orig_ord_no: 모주문번호.
        mdfy_qty: 정정수량.
    """

    ord_no: str             # 주문번호
    base_orig_ord_no: str   # 모주문번호
    mdfy_qty: str           # 정정수량


# ── kt50003: 금현물 취소주문 응답 ────────────────────────────

@dataclass(frozen=True)
class GoldCancelOrderResponse:
    """금현물 취소주문 응답 (kt50003).

    Args:
        ord_no: 주문번호.
        base_orig_ord_no: 모주문번호.
        cncl_qty: 취소수량.
    """

    ord_no: str             # 주문번호
    base_orig_ord_no: str   # 모주문번호
    cncl_qty: str           # 취소수량


# ── kt50020: 금현물 잔고확인 ─────────────────────────────────

@dataclass(frozen=True)
class GoldBalanceItem:
    """금현물계좌평가현황 단일 항목."""

    stk_cd: str         # 종목코드
    stk_nm: str         # 종목명
    real_qty: str       # 보유수량
    avg_prc: str        # 평균단가
    cur_prc: str        # 현재가
    est_amt: str        # 평가금액
    est_lspft: str      # 손익금액
    est_ratio: str      # 손익율 (단위: %)
    cmsn: str           # 수수료
    vlad_tax: str       # 부가가치세
    book_amt2: str      # 매입금액
    pl_prch_prc: str    # 손익분기매입가
    qty: str            # 결제잔고
    buy_qty: str        # 매수수량
    sell_qty: str       # 매도수량
    able_qty: str       # 가능수량


@dataclass(frozen=True)
class GoldBalance:
    """금현물 잔고확인 응답 (kt50020).

    Args:
        tot_entr: 예수금.
        net_entr: 추정예수금.
        tot_est_amt: 잔고평가액.
        net_amt: 예탁자산평가액.
        tot_book_amt2: 총매입금액.
        tot_dep_amt: 추정예탁자산.
        paym_alowa: 출금가능금액.
        pl_amt: 실현손익.
        items: 금현물계좌평가현황 리스트.
    """

    tot_entr: str           # 예수금
    net_entr: str           # 추정예수금
    tot_est_amt: str        # 잔고평가액
    net_amt: str            # 예탁자산평가액
    tot_book_amt2: str      # 총매입금액
    tot_dep_amt: str        # 추정예탁자산
    paym_alowa: str         # 출금가능금액
    pl_amt: str             # 실현손익
    items: list[GoldBalanceItem]


# ── kt50021: 금현물 예수금 ───────────────────────────────────

@dataclass(frozen=True)
class GoldDeposit:
    """금현물 예수금 응답 (kt50021)."""

    entra: str              # 예수금
    profa_ch: str           # 증거금현금
    chck_ina_amt: str       # 수표입금액
    etc_loan: str           # 기타대여금
    etc_loan_dlfe: str      # 기타대여금연체료
    etc_loan_tot: str       # 기타대여금합계
    prsm_entra: str         # 추정예수금
    buy_exct_amt: str       # 매수정산금
    sell_exct_amt: str      # 매도정산금
    sell_buy_exct_amt: str  # 매도매수정산금
    dly_amt: str            # 미수변제소요금
    prsm_pymn_alow_amt: str # 추정출금가능금액
    pymn_alow_amt: str      # 출금가능금액
    ord_alow_amt: str       # 주문가능금액


# ── kt50030: 금현물 주문체결전체조회 ────────────────────────

@dataclass(frozen=True)
class GoldOrderStatusItem:
    """금현물 주문체결전체조회 단일 항목."""

    stk_bond_tp: str        # 주식채권구분
    ord_no: str             # 주문번호
    stk_cd: str             # 상품코드
    trde_tp: str            # 매매구분
    io_tp_nm: str           # 주문유형구분
    ord_qty: str            # 주문수량
    ord_uv: str             # 주문단가
    cnfm_qty: str           # 확인수량
    data_send_end_tp: str   # 접수구분
    mrkt_deal_tp: str       # 시장구분
    rsrv_tp: str            # 예약/반대여부
    orig_ord_no: str        # 원주문번호
    stk_nm: str             # 종목명
    dcd_tp_nm: str          # 결제구분
    crd_deal_tp: str        # 신용거래구분
    cntr_qty: str           # 체결수량
    cntr_uv: str            # 체결단가
    ord_remnq: str          # 미체결수량
    comm_ord_tp: str        # 통신구분
    mdfy_cncl_tp: str       # 정정취소구분
    dmst_stex_tp: str       # 국내거래소구분
    cond_uv: str            # 스톱가


@dataclass(frozen=True)
class GoldOrderStatus:
    """금현물 주문체결전체조회 응답 (kt50030).

    Args:
        items: 계좌별주문체결현황 리스트.
    """

    items: list[GoldOrderStatusItem]


# ── kt50031: 금현물 주문체결조회 ────────────────────────────

@dataclass(frozen=True)
class GoldOrderDetailItem:
    """금현물 주문체결조회 단일 항목."""

    ord_no: str         # 주문번호
    stk_cd: str         # 종목번호
    trde_tp: str        # 매매구분
    crd_tp: str         # 신용구분
    ord_qty: str        # 주문수량
    ord_uv: str         # 주문단가
    cnfm_qty: str       # 확인수량
    acpt_tp: str        # 접수구분
    rsrv_tp: str        # 반대여부
    ord_tm: str         # 주문시간
    ori_ord: str        # 원주문
    stk_nm: str         # 종목명
    io_tp_nm: str       # 주문구분
    loan_dt: str        # 대출일
    cntr_qty: str       # 체결수량
    cntr_uv: str        # 체결단가
    ord_remnq: str      # 주문잔량
    comm_ord_tp: str    # 통신구분
    mdfy_cncl: str      # 정정취소
    cnfm_tm: str        # 확인시간
    dmst_stex_tp: str   # 국내거래소구분
    cond_uv: str        # 스톱가


@dataclass(frozen=True)
class GoldOrderDetail:
    """금현물 주문체결조회 응답 (kt50031).

    Args:
        items: 계좌별주문체결내역상세 리스트.
    """

    items: list[GoldOrderDetailItem]


# ── kt50032: 금현물 거래내역조회 ────────────────────────────

@dataclass(frozen=True)
class GoldTradeHistoryItem:
    """금현물 거래내역조회 단일 항목."""

    deal_dt: str            # 거래일자
    deal_no: str            # 거래번호
    rmrk_nm: str            # 적요명
    deal_qty: str           # 거래수량
    gold_spot_vat: str      # 금현물부가가치세
    exct_amt: str           # 정산금액
    dly_sum: str            # 연체합
    entra_remn: str         # 예수금잔고
    mdia_nm: str            # 매체구분명
    orig_deal_no: str       # 원거래번호
    stk_nm: str             # 종목명
    uv_exrt: str            # 거래단가
    cmsn: str               # 수수료
    uncl_ocr: str           # 미수(원/g)
    rpym_sum: str           # 변제합
    spot_remn: str          # 현물잔고
    proc_time: str          # 처리시간
    rcpy_no: str            # 출납번호
    stk_cd: str             # 종목코드
    deal_amt: str           # 거래금액
    tax_tot_amt: str        # 소득/주민세
    cntr_dt: str            # 체결일
    proc_brch_nm: str       # 처리점
    prcsr: str              # 처리자


@dataclass(frozen=True)
class GoldTradeHistory:
    """금현물 거래내역조회 응답 (kt50032).

    Args:
        acnt_print: 계좌번호 출력용.
        items: 금현물거래내역 리스트.
    """

    acnt_print: str
    items: list[GoldTradeHistoryItem]


# ── kt50075: 금현물 미체결조회 ───────────────────────────────

@dataclass(frozen=True)
class GoldUnfilledItem:
    """금현물 미체결조회 단일 항목."""

    stk_bond_tp: str        # 주식채권구분
    ord_no: str             # 주문번호
    stk_cd: str             # 상품코드
    trde_tp: str            # 매매구분
    io_tp_nm: str           # 주문유형구분
    ord_qty: str            # 주문수량
    ord_uv: str             # 주문단가
    cnfm_qty: str           # 확인수량
    data_send_end_tp: str   # 접수구분
    mrkt_deal_tp: str       # 시장구분
    rsrv_tp: str            # 예약/반대여부
    orig_ord_no: str        # 원주문번호
    stk_nm: str             # 종목명
    dcd_tp_nm: str          # 결제구분
    crd_deal_tp: str        # 신용거래구분
    cntr_qty: str           # 체결수량
    cntr_uv: str            # 체결단가
    ord_remnq: str          # 미체결수량
    comm_ord_tp: str        # 통신구분
    mdfy_cncl_tp: str       # 정정취소구분
    dmst_stex_tp: str       # 국내거래소구분
    cond_uv: str            # 스톱가


@dataclass(frozen=True)
class GoldUnfilled:
    """금현물 미체결조회 응답 (kt50075).

    Args:
        items: 계좌별주문미체결현황 리스트.
    """

    items: list[GoldUnfilledItem]


# ============================================================
# 10단계 — 조건검색 (ka10171 ~ ka10174)
# ============================================================

# ── ka10171: 조건검색 목록조회 ──────────────────────────────

@dataclass(frozen=True)
class ConditionItem:
    """조건검색식 단일 항목.

    Args:
        seq: 조건검색식 일련번호.
        name: 조건검색식 이름.
    """

    seq: str    # 조건검색식 일련번호
    name: str   # 조건검색식 이름


@dataclass(frozen=True)
class ConditionList:
    """조건검색 목록조회 응답 (ka10171).

    Args:
        items: 조건검색식 목록.
    """

    items: list[ConditionItem]


# ── ka10172: 조건검색 요청 일반 ─────────────────────────────

@dataclass(frozen=True)
class ConditionSearchItem:
    """조건검색 결과 단일 종목 항목.

    Args:
        stock_code: 종목코드 (예: ``"A005930"``).
        stock_name: 종목명.
        current_price: 현재가.
        change_sign: 전일대비기호.
        change: 전일대비.
        change_rate: 등락율.
        volume: 누적거래량.
        open_price: 시가.
        high_price: 고가.
        low_price: 저가.
    """

    stock_code: str     # 종목코드 (9001)
    stock_name: str     # 종목명 (302)
    current_price: str  # 현재가 (10)
    change_sign: str    # 전일대비기호 (25)
    change: str         # 전일대비 (11)
    change_rate: str    # 등락율 (12)
    volume: str         # 누적거래량 (13)
    open_price: str     # 시가 (16)
    high_price: str     # 고가 (17)
    low_price: str      # 저가 (18)


@dataclass(frozen=True)
class ConditionSearchResult:
    """조건검색 요청 일반 응답 (ka10172).

    Args:
        seq: 조건검색식 일련번호.
        cont_yn: 연속조회 여부 (``"Y"`` / ``"N"``).
        next_key: 연속조회키.
        items: 검색 결과 종목 리스트.
    """

    seq: str
    cont_yn: str
    next_key: str
    items: list[ConditionSearchItem]


# ── ka10173: 조건검색 요청 실시간 ───────────────────────────

@dataclass(frozen=True)
class ConditionRealtimeValues:
    """조건검색 실시간 단일 이벤트 값.

    Args:
        serial: 일련번호 (841).
        stock_code: 종목코드 (9001).
        insert_delete: 삽입삭제 구분 — ``"I"`` (삽입) / ``"D"`` (삭제) (843).
        exec_time: 체결시간 (20).
        sell_buy: 매도수 구분 (907).
    """

    serial: str         # 일련번호 (841)
    stock_code: str     # 종목코드 (9001)
    insert_delete: str  # 삽입삭제 구분 I:삽입 D:삭제 (843)
    exec_time: str      # 체결시간 (20)
    sell_buy: str       # 매도/수 구분 (907)


@dataclass(frozen=True)
class ConditionRealtimeItem:
    """조건검색 실시간 단일 이벤트.

    Args:
        type: 실시간 항목 TR명 (예: ``"0B"``).
        name: 실시간 항목명.
        item: 종목코드.
        values: 실시간 수신 값.
    """

    type: str                       # 실시간 항목 TR명
    name: str                       # 실시간 항목명
    item: str                       # 종목코드
    values: ConditionRealtimeValues  # 실시간 수신 값


# ── ka10174: 조건검색 실시간 해제 ───────────────────────────

@dataclass(frozen=True)
class ConditionStopResult:
    """조건검색 실시간 해제 응답 (ka10174).

    Args:
        seq: 해제된 조건검색식 일련번호.
    """

    seq: str  # 해제된 조건검색식 일련번호


# ============================================================
# 11단계 — 신용주문 관련 종목정보 (kt20xxx)
# ============================================================

type CreditStockGradeType = Literal["%", "A", "B", "C", "D", "E"]
"""신용종목등급구분.

- ``"%"``: 전체
- ``"A"`` ~ ``"E"``: 각 등급
"""

type CreditMarketType = Literal["%", "1", "0"]
"""신용융자 시장거래구분.

- ``"%"``: 전체
- ``"1"``: 코스피
- ``"0"``: 코스닥
"""

# ── kt20016: 신용융자 가능종목요청 ───────────────────────────

@dataclass(frozen=True)
class CreditLoanStockItem:
    """신용융자 가능종목 단일 항목.

    Args:
        stk_cd: 종목코드.
        stk_nm: 종목명.
        crd_assr_rt: 신용보증금율.
        repl_pric: 대용가.
        pred_close_pric: 전일종가.
        crd_limit_over_yn: 신용한도초과여부.
        crd_limit_over_txt: 신용한도초과 텍스트 (``"N"``: 공란, ``"Y"``: 회사한도 초과).
    """

    stk_cd: str             # 종목코드
    stk_nm: str             # 종목명
    crd_assr_rt: str        # 신용보증금율
    repl_pric: str          # 대용가
    pred_close_pric: str    # 전일종가
    crd_limit_over_yn: str  # 신용한도초과여부
    crd_limit_over_txt: str # 신용한도초과 텍스트


@dataclass(frozen=True)
class CreditLoanStocks:
    """신용융자 가능종목요청 응답 (kt20016).

    Args:
        crd_loan_able: 신용융자가능여부 안내 문자열.
        items: 신용융자 가능종목 리스트.
    """

    crd_loan_able: str
    items: list[CreditLoanStockItem]


# ── kt20017: 신용융자 가능문의 ───────────────────────────────

@dataclass(frozen=True)
class CreditLoanAvailability:
    """신용융자 가능문의 응답 (kt20017).

    Args:
        crd_alow_yn: 신용가능여부 안내 문자열 (예: ``"< A군 신용융자 가능 >"``).
    """

    crd_alow_yn: str  # 신용가능여부


# ============================================================
# 12단계 — 실시간 WebSocket
# ============================================================

type RealtimeType = Literal[
    "00", "04",
    "0A", "0B", "0C", "0D", "0E", "0F", "0G", "0H", "0I",
    "0J", "0U",
    "0g", "0m", "0s", "0u", "0w",
    "1h",
]
"""실시간 수신 TR 타입.

- ``"00"``: 주문체결
- ``"04"``: 잔고
- ``"0A"``: 주식기세
- ``"0B"``: 주식체결
- ``"0C"``: 주식우선호가
- ``"0D"``: 주식호가잔량
- ``"0E"``: 주식시간외호가
- ``"0F"``: 주식당일거래원
- ``"0G"``: ETF NAV
- ``"0H"``: 주식예상체결
- ``"0I"``: 국제금환산가격
- ``"0J"``: 업종지수
- ``"0U"``: 업종등락
- ``"0g"``: 주식종목정보
- ``"0m"``: ELW 이론가
- ``"0s"``: 장시작시간
- ``"0u"``: ELW 지표
- ``"0w"``: 종목프로그램매매
- ``"1h"``: VI발동/해제
"""


@dataclass(frozen=True)
class RealtimeEvent:
    """실시간 WebSocket 수신 이벤트.

    서버에서 ``trnm="REAL"`` 메시지가 수신될 때 data 배열의 각 항목을 이 dataclass로 파싱한다.

    Args:
        type: 실시간 항목 TR명. (예: ``"0B"``, ``"00"``)
        name: 실시간 항목명. (예: ``"주식체결"``, ``"주문체결"``)
        item: 종목코드 또는 item 식별자. 계좌 기반 타입(``"00"``, ``"04"``)은 빈 문자열.
        values: 필드번호 → 값 딕셔너리. (예: ``{"10": "+60700", "20": "165208"}``)

    Example:
        >>> event.values.get("10", "")   # 현재가
        '+60700'
        >>> event.values.get("20", "")   # 체결시간
        '165208'
    """

    type: str               # 실시간 항목 TR명 (예: "0B")
    name: str               # 실시간 항목명 (예: "주식체결")
    item: str               # 종목코드 (없으면 "")
    values: dict[str, str]  # 필드번호 → 값 (예: {"10": "+60700", ...})
