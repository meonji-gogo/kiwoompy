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
