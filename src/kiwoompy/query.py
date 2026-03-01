"""조회 모듈 — 계좌·잔고·손익·주문체결·시세·종목정보·순위정보·차트·업종·기관/외국인·공매도·대차거래·ETF·ELW·테마·프로그램매매 조회."""

from __future__ import annotations

from typing import Literal

from kiwoompy.api import KiwoomApi
from kiwoompy.exceptions import KiwoomApiError
from kiwoompy.models import (
    AllSectorIndex,
    AllSectorIndexItem,
    ForeignTrade,
    ForeignTradeItem,
    InstFrgnConsecutiveItem,
    InstFrgnConsecutiveTrade,
    InstitutionTrade,
    SectorDailyPrice,
    SectorDailyPriceItem,
    SectorInvestorNetBuy,
    SectorInvestorNetBuyItem,
    SectorPrice,
    SectorPriceTmItem,
    SectorProgram,
    SectorStockPriceItem,
    SectorStockPrices,
    ShortSellItem,
    ShortSellTrend,
    StockLoanByStock,
    StockLoanByStockItem,
    StockLoanHistory,
    StockLoanHistoryItem,
    StockLoanItem,
    StockLoanTop10,
    StockLoanTop10Item,
    StockLoanTrend,
    ElwAccessRate,
    ElwAccessRateItem,
    ElwBalRank,
    ElwBalRankItem,
    ElwBrokerNetTrade,
    ElwBrokerNetTradeItem,
    ElwDailySens,
    ElwDailySensItem,
    ElwDetail,
    ElwFlucRank,
    ElwFlucRankItem,
    ElwGap,
    ElwGapItem,
    ElwLpDaily,
    ElwLpDailyItem,
    ElwPriceSurge,
    ElwPriceSurgeItem,
    ElwSearch,
    ElwSearchItem,
    ElwSens,
    ElwSensItem,
    EtfAllQuote,
    EtfAllQuoteItem,
    EtfDailyFill,
    EtfDailyFillItem,
    EtfDailyTrend,
    EtfDailyTrendItem,
    EtfInfo,
    EtfNav,
    EtfNavItem,
    EtfReturn,
    EtfReturnItem,
    EtfTimeFill,
    EtfTimeFillItem,
    EtfTimeTrend,
    EtfTimeTrendItem,
    EtfTimeTrend2,
    EtfTimeTrend2Item,
    ProgramAccTrend,
    ProgramAccTrendItem,
    ProgramArbitrageBal,
    ProgramArbitrageBalItem,
    ProgramTop50,
    ProgramTop50Item,
    ProgramTrend,
    ProgramTrendItem,
    StockDailyProgram,
    StockDailyProgramItem,
    StockProgramStatus,
    StockProgramStatusItem,
    StockTimeProgram,
    StockTimeProgramItem,
    ThemeGroup,
    ThemeGroupItem,
    ThemeStockItem,
    ThemeStocks,
    AfterHoursRank,
    AfterHoursRankItem,
    BidQtySurge,
    InvestorChart,
    InvestorChartItem,
    IntraInvestorChart,
    IntraInvestorChartItem,
    SectorCandleItem,
    SectorDayChart,
    SectorDayChartItem,
    SectorMinChart,
    SectorMinChartItem,
    SectorMonthChart,
    SectorTickChart,
    SectorWeekChart,
    SectorYearChart,
    StockCandleItem,
    StockDayChart,
    StockDayChartItem,
    StockMinChart,
    StockMinChartItem,
    StockMonthChart,
    StockMonthChartItem,
    StockTickChart,
    StockWeekChart,
    StockWeekChartItem,
    StockYearChart,
    StockYearChartItem,
    BidQtySurgeItem,
    BidQtyUpper,
    BidQtyUpperItem,
    BrokerTradeUpper,
    BrokerTradeUpperItem,
    CreditRatioUpper,
    CreditRatioUpperItem,
    DailyMainBroker,
    DailyMainBrokerEntry,
    DailyTopExit,
    DailyTopExitItem,
    DailyTradeQtyUpper,
    DailyTradeQtyUpperItem,
    ExpectedTradeUpper,
    ExpectedTradeUpperItem,
    ForeignBrokerTradeUpper,
    ForeignBrokerTradeUpperItem,
    ForeignConsecTradeUpper,
    ForeignConsecTradeUpperItem,
    ForeignInstitutionTradeUpper,
    ForeignInstitutionTradeUpperItem,
    ForeignLimitExhaustUpper,
    ForeignLimitExhaustUpperItem,
    ForeignPeriodTradeUpper,
    ForeignPeriodTradeUpperItem,
    InvestorTradeUpper,
    InvestorTradeUpperItem,
    NetBuyBrokerRank,
    NetBuyBrokerRankItem,
    PriceChangeUpper,
    PriceChangeUpperItem,
    PrevTradeQtyUpper,
    PrevTradeQtyUpperItem,
    QtyRatioSurge,
    QtyRatioSurgeItem,
    SameNetTradeRank,
    SameNetTradeRankItem,
    StockBrokerRank,
    StockBrokerRankItem,
    TradeAmtUpper,
    TradeAmtUpperItem,
    TradeQtySurge,
    TradeQtySurgeItem,
    AccountBalance,
    AccountEvaluation,
    AccountEvaluationItem,
    AccountNumbers,
    AccountReturnItem,
    AfterCloseInvestorItem,
    AfterCloseInvestorTrading,
    AfterhoursOrderbook,
    BrokerInstantVolume,
    BrokerInstantVolumeItem,
    BrokerItem,
    BrokerList,
    BrokerStockTrend,
    BrokerStockTrendItem,
    BrokerSupplyAnalysis,
    BrokerSupplyItem,
    CreditOrderableQuantity,
    CreditTradingItem,
    CreditTradingTrend,
    DailyAccountReturn,
    DailyAccountStatus,
    DailyBalanceReturn,
    DailyBalanceReturnItem,
    DailyInstitutionStockItem,
    DailyInstitutionStocks,
    DailyPriceItem,
    DailyPrices,
    DailyRealizedProfit,
    DailyRealizedProfitDetail,
    DailyRealizedProfitDetailItem,
    DailyRealizedProfitItem,
    DailyTradeJournal,
    DailyTradeJournalItem,
    DailyTradingDetail,
    DailyTradingDetailItem,
    DepositDetail,
    DailyEstimatedAssetItem,
    EstimatedAsset,
    ExecutionBalance,
    ExecutionBalanceItem,
    ExecutionInfo,
    ExecutionInfoItem,
    ExecutionStrength,
    ExecutionStrengthItem,
    FilledOrderItem,
    FxDepositItem,
    HighLowPER,
    HighLowPERItem,
    HighLowStockItem,
    HighLowStocks,
    HoldingItem,
    IntradayInvestorItem,
    IntradayInvestorTrading,
    InvestorDailyStockItem,
    InvestorDailyStocks,
    LimitStockItem,
    LimitStocks,
    MarginDetail,
    MarketSummary,
    NearHighLow,
    NearHighLowItem,
    NewStockRightsItem,
    NewStockRightsPrices,
    NextDaySettlement,
    NextDaySettlementItem,
    OpenPriceChange,
    OpenPriceChangeItem,
    OrderableAmount,
    OrderableQuantity,
    OrderbookLevel,
    Orderbook,
    OrderExecutionStatus,
    OrderExecutionStatusItem,
    OrderHistoryDetailItem,
    PriceSurgeItem,
    PriceSurgeStocks,
    RealizedProfitByDateItem,
    RealizedProfitByPeriodItem,
    SectorItem,
    SectorList,
    SplitOrderDetailItem,
    StockBrokers,
    StockDetail,
    StockInfo,
    StockInstitutionTrend,
    StockInstitutionTrendItem,
    StockInvestorByDay,
    StockInvestorItem,
    StockInvestorTotal,
    StockList,
    StockListItem,
    StockMinutes,
    StockPeriodItem,
    StockPeriods,
    SupplyConcentration,
    SupplyConcentrationItem,
    TodayPrevExecution,
    TodayPrevExecutionItem,
    TodayPrevExecutionQty,
    TodayPrevExecutionQtyItem,
    TransactionHistoryItem,
    UnfilledOrderItem,
    VIStockItem,
    VIStocks,
    VolumeUpdatedItem,
    VolumeUpdatedStocks,
    WatchlistInfo,
    WatchlistStockItem,
    BrokerEntry,
    GoldBid,
    GoldBidItem,
    GoldContractTrend,
    GoldContractTrendItem,
    GoldDailyChart,
    GoldDailyChartItem,
    GoldDailyMinuteChart,
    GoldDailyMinuteChartItem,
    GoldDailyTickChart,
    GoldDailyTickChartItem,
    GoldDailyTrend,
    GoldDailyTrendItem,
    GoldExpectedContract,
    GoldExpectedContractItem,
    GoldInvestorStatus,
    GoldInvestorStatusItem,
    GoldMarketInfo,
    GoldMinuteChart,
    GoldMinuteChartItem,
    GoldMonthlyChart,
    GoldMonthlyChartItem,
    GoldStockCode,
    GoldTickChart,
    GoldTickChartItem,
    GoldWeeklyChart,
    GoldWeeklyChartItem,
    CreditLoanAvailability,
    CreditLoanStockItem,
    CreditLoanStocks,
    CreditMarketType,
    CreditStockGradeType,
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

# ---------------------------------------------------------------------------
# 4단계 매핑 테이블
# ---------------------------------------------------------------------------

_DISPLAY_TYPE_CODE: dict[str, str] = {
    "qty":    "0",
    "amount": "1",
}
_NEW_STOCK_RIGHTS_CODE: dict[str, str] = {
    "all":          "00",
    "rights_cert":  "05",
    "rights_deed":  "07",
}
_INSTITUTION_TRADE_CODE: dict[str, str] = {
    "sell": "1",
    "buy":  "2",
}
_ESTIMATED_PRICE_CODE: dict[str, str] = {
    "buy":  "1",
    "sell": "2",
}
_CREDIT_QUERY_CODE: dict[str, str] = {
    "loan":  "1",
    "short": "2",
}
_HIGH_LOW_SELECT_CODE: dict[str, str] = {
    "high": "1",
    "low":  "2",
}
_PER_TYPE_CODE: dict[str, str] = {
    "low_pbr":  "1",
    "high_pbr": "2",
    "low_per":  "3",
    "high_per": "4",
    "low_roe":  "5",
    "high_roe": "6",
}
_TODAY_PREV_CODE: dict[str, str] = {
    "today": "1",
    "prev":  "2",
}
_TICK_MIN_CODE: dict[str, str] = {
    "tick":   "0",
    "minute": "1",
}
_STK_MARKET_CODE: dict[str, str] = {
    "kospi":       "0",
    "kosdaq":      "10",
    "kotc":        "30",
    "konex":       "50",
    "etn":         "60",
    "loss_etn":    "70",
    "gold":        "80",
    "vol_etn":     "90",
    "infra":       "2",
    "elw":         "3",
    "mutual_fund": "4",
    "rights":      "5",
    "reit":        "6",
    "rights_deed": "7",
    "etf":         "8",
    "high_yield":  "9",
}
_SECTOR_MARKET_CODE: dict[str, str] = {
    "kospi":    "0",
    "kosdaq":   "1",
    "kospi200": "2",
    "kospi100": "4",
    "krx100":   "7",
}
_MRKCOND_EXCHANGE_CODE: dict[str, str] = {
    "krx": "1",
    "nxt": "2",
    "all": "3",
}
_MRKT_TYPE3_CODE: dict[str, str] = {
    "all":    "000",
    "kospi":  "001",
    "kosdaq": "101",
}
_MRKT_TYPE3_EXT_CODE: dict[str, str] = {
    "all":      "000",
    "kospi":    "001",
    "kosdaq":   "101",
    "kospi200": "201",
}
_INTRA_AMT_QTY_CODE: dict[str, str] = {
    "amount_qty": "1",
}
_AFTER_AMT_QTY_CODE: dict[str, str] = {
    "amount": "1",
    "qty":    "2",
}
_AFTER_TRADE_TYPE_CODE: dict[str, str] = {
    "net_buy": "0",
    "buy":     "1",
    "sell":    "2",
}
_INVESTOR_CODE: dict[str, str] = {
    "foreign":    "6",
    "institution": "7",
    "trust":       "1",
    "insurance":   "0",
    "bank":        "2",
    "pension":     "3",
    "gov":         "4",
    "other_corp":  "5",
}
_INVESTOR2_CODE: dict[str, str] = {
    "individual":   "8000",
    "foreign":      "9000",
    "financial_inv": "1000",
    "trust":        "3000",
    "private_fund": "3100",
    "other_fin":    "5000",
    "bank":         "4000",
    "insurance":    "2000",
    "pension":      "6000",
    "gov":          "7000",
    "other_corp":   "7100",
    "institution":  "9999",
}
_AMT_QTY_CODE: dict[str, str] = {
    "amount": "1",
    "qty":    "2",
}
_INVESTOR_TRADE_CODE: dict[str, str] = {
    "net_buy": "0",
    "buy":     "1",
    "sell":    "2",
}
_UNIT_CODE: dict[str, str] = {
    "thousand": "1000",
    "single":   "1",
}

# ---------------------------------------------------------------------------
# 5단계 매핑 테이블 — 순위정보
# ---------------------------------------------------------------------------

_RKINFO_MARKET_CODE: dict[str, str] = {
    "all":    "000",
    "kospi":  "001",
    "kosdaq": "101",
}
_RKINFO_STEX_CODE: dict[str, str] = {
    "krx": "1",
    "nxt": "2",
    "all": "3",
}
_RKINFO_BID_SORT_CODE: dict[str, str] = {
    "net_buy_qty":  "1",
    "net_sell_qty": "2",
    "buy_ratio":    "3",
    "sell_ratio":   "4",
}
_RKINFO_SURGE_SORT2_CODE: dict[str, str] = {
    "surge_qty":   "1",
    "surge_ratio": "2",
}
_RKINFO_PRICE_CHANGE_SORT_CODE: dict[str, str] = {
    "rise_ratio": "1",
    "rise_gap":   "2",
    "fall_ratio": "3",
    "fall_gap":   "4",
    "flat":       "5",
}
_RKINFO_BASE_DATE_CODE: dict[str, str] = {
    "today": "0",
    "prev":  "1",
}
_RKINFO_SORT_CND_CODE: dict[str, str] = {
    "qty":    "1",
    "amount": "2",
}
_RKINFO_BID_TRADE_CODE: dict[str, str] = {
    "buy":  "1",
    "sell": "2",
}
_RKINFO_ORG_TYPE_CODE: dict[str, str] = {
    "foreign":      "9000",
    "foreign_corp": "9100",
    "financial_inv":"1000",
    "trust":        "3000",
    "other_finance":"5000",
    "bank":         "4000",
    "insurance":    "2000",
    "pension":      "6000",
    "gov":          "7000",
    "other_corp":   "7100",
    "institution":  "9999",
}

# ---------------------------------------------------------------------------
# 6단계 매핑 테이블 — 차트
# ---------------------------------------------------------------------------
_CHART_ADJ_CODE: dict[str, str] = {
    "adjusted": "1",
    "raw":      "0",
}
_CHART_AMT_QTY_CODE: dict[str, str] = {
    "amount": "1",
    "qty":    "2",
}
_CHART_TRADE_CODE: dict[str, str] = {
    "net_buy": "0",
    "buy":     "1",
    "sell":    "2",
}
_CHART_UNIT_CODE: dict[str, str] = {
    "thousand": "1000",
    "single":   "1",
}
_CHART_SECTOR_MARKET_CODE: dict[str, str] = {
    "kospi":    "0",
    "kosdaq":   "1",
    "kospi200": "2",
}

# ---------------------------------------------------------------------------
# 7단계 매핑 테이블 — 업종·기관/외국인·공매도·대차거래
# ---------------------------------------------------------------------------
_SECT_MRKT_CODE: dict[str, str] = {
    "kospi":    "0",
    "kosdaq":   "1",
    "kospi200": "2",
}
_SECT_AMT_QTY_CODE: dict[str, str] = {
    "amount": "0",
    "qty":    "1",
}
_SECT_EXCHANGE_CODE: dict[str, str] = {
    "krx": "1",
    "nxt": "2",
    "all": "3",
}
_FRGN_STK_SECT_CODE: dict[str, str] = {
    "stock":  "0",
    "sector": "1",
}
_FRGN_DURATION_CODE: dict[str, str] = {
    "1":      "1",
    "3":      "3",
    "5":      "5",
    "10":     "10",
    "20":     "20",
    "120":    "120",
    "custom": "0",
}
_SLB_MRKT_CODE: dict[str, str] = {
    "kospi":  "001",
    "kosdaq": "101",
}

# ---------------------------------------------------------------------------
# 8단계 매핑 테이블 — ETF·ELW·테마·프로그램매매
# ---------------------------------------------------------------------------
_ETF_DURATION_CODE: dict[str, str] = {
    "1w": "0",
    "1m": "1",
    "6m": "2",
    "1y": "3",
}
_ELW_FLUC_CODE: dict[str, str] = {
    "surge":   "1",
    "plunge":  "2",
}
_ELW_RIGHT_CODE: dict[str, str] = {
    "all":        "000",
    "call":       "001",
    "put":        "002",
    "dc":         "003",
    "dp":         "004",
    "ex":         "005",
    "early_call": "006",
    "early_put":  "007",
}
_ELW_SORT_CODE: dict[str, str] = {
    "rise_rate": "1",
    "rise_gap":  "2",
    "fall_rate": "3",
    "fall_gap":  "4",
    "volume":    "5",
    "amount":    "6",
    "expire":    "7",
}
_THEME_SEARCH_CODE: dict[str, str] = {
    "all":   "0",
    "theme": "1",
    "stock": "2",
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

    _ACNT_PATH    = "/api/dostk/acnt"
    _MRKCOND_PATH = "/api/dostk/mrkcond"
    _STKINFO_PATH = "/api/dostk/stkinfo"
    _RKINFO_PATH  = "/api/dostk/rkinfo"
    _CHART_PATH    = "/api/dostk/chart"
    _SECT_PATH     = "/api/dostk/sect"
    _FRGNISTT_PATH = "/api/dostk/frgnistt"
    _SHSA_PATH     = "/api/dostk/shsa"
    _SLB_PATH      = "/api/dostk/slb"
    _ETF_PATH      = "/api/dostk/etf"
    _ELW_PATH      = "/api/dostk/elw"
    _THME_PATH     = "/api/dostk/thme"

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

    # =======================================================================
    # 4단계 — 국내주식 시세 (mrkcond)
    # =======================================================================

    # -----------------------------------------------------------------------
    # ka10004 — 주식호가요청
    # -----------------------------------------------------------------------

    def get_orderbook(self, stock_code: str) -> Orderbook:
        """주식 10차 호가 및 잔량을 조회한다 (ka10004).

        Args:
            stock_code: 거래소별 종목코드.
                KRX: ``"005930"``, NXT: ``"005930_NX"``, SOR: ``"005930_AL"``.

        Returns:
            호가 정보 ``Orderbook``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10004"),
        ))

        def _sell_level(n: int) -> OrderbookLevel:
            if n == 1:
                return OrderbookLevel(
                    price=raw.get("sel_fpr_bid", ""),
                    qty=raw.get("sel_fpr_req", ""),
                    qty_change=raw.get("sel_1th_pre_req_pre", ""),
                )
            return OrderbookLevel(
                price=raw.get(f"sel_{n}th_pre_bid", ""),
                qty=raw.get(f"sel_{n}th_pre_req", ""),
                qty_change=raw.get(f"sel_{n}th_pre_req_pre", ""),
            )

        def _buy_level(n: int) -> OrderbookLevel:
            if n == 1:
                return OrderbookLevel(
                    price=raw.get("buy_fpr_bid", ""),
                    qty=raw.get("buy_fpr_req", ""),
                    qty_change=raw.get("buy_1th_pre_req_pre", ""),
                )
            return OrderbookLevel(
                price=raw.get(f"buy_{n}th_pre_bid", ""),
                qty=raw.get(f"buy_{n}th_pre_req", ""),
                qty_change=raw.get(f"buy_{n}th_pre_req_pre", ""),
            )

        return Orderbook(
            base_time=raw.get("bid_req_base_tm", ""),
            sell_levels=[_sell_level(i) for i in range(1, 11)],
            buy_levels=[_buy_level(i) for i in range(1, 11)],
            tot_sell_qty=raw.get("tot_sel_req", ""),
            tot_buy_qty=raw.get("tot_buy_req", ""),
            tot_sell_qty_change=raw.get("tot_sel_req_jub_pre", ""),
            tot_buy_qty_change=raw.get("tot_buy_req_jub_pre", ""),
            ovt_sell_qty=raw.get("ovt_sel_req", ""),
            ovt_buy_qty=raw.get("ovt_buy_req", ""),
            ovt_sell_qty_change=raw.get("ovt_sel_req_pre", ""),
            ovt_buy_qty_change=raw.get("ovt_buy_req_pre", ""),
        )

    # -----------------------------------------------------------------------
    # ka10005 — 주식일주월시분요청
    # -----------------------------------------------------------------------

    def get_stock_periods(self, stock_code: str) -> StockPeriods:
        """주식의 일·주·월·시·분 OHLCV 데이터를 조회한다 (ka10005).

        Args:
            stock_code: 거래소별 종목코드.

        Returns:
            기간별 OHLCV 리스트 ``StockPeriods``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10005"),
        ))
        items = [
            StockPeriodItem(
                date=item.get("date", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                close_pric=item.get("close_pric", ""),
                pre=item.get("pre", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
                for_poss=item.get("for_poss", ""),
                for_wght=item.get("for_wght", ""),
                for_netprps=item.get("for_netprps", ""),
                orgn_netprps=item.get("orgn_netprps", ""),
                ind_netprps=item.get("ind_netprps", ""),
                crd_remn_rt=item.get("crd_remn_rt", ""),
                frgn=item.get("frgn", ""),
                prm=item.get("prm", ""),
            )
            for item in raw.get("stk_ddwkmm", [])
        ]
        return StockPeriods(items=items)

    # -----------------------------------------------------------------------
    # ka10006 — 주식시분요청
    # -----------------------------------------------------------------------

    def get_stock_minutes(self, stock_code: str) -> StockMinutes:
        """주식 시·분 시세를 조회한다 (ka10006).

        Args:
            stock_code: 거래소별 종목코드.

        Returns:
            시분 시세 ``StockMinutes``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10006"),
        ))
        return StockMinutes(
            date=raw.get("date", ""),
            open_pric=raw.get("open_pric", ""),
            high_pric=raw.get("high_pric", ""),
            low_pric=raw.get("low_pric", ""),
            close_pric=raw.get("close_pric", ""),
            pre=raw.get("pre", ""),
            flu_rt=raw.get("flu_rt", ""),
            trde_qty=raw.get("trde_qty", ""),
            trde_prica=raw.get("trde_prica", ""),
            cntr_str=raw.get("cntr_str", ""),
        )

    # -----------------------------------------------------------------------
    # ka10007 — 시세표성정보요청
    # -----------------------------------------------------------------------

    def get_market_summary(self, stock_code: str) -> MarketSummary:
        """종목의 종합 시세표(현재가·호가·예상체결 등)를 조회한다 (ka10007).

        Args:
            stock_code: 거래소별 종목코드.

        Returns:
            시세표성정보 ``MarketSummary``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10007"),
        ))
        return MarketSummary(
            stk_nm=raw.get("stk_nm", ""),
            stk_cd=raw.get("stk_cd", ""),
            date=raw.get("date", ""),
            tm=raw.get("tm", ""),
            cur_prc=raw.get("cur_prc", ""),
            flu_rt=raw.get("flu_rt", ""),
            open_pric=raw.get("open_pric", ""),
            high_pric=raw.get("high_pric", ""),
            low_pric=raw.get("low_pric", ""),
            trde_qty=raw.get("trde_qty", ""),
            trde_prica=raw.get("trde_prica", ""),
            pred_close_pric=raw.get("pred_close_pric", ""),
            upl_pric=raw.get("upl_pric", ""),
            lst_pric=raw.get("lst_pric", ""),
            exp_cntr_pric=raw.get("exp_cntr_pric", ""),
            exp_cntr_qty=raw.get("exp_cntr_qty", ""),
            tot_buy_req=raw.get("tot_buy_req", ""),
            tot_sel_req=raw.get("tot_sel_req", ""),
        )

    # -----------------------------------------------------------------------
    # ka10086 — 일별주가요청
    # -----------------------------------------------------------------------

    def get_daily_prices(
        self,
        stock_code: str,
        query_date: str,
        display_type: "DisplayType" = "qty",
    ) -> DailyPrices:
        """일별 주가 및 투자자별 순매수 데이터를 조회한다 (ka10086).

        Args:
            stock_code: 거래소별 종목코드.
            query_date: 조회일자 (``YYYYMMDD`` 형식).
            display_type: 표시구분. ``"qty"``: 수량, ``"amount"``: 금액(백만원).

        Returns:
            일별주가 리스트 ``DailyPrices``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "stk_cd": stock_code,
                "qry_dt": query_date,
                "indc_tp": _DISPLAY_TYPE_CODE[display_type],
            },
            headers=self._headers("ka10086"),
        ))
        items = [
            DailyPriceItem(
                date=item.get("date", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                close_pric=item.get("close_pric", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                for_netprps=item.get("for_netprps", ""),
                orgn_netprps=item.get("orgn_netprps", ""),
                ind_netprps=item.get("ind_netprps", ""),
                for_poss=item.get("for_poss", ""),
                for_wght=item.get("for_wght", ""),
                crd_remn_rt=item.get("crd_remn_rt", ""),
            )
            for item in raw.get("daly_stkpc", [])
        ]
        return DailyPrices(items=items)

    # -----------------------------------------------------------------------
    # ka10087 — 시간외단일가요청
    # -----------------------------------------------------------------------

    def get_afterhours_orderbook(self, stock_code: str) -> AfterhoursOrderbook:
        """시간외단일가 호가 및 현재가를 조회한다 (ka10087).

        Args:
            stock_code: 종목코드 (6자리).

        Returns:
            시간외단일가 호가 ``AfterhoursOrderbook``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10087"),
        ))
        return AfterhoursOrderbook(
            base_time=raw.get("bid_req_base_tm", ""),
            ovt_cur_prc=raw.get("ovt_sigpric_cur_prc", ""),
            ovt_flu_rt=raw.get("ovt_sigpric_flu_rt", ""),
            ovt_acc_trde_qty=raw.get("ovt_sigpric_acc_trde_qty", ""),
            ovt_sell_tot=raw.get("ovt_sigpric_sel_bid_tot_req", ""),
            ovt_buy_tot=raw.get("ovt_sigpric_buy_bid_tot_req", ""),
            sel_bid_tot=raw.get("sel_bid_tot_req", ""),
            buy_bid_tot=raw.get("buy_bid_tot_req", ""),
        )

    # -----------------------------------------------------------------------
    # ka10011 — 신주인수권전체시세요청
    # -----------------------------------------------------------------------

    def get_newstock_rights_prices(
        self,
        rights_type: "NewStockRightsType" = "all",
    ) -> NewStockRightsPrices:
        """신주인수권 전체 시세를 조회한다 (ka10011).

        Args:
            rights_type: 신주인수권구분.
                ``"all"``: 전체, ``"rights_cert"``: 신주인수권증권, ``"rights_deed"``: 신주인수권증서.

        Returns:
            신주인수권 시세 리스트 ``NewStockRightsPrices``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"newstk_recvrht_tp": _NEW_STOCK_RIGHTS_CODE[rights_type]},
            headers=self._headers("ka10011"),
        ))
        items = [
            NewStockRightsItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
            )
            for item in raw.get("newstk_recvrht_mrpr", [])
        ]
        return NewStockRightsPrices(items=items)

    # -----------------------------------------------------------------------
    # ka10044 — 일별기관매매종목요청
    # -----------------------------------------------------------------------

    def get_daily_institution_stocks(
        self,
        start_date: str,
        end_date: str,
        trade_type: "InstitutionTradeType",
        market_type: "MrktType3",
        exchange: "MrkcondExchangeType" = "all",
    ) -> DailyInstitutionStocks:
        """기관 순매도·순매수 상위 종목을 조회한다 (ka10044).

        Args:
            start_date: 시작일자 (``YYYYMMDD`` 형식).
            end_date: 종료일자 (``YYYYMMDD`` 형식).
            trade_type: 매매구분. ``"sell"``: 순매도, ``"buy"``: 순매수.
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            일별기관매매종목 리스트 ``DailyInstitutionStocks``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "strt_dt": start_date,
                "end_dt": end_date,
                "trde_tp": _INSTITUTION_TRADE_CODE[trade_type],
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10044"),
        ))
        items = [
            DailyInstitutionStockItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                netprps_qty=item.get("netprps_qty", ""),
                netprps_amt=item.get("netprps_amt", ""),
            )
            for item in raw.get("daly_orgn_trde_stk", [])
        ]
        return DailyInstitutionStocks(items=items)

    # -----------------------------------------------------------------------
    # ka10045 — 종목별기관매매추이요청
    # -----------------------------------------------------------------------

    def get_stock_institution_trend(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        org_price_type: "EstimatedPriceType" = "buy",
        for_price_type: "EstimatedPriceType" = "buy",
    ) -> StockInstitutionTrend:
        """종목별 기관·외인 매매 추이를 조회한다 (ka10045).

        Args:
            stock_code: 거래소별 종목코드.
            start_date: 시작일자 (``YYYYMMDD`` 형식).
            end_date: 종료일자 (``YYYYMMDD`` 형식).
            org_price_type: 기관추정단가구분. ``"buy"``: 매수단가, ``"sell"``: 매도단가.
            for_price_type: 외인추정단가구분. ``"buy"``: 매수단가, ``"sell"``: 매도단가.

        Returns:
            종목별기관매매추이 ``StockInstitutionTrend``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "stk_cd": stock_code,
                "strt_dt": start_date,
                "end_dt": end_date,
                "orgn_prsm_unp_tp": _ESTIMATED_PRICE_CODE[org_price_type],
                "for_prsm_unp_tp": _ESTIMATED_PRICE_CODE[for_price_type],
            },
            headers=self._headers("ka10045"),
        ))
        items = [
            StockInstitutionTrendItem(
                dt=item.get("dt", ""),
                close_pric=item.get("close_pric", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                orgn_dt_acc=item.get("orgn_dt_acc", ""),
                orgn_daly_nettrde_qty=item.get("orgn_daly_nettrde_qty", ""),
                for_dt_acc=item.get("for_dt_acc", ""),
                for_daly_nettrde_qty=item.get("for_daly_nettrde_qty", ""),
                limit_exh_rt=item.get("limit_exh_rt", ""),
            )
            for item in raw.get("stk_orgn_trde_trnsn", [])
        ]
        return StockInstitutionTrend(
            orgn_prsm_avg_pric=raw.get("orgn_prsm_avg_pric", ""),
            for_prsm_avg_pric=raw.get("for_prsm_avg_pric", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka10046 — 체결강도추이시간별요청
    # -----------------------------------------------------------------------

    def get_execution_strength_by_time(self, stock_code: str) -> ExecutionStrength:
        """체결강도 추이(시간별)를 조회한다 (ka10046).

        Args:
            stock_code: 거래소별 종목코드 (6자리).

        Returns:
            체결강도 시계열 ``ExecutionStrength``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10046"),
        ))
        items = [
            ExecutionStrengthItem(
                time_or_dt=item.get("cntr_tm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                cntr_str=item.get("cntr_str", ""),
                cntr_str_5=item.get("cntr_str_5min", ""),
                cntr_str_20=item.get("cntr_str_20min", ""),
                cntr_str_60=item.get("cntr_str_60min", ""),
            )
            for item in raw.get("cntr_str_tm", [])
        ]
        return ExecutionStrength(items=items)

    # -----------------------------------------------------------------------
    # ka10047 — 체결강도추이일별요청
    # -----------------------------------------------------------------------

    def get_execution_strength_by_day(self, stock_code: str) -> ExecutionStrength:
        """체결강도 추이(일별)를 조회한다 (ka10047).

        Args:
            stock_code: 거래소별 종목코드 (6자리).

        Returns:
            체결강도 일별 시계열 ``ExecutionStrength``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10047"),
        ))
        items = [
            ExecutionStrengthItem(
                time_or_dt=item.get("dt", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                cntr_str=item.get("cntr_str", ""),
                cntr_str_5=item.get("cntr_str_5min", ""),
                cntr_str_20=item.get("cntr_str_20min", ""),
                cntr_str_60=item.get("cntr_str_60min", ""),
            )
            for item in raw.get("cntr_str_daly", [])
        ]
        return ExecutionStrength(items=items)

    # -----------------------------------------------------------------------
    # ka10063 — 장중투자자별매매요청
    # -----------------------------------------------------------------------

    def get_intraday_investor_trading(
        self,
        market_type: "MrktType3",
        investor: "InvestorType",
        exchange: "MrkcondExchangeType" = "all",
        foreign_all: str = "0",
        simultaneous_net_buy: str = "0",
    ) -> IntradayInvestorTrading:
        """장중 투자자별 매매 상위 종목을 조회한다 (ka10063).

        Args:
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            investor: 투자자별.
                ``"foreign"``: 외국인, ``"institution"``: 기관계, ``"trust"``: 투신,
                ``"insurance"``: 보험, ``"bank"``: 은행, ``"pension"``: 연기금,
                ``"gov"``: 국가, ``"other_corp"``: 기타법인.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            foreign_all: 외국계전체. ``"1"``: 체크, ``"0"``: 미체크.
            simultaneous_net_buy: 동시순매수구분. ``"1"``: 체크, ``"0"``: 미체크.

        Returns:
            장중투자자별매매 리스트 ``IntradayInvestorTrading``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "amt_qty_tp": "1",
                "invsr": _INVESTOR_CODE[investor],
                "frgn_all": foreign_all,
                "smtm_netprps_tp": simultaneous_net_buy,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10063"),
        ))
        items = [
            IntradayInvestorItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                netprps_qty=item.get("netprps_qty", ""),
                buy_qty=item.get("buy_qty", ""),
                sell_qty=item.get("sell_qty", ""),
            )
            for item in raw.get("opmr_invsr_trde", [])
        ]
        return IntradayInvestorTrading(items=items)

    # -----------------------------------------------------------------------
    # ka10066 — 장마감후투자자별매매요청
    # -----------------------------------------------------------------------

    def get_afterclose_investor_trading(
        self,
        market_type: "MrktType3",
        trade_type: "AfterTradeType",
        amount_qty_type: "AfterAmtQtyType" = "amount",
        exchange: "MrkcondExchangeType" = "all",
    ) -> AfterCloseInvestorTrading:
        """장마감 후 투자자별 매매 상위 종목을 조회한다 (ka10066).

        Args:
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            trade_type: 매매구분. ``"net_buy"``: 순매수, ``"buy"``: 매수, ``"sell"``: 매도.
            amount_qty_type: 금액수량구분. ``"amount"``: 금액, ``"qty"``: 수량.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            장마감후투자자별매매 리스트 ``AfterCloseInvestorTrading``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "amt_qty_tp": _AFTER_AMT_QTY_CODE[amount_qty_type],
                "trde_tp": _AFTER_TRADE_TYPE_CODE[trade_type],
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10066"),
        ))
        items = [
            AfterCloseInvestorItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                ind_invsr=item.get("ind_invsr", ""),
                frgnr_invsr=item.get("frgnr_invsr", ""),
                orgn=item.get("orgn", ""),
            )
            for item in raw.get("opaf_invsr_trde", [])
        ]
        return AfterCloseInvestorTrading(items=items)

    # -----------------------------------------------------------------------
    # ka10078 — 증권사별종목매매동향요청
    # -----------------------------------------------------------------------

    def get_broker_stock_trend(
        self,
        broker_code: str,
        stock_code: str,
        start_date: str,
        end_date: str,
    ) -> BrokerStockTrend:
        """특정 증권사의 종목별 매매동향을 조회한다 (ka10078).

        Args:
            broker_code: 회원사코드 (3자리). ``get_broker_list()``로 조회 가능.
            stock_code: 거래소별 종목코드.
            start_date: 시작일자 (``YYYYMMDD`` 형식).
            end_date: 종료일자 (``YYYYMMDD`` 형식).

        Returns:
            증권사별종목매매동향 리스트 ``BrokerStockTrend``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "mmcm_cd": broker_code,
                "stk_cd": stock_code,
                "strt_dt": start_date,
                "end_dt": end_date,
            },
            headers=self._headers("ka10078"),
        ))
        items = [
            BrokerStockTrendItem(
                dt=item.get("dt", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                netprps_qty=item.get("netprps_qty", ""),
                buy_qty=item.get("buy_qty", ""),
                sell_qty=item.get("sell_qty", ""),
            )
            for item in raw.get("sec_stk_trde_trend", [])
        ]
        return BrokerStockTrend(items=items)

    # =======================================================================
    # 4단계 — 국내주식 종목정보 (stkinfo)
    # =======================================================================

    # -----------------------------------------------------------------------
    # ka10001 — 주식기본정보요청
    # -----------------------------------------------------------------------

    def get_stock_info(self, stock_code: str) -> StockInfo:
        """주식 기본정보(현재가·재무지표·시가총액 등)를 조회한다 (ka10001).

        Args:
            stock_code: 거래소별 종목코드.

        Returns:
            주식기본정보 ``StockInfo``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10001"),
        ))
        return StockInfo(
            stk_cd=raw.get("stk_cd", ""),
            stk_nm=raw.get("stk_nm", ""),
            cur_prc=raw.get("cur_prc", ""),
            flu_rt=raw.get("flu_rt", ""),
            trde_qty=raw.get("trde_qty", ""),
            open_pric=raw.get("open_pric", ""),
            high_pric=raw.get("high_pric", ""),
            low_pric=raw.get("low_pric", ""),
            upl_pric=raw.get("upl_pric", ""),
            lst_pric=raw.get("lst_pric", ""),
            mac=raw.get("mac", ""),
            per=raw.get("per", ""),
            pbr=raw.get("pbr", ""),
            eps=raw.get("eps", ""),
            roe=raw.get("roe", ""),
            flo_stk=raw.get("flo_stk", ""),
            cap=raw.get("cap", ""),
            oyr_hgst=raw.get("oyr_hgst", ""),
            oyr_lwst=raw.get("oyr_lwst", ""),
        )

    # -----------------------------------------------------------------------
    # ka10002 — 주식거래원요청
    # -----------------------------------------------------------------------

    def get_stock_brokers(self, stock_code: str) -> StockBrokers:
        """주식 매도·매수 상위 5개 거래원을 조회한다 (ka10002).

        Args:
            stock_code: 거래소별 종목코드.

        Returns:
            매도·매수 거래원 정보 ``StockBrokers``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10002"),
        ))
        sell_brokers = [
            BrokerEntry(
                name=raw.get(f"sel_trde_ori_nm_{i}", ""),
                code=raw.get(f"sel_trde_ori_{i}", ""),
                qty=raw.get(f"sel_trde_qty_{i}", ""),
            )
            for i in range(1, 6)
        ]
        buy_brokers = [
            BrokerEntry(
                name=raw.get(f"buy_trde_ori_nm_{i}", ""),
                code=raw.get(f"buy_trde_ori_{i}", ""),
                qty=raw.get(f"buy_trde_qty_{i}", ""),
            )
            for i in range(1, 6)
        ]
        return StockBrokers(
            stk_cd=raw.get("stk_cd", ""),
            stk_nm=raw.get("stk_nm", ""),
            cur_prc=raw.get("cur_prc", ""),
            sell_brokers=sell_brokers,
            buy_brokers=buy_brokers,
        )

    # -----------------------------------------------------------------------
    # ka10003 — 체결정보요청
    # -----------------------------------------------------------------------

    def get_execution_info(self, stock_code: str) -> ExecutionInfo:
        """주식 체결 내역을 조회한다 (ka10003).

        Args:
            stock_code: 거래소별 종목코드.

        Returns:
            체결정보 리스트 ``ExecutionInfo``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10003"),
        ))
        items = [
            ExecutionInfoItem(
                tm=item.get("tm", ""),
                cur_prc=item.get("cur_prc", ""),
                cntr_trde_qty=item.get("cntr_trde_qty", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                cntr_str=item.get("cntr_str", ""),
                stex_tp=item.get("stex_tp", ""),
            )
            for item in raw.get("cntr_infr", [])
        ]
        return ExecutionInfo(items=items)

    # -----------------------------------------------------------------------
    # ka10013 — 신용매매동향요청
    # -----------------------------------------------------------------------

    def get_credit_trading_trend(
        self,
        stock_code: str,
        date: str,
        query_type: "CreditQueryType" = "loan",
    ) -> CreditTradingTrend:
        """신용 매매동향(융자·대주 잔고 추이)을 조회한다 (ka10013).

        Args:
            stock_code: 거래소별 종목코드.
            date: 조회일자 (``YYYYMMDD`` 형식).
            query_type: 조회구분. ``"loan"``: 융자, ``"short"``: 대주.

        Returns:
            신용매매동향 리스트 ``CreditTradingTrend``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "stk_cd": stock_code,
                "dt": date,
                "qry_tp": _CREDIT_QUERY_CODE[query_type],
            },
            headers=self._headers("ka10013"),
        ))
        items = [
            CreditTradingItem(
                dt=item.get("dt", ""),
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                new=item.get("new", ""),
                rpya=item.get("rpya", ""),
                remn=item.get("remn", ""),
                remn_rt=item.get("remn_rt", ""),
            )
            for item in raw.get("crd_trde_trend", [])
        ]
        return CreditTradingTrend(items=items)

    # -----------------------------------------------------------------------
    # ka10015 — 일별거래상세요청
    # -----------------------------------------------------------------------

    def get_daily_trading_detail(
        self,
        stock_code: str,
        start_date: str,
    ) -> DailyTradingDetail:
        """일별 거래상세(거래량·거래대금·투자자별 순매수 등)를 조회한다 (ka10015).

        Args:
            stock_code: 거래소별 종목코드.
            start_date: 시작일자 (``YYYYMMDD`` 형식).

        Returns:
            일별거래상세 리스트 ``DailyTradingDetail``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "stk_cd": stock_code,
                "strt_dt": start_date,
            },
            headers=self._headers("ka10015"),
        ))
        items = [
            DailyTradingDetailItem(
                dt=item.get("dt", ""),
                close_pric=item.get("close_pric", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
                cntr_str=item.get("cntr_str", ""),
                for_netprps=item.get("for_netprps", ""),
                orgn_netprps=item.get("orgn_netprps", ""),
                ind_netprps=item.get("ind_netprps", ""),
            )
            for item in raw.get("daly_trde_dtl", [])
        ]
        return DailyTradingDetail(items=items)

    # -----------------------------------------------------------------------
    # ka10016 — 신고저가요청
    # -----------------------------------------------------------------------

    def get_high_low_stocks(
        self,
        high_low_type: "HighLowSelectType",
        market_type: "MrktType3" = "all",
        exchange: "MrkcondExchangeType" = "all",
        period: str = "5",
        stock_condition: str = "0",
        volume_type: str = "00000",
        credit_condition: str = "0",
        include_limit: str = "0",
        high_low_close_type: str = "1",
    ) -> HighLowStocks:
        """신고가·신저가 종목을 조회한다 (ka10016).

        Args:
            high_low_type: 신고저구분. ``"high"``: 신고가, ``"low"``: 신저가.
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            period: 기간 (일). 5·10·20·60·250 중 선택.
            stock_condition: 종목조건. ``"0"``: 전체조회 등.
            volume_type: 거래량구분. ``"00000"``: 전체조회 등.
            credit_condition: 신용조건. ``"0"``: 전체조회 등.
            include_limit: 상하한포함. ``"0"``: 미포함, ``"1"``: 포함.
            high_low_close_type: 고저종구분. ``"1"``: 고저기준, ``"2"``: 종가기준.

        Returns:
            신고저가 종목 리스트 ``HighLowStocks``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "ntl_tp": _HIGH_LOW_SELECT_CODE[high_low_type],
                "high_low_close_tp": high_low_close_type,
                "stk_cnd": stock_condition,
                "trde_qty_tp": volume_type,
                "crd_cnd": credit_condition,
                "updown_incls": include_limit,
                "dt": period,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10016"),
        ))
        items = [
            HighLowStockItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
            )
            for item in raw.get("ntl_pric", [])
        ]
        return HighLowStocks(items=items)

    # -----------------------------------------------------------------------
    # ka10017 — 상하한가요청
    # -----------------------------------------------------------------------

    def get_limit_stocks(
        self,
        up_down_type: str,
        market_type: "MrktType3" = "all",
        exchange: "MrkcondExchangeType" = "all",
        sort_type: str = "1",
        stock_condition: str = "0",
        volume_type: str = "00000",
        credit_condition: str = "0",
        price_condition: str = "0",
    ) -> LimitStocks:
        """상한가·하한가 종목을 조회한다 (ka10017).

        Args:
            up_down_type: 상하한구분.
                ``"1"``: 상한, ``"2"``: 상승, ``"3"``: 보합, ``"4"``: 하한, ``"5"``: 하락,
                ``"6"``: 전일상한, ``"7"``: 전일하한.
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            sort_type: 정렬구분. ``"1"``: 종목코드순, ``"2"``: 연속횟수순, ``"3"``: 등락률순.
            stock_condition: 종목조건. ``"0"``: 전체조회 등.
            volume_type: 거래량구분. ``"00000"``: 전체조회 등.
            credit_condition: 신용조건. ``"0"``: 전체조회 등.
            price_condition: 매매금구분. ``"0"``: 전체조회 등.

        Returns:
            상하한가 종목 리스트 ``LimitStocks``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "updown_tp": up_down_type,
                "sort_tp": sort_type,
                "stk_cnd": stock_condition,
                "trde_qty_tp": volume_type,
                "crd_cnd": credit_condition,
                "trde_gold_tp": price_condition,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10017"),
        ))
        items = [
            LimitStockItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                sel_bid=item.get("sel_bid", ""),
                buy_bid=item.get("buy_bid", ""),
                cnt=item.get("cnt", ""),
            )
            for item in raw.get("updown_pric", [])
        ]
        return LimitStocks(items=items)

    # -----------------------------------------------------------------------
    # ka10018 — 고저가근접요청
    # -----------------------------------------------------------------------

    def get_near_high_low(
        self,
        high_low_type: "HighLowSelectType",
        approach_rate: str,
        market_type: "MrktType3" = "all",
        exchange: "MrkcondExchangeType" = "all",
        volume_type: str = "00000",
        stock_condition: str = "0",
        credit_condition: str = "0",
    ) -> NearHighLow:
        """고가·저가 근접 종목을 조회한다 (ka10018).

        Args:
            high_low_type: 고저구분. ``"high"``: 고가, ``"low"``: 저가.
            approach_rate: 근접율. ``"05"``: 0.5%, ``"10"``: 1.0%, ``"15"``: 1.5% 등.
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            volume_type: 거래량구분. ``"00000"``: 전체조회 등.
            stock_condition: 종목조건. ``"0"``: 전체조회 등.
            credit_condition: 신용조건. ``"0"``: 전체조회 등.

        Returns:
            고저가근접 종목 리스트 ``NearHighLow``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "high_low_tp": _HIGH_LOW_SELECT_CODE[high_low_type],
                "alacc_rt": approach_rate,
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "trde_qty_tp": volume_type,
                "stk_cnd": stock_condition,
                "crd_cnd": credit_condition,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10018"),
        ))
        items = [
            NearHighLowItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                tdy_high_pric=item.get("tdy_high_pric", ""),
                tdy_low_pric=item.get("tdy_low_pric", ""),
            )
            for item in raw.get("high_low_pric_alacc", [])
        ]
        return NearHighLow(items=items)

    # -----------------------------------------------------------------------
    # ka10019 — 가격급등락요청
    # -----------------------------------------------------------------------

    def get_price_surge_stocks(
        self,
        surge_type: str,
        time_type: str,
        time_value: str,
        market_type: "MrktType3Ext" = "all",
        exchange: "MrkcondExchangeType" = "all",
        volume_type: str = "00000",
        stock_condition: str = "0",
        credit_condition: str = "0",
        price_condition: str = "0",
        include_limit: str = "1",
    ) -> PriceSurgeStocks:
        """가격 급등·급락 종목을 조회한다 (ka10019).

        Args:
            surge_type: 등락구분. ``"1"``: 급등, ``"2"``: 급락.
            time_type: 시간구분. ``"1"``: 분전, ``"2"``: 일전.
            time_value: 시간(분 또는 일). 예) ``"60"`` → 60분 전 대비.
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``, ``"kospi200"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            volume_type: 거래량구분. ``"00000"``: 전체조회 등.
            stock_condition: 종목조건. ``"0"``: 전체조회 등.
            credit_condition: 신용조건. ``"0"``: 전체조회 등.
            price_condition: 가격조건. ``"0"``: 전체조회 등.
            include_limit: 상하한포함. ``"0"``: 미포함, ``"1"``: 포함.

        Returns:
            가격급등락 종목 리스트 ``PriceSurgeStocks``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "mrkt_tp": _MRKT_TYPE3_EXT_CODE[market_type],
                "flu_tp": surge_type,
                "tm_tp": time_type,
                "tm": time_value,
                "trde_qty_tp": volume_type,
                "stk_cnd": stock_condition,
                "crd_cnd": credit_condition,
                "pric_cnd": price_condition,
                "updown_incls": include_limit,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10019"),
        ))
        items = [
            PriceSurgeItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                base_pric=item.get("base_pric", ""),
                jmp_rt=item.get("jmp_rt", ""),
                trde_qty=item.get("trde_qty", ""),
            )
            for item in raw.get("pric_jmpflu", [])
        ]
        return PriceSurgeStocks(items=items)

    # -----------------------------------------------------------------------
    # ka10024 — 거래량갱신요청
    # -----------------------------------------------------------------------

    def get_volume_updated_stocks(
        self,
        market_type: "MrktType3" = "all",
        cycle_type: str = "5",
        volume_type: str = "5",
        exchange: "MrkcondExchangeType" = "all",
    ) -> VolumeUpdatedStocks:
        """기간 대비 거래량이 갱신된 종목을 조회한다 (ka10024).

        Args:
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            cycle_type: 주기구분. ``"5"``: 5일, ``"10"``: 10일, ``"20"``: 20일 등.
            volume_type: 거래량구분.
                ``"5"``: 5천주이상, ``"10"``: 만주이상, ``"50"``: 5만주이상 등.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            거래량갱신 종목 리스트 ``VolumeUpdatedStocks``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "cycle_tp": cycle_type,
                "trde_qty_tp": volume_type,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10024"),
        ))
        items = [
            VolumeUpdatedItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                prev_trde_qty=item.get("prev_trde_qty", ""),
                now_trde_qty=item.get("now_trde_qty", ""),
            )
            for item in raw.get("trde_qty_updt", [])
        ]
        return VolumeUpdatedStocks(items=items)

    # -----------------------------------------------------------------------
    # ka10025 — 매물대집중요청
    # -----------------------------------------------------------------------

    def get_supply_concentration(
        self,
        concentration_rate: str,
        supply_count: str,
        cycle_type: str = "50",
        market_type: "MrktType3" = "all",
        exchange: "MrkcondExchangeType" = "all",
        current_price_entry: str = "0",
    ) -> SupplyConcentration:
        """매물대가 집중된 종목을 조회한다 (ka10025).

        Args:
            concentration_rate: 매물집중비율 (0~100).
            supply_count: 매물대수 (숫자 입력).
            cycle_type: 주기구분.
                ``"50"``: 50일, ``"100"``: 100일, ``"150"``: 150일, ``"200"``: 200일, ``"250"``: 250일, ``"300"``: 300일.
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            current_price_entry: 현재가진입. ``"0"``: 미포함, ``"1"``: 포함.

        Returns:
            매물대집중 종목 리스트 ``SupplyConcentration``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "prps_cnctr_rt": concentration_rate,
                "cur_prc_entry": current_price_entry,
                "prpscnt": supply_count,
                "cycle_tp": cycle_type,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10025"),
        ))
        items = [
            SupplyConcentrationItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                pric_strt=item.get("pric_strt", ""),
                pric_end=item.get("pric_end", ""),
                prps_qty=item.get("prps_qty", ""),
                prps_rt=item.get("prps_rt", ""),
            )
            for item in raw.get("prps_cnctr", [])
        ]
        return SupplyConcentration(items=items)

    # -----------------------------------------------------------------------
    # ka10026 — 고저PER요청
    # -----------------------------------------------------------------------

    def get_high_low_per(
        self,
        per_type: "PERType",
        exchange: "MrkcondExchangeType" = "all",
    ) -> HighLowPER:
        """고PER·저PER·PBR·ROE 상위 종목을 조회한다 (ka10026).

        Args:
            per_type: PER구분.
                ``"low_pbr"``: 저PBR, ``"high_pbr"``: 고PBR,
                ``"low_per"``: 저PER, ``"high_per"``: 고PER,
                ``"low_roe"``: 저ROE, ``"high_roe"``: 고ROE.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            고저PER 종목 리스트 ``HighLowPER``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "pertp": _PER_TYPE_CODE[per_type],
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10026"),
        ))
        items = [
            HighLowPERItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                per=item.get("per", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                now_trde_qty=item.get("now_trde_qty", ""),
            )
            for item in raw.get("high_low_per", [])
        ]
        return HighLowPER(items=items)

    # -----------------------------------------------------------------------
    # ka10028 — 시가대비등락률요청
    # -----------------------------------------------------------------------

    def get_open_price_change(
        self,
        sort_type: str = "1",
        change_condition: str = "1",
        market_type: "MrktType3" = "all",
        exchange: "MrkcondExchangeType" = "all",
        volume_condition: str = "0000",
        include_limit: str = "1",
        stock_condition: str = "0",
        credit_condition: str = "0",
        amount_condition: str = "0",
    ) -> OpenPriceChange:
        """시가 대비 등락률 상·하위 종목을 조회한다 (ka10028).

        Args:
            sort_type: 정렬구분. ``"1"``: 시가, ``"2"``: 고가, ``"3"``: 저가, ``"4"``: 기준가.
            change_condition: 등락조건. ``"1"``: 상위, ``"2"``: 하위.
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            volume_condition: 거래량조건. ``"0000"``: 전체조회 등.
            include_limit: 상하한포함. ``"0"``: 불포함, ``"1"``: 포함.
            stock_condition: 종목조건. ``"0"``: 전체조회 등.
            credit_condition: 신용조건. ``"0"``: 전체조회 등.
            amount_condition: 거래대금조건. ``"0"``: 전체조회 등.

        Returns:
            시가대비등락률 종목 리스트 ``OpenPriceChange``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "sort_tp": sort_type,
                "trde_qty_cnd": volume_condition,
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "updown_incls": include_limit,
                "stk_cnd": stock_condition,
                "crd_cnd": credit_condition,
                "trde_prica_cnd": amount_condition,
                "flu_cnd": change_condition,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10028"),
        ))
        items = [
            OpenPriceChangeItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                open_pric=item.get("open_pric", ""),
                open_pric_pre=item.get("open_pric_pre", ""),
                now_trde_qty=item.get("now_trde_qty", ""),
            )
            for item in raw.get("open_pric_pre_flu_rt", [])
        ]
        return OpenPriceChange(items=items)

    # -----------------------------------------------------------------------
    # ka10043 — 거래원매물대분석요청
    # -----------------------------------------------------------------------

    def get_broker_supply_analysis(
        self,
        stock_code: str,
        broker_code: str,
        start_date: str,
        end_date: str,
        period: str = "5",
        sort_base: str = "1",
        query_date_type: str = "0",
        time_point_type: str = "0",
        exchange: "MrkcondExchangeType" = "all",
    ) -> BrokerSupplyAnalysis:
        """특정 거래원의 종목 매물대 분석 데이터를 조회한다 (ka10043).

        Args:
            stock_code: 거래소별 종목코드.
            broker_code: 회원사코드 (3자리). ``get_broker_list()``로 조회 가능.
            start_date: 시작일자 (``YYYYMMDD`` 형식).
            end_date: 종료일자 (``YYYYMMDD`` 형식).
            period: 기간. ``"5"``: 5일, ``"10"``: 10일, ``"20"``: 20일, ``"40"``: 40일, ``"60"``: 60일, ``"120"``: 120일.
            sort_base: 정렬기준. ``"1"``: 종가순, ``"2"``: 날짜순.
            query_date_type: 조회기간구분. ``"0"``: 기간으로 조회, ``"1"``: 시작·종료일로 조회.
            time_point_type: 시점구분. ``"0"``: 당일, ``"1"``: 전일.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            거래원매물대분석 리스트 ``BrokerSupplyAnalysis``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "stk_cd": stock_code,
                "strt_dt": start_date,
                "end_dt": end_date,
                "qry_dt_tp": query_date_type,
                "pot_tp": time_point_type,
                "dt": period,
                "sort_base": sort_base,
                "mmcm_cd": broker_code,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10043"),
        ))
        items = [
            BrokerSupplyItem(
                dt=item.get("dt", ""),
                close_pric=item.get("close_pric", ""),
                sel_qty=item.get("sel_qty", ""),
                buy_qty=item.get("buy_qty", ""),
                netprps_qty=item.get("netprps_qty", ""),
                trde_wght=item.get("trde_wght", ""),
            )
            for item in raw.get("trde_ori_prps_anly", [])
        ]
        return BrokerSupplyAnalysis(items=items)

    # -----------------------------------------------------------------------
    # ka10052 — 거래원순간거래량요청
    # -----------------------------------------------------------------------

    def get_broker_instant_volume(
        self,
        broker_code: str,
        market_type: str = "0",
        stock_code: str = "",
        volume_type: str = "0",
        price_type: str = "0",
        exchange: "MrkcondExchangeType" = "all",
    ) -> BrokerInstantVolume:
        """특정 거래원의 순간거래량을 조회한다 (ka10052).

        Args:
            broker_code: 회원사코드 (3자리). ``get_broker_list()``로 조회 가능.
            market_type: 시장구분. ``"0"``: 전체, ``"1"``: 코스피, ``"2"``: 코스닥, ``"3"``: 종목.
            stock_code: 종목코드. 시장구분이 ``"3"``(종목)일 때 사용.
            volume_type: 수량구분. ``"0"``: 전체, ``"1"``: 1000주 이상 등.
            price_type: 가격구분. ``"0"``: 전체, ``"1"``: 1천원 미만 등.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            거래원순간거래량 리스트 ``BrokerInstantVolume``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "mmcm_cd": broker_code,
                "stk_cd": stock_code,
                "mrkt_tp": market_type,
                "qty_tp": volume_type,
                "pric_tp": price_type,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10052"),
        ))
        items = [
            BrokerInstantVolumeItem(
                tm=item.get("tm", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                trde_ori_nm=item.get("trde_ori_nm", ""),
                tp=item.get("tp", ""),
                mont_trde_qty=item.get("mont_trde_qty", ""),
                acc_netprps=item.get("acc_netprps", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
            )
            for item in raw.get("trde_ori_mont_trde_qty", [])
        ]
        return BrokerInstantVolume(items=items)

    # -----------------------------------------------------------------------
    # ka10054 — 변동성완화장치발동종목요청
    # -----------------------------------------------------------------------

    def get_vi_triggered_stocks(
        self,
        market_type: "MrktType3" = "all",
        exchange: "MrkcondExchangeType" = "all",
        stock_code: str = "",
        trigger_type: str = "0",
        trigger_direction: str = "0",
        pre_market_type: str = "0",
        skip_stocks: str = "000000000",
    ) -> VIStocks:
        """변동성완화장치(VI) 발동 종목을 조회한다 (ka10054).

        Args:
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            stock_code: 종목코드. 공백이면 전체 시장 조회.
            trigger_type: 발동구분. ``"0"``: 전체, ``"1"``: 정적VI, ``"2"``: 동적VI, ``"3"``: 동적+정적VI.
            trigger_direction: 발동방향. ``"0"``: 전체, ``"1"``: 상승, ``"2"``: 하락.
            pre_market_type: 장전구분. ``"0"``: 전체, ``"1"``: 정규시장, ``"2"``: 시간외단일가.
            skip_stocks: 제외종목 (9자리). 전종목포함: ``"000000000"``.

        Returns:
            VI 발동종목 리스트 ``VIStocks``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "bf_mkrt_tp": pre_market_type,
                "stk_cd": stock_code,
                "motn_tp": trigger_type,
                "skip_stk": skip_stocks,
                "trde_qty_tp": "0",
                "min_trde_qty": "0",
                "max_trde_qty": "0",
                "trde_prica_tp": "0",
                "min_trde_prica": "0",
                "max_trde_prica": "0",
                "motn_drc": trigger_direction,
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10054"),
        ))
        items = [
            VIStockItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                motn_pric=item.get("motn_pric", ""),
                viaplc_tp=item.get("viaplc_tp", ""),
                vimotn_cnt=item.get("vimotn_cnt", ""),
                stex_tp=item.get("stex_tp", ""),
            )
            for item in raw.get("motn_stk", [])
        ]
        return VIStocks(items=items)

    # -----------------------------------------------------------------------
    # ka10055 — 당일전일체결량요청
    # -----------------------------------------------------------------------

    def get_today_prev_execution_qty(
        self,
        stock_code: str,
        day_type: "TodayPrevType" = "today",
    ) -> TodayPrevExecutionQty:
        """당일·전일 체결량 시계열을 조회한다 (ka10055).

        Args:
            stock_code: 거래소별 종목코드.
            day_type: 당일전일구분. ``"today"``: 당일, ``"prev"``: 전일.

        Returns:
            당일전일체결량 리스트 ``TodayPrevExecutionQty``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "stk_cd": stock_code,
                "tdy_pred": _TODAY_PREV_CODE[day_type],
            },
            headers=self._headers("ka10055"),
        ))
        items = [
            TodayPrevExecutionQtyItem(
                cntr_tm=item.get("cntr_tm", ""),
                cntr_pric=item.get("cntr_pric", ""),
                flu_rt=item.get("flu_rt", ""),
                cntr_qty=item.get("cntr_qty", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                acc_trde_prica=item.get("acc_trde_prica", ""),
            )
            for item in raw.get("tdy_pred_cntr_qty", [])
        ]
        return TodayPrevExecutionQty(items=items)

    # -----------------------------------------------------------------------
    # ka10058 — 투자자별일별매매종목요청
    # -----------------------------------------------------------------------

    def get_investor_daily_stocks(
        self,
        start_date: str,
        end_date: str,
        trade_type: "InstitutionTradeType",
        investor_type: "InvestorType2",
        market_type: "MrktType3" = "all",
        exchange: "MrkcondExchangeType" = "all",
    ) -> InvestorDailyStocks:
        """투자자별 일별 매매 상위 종목을 조회한다 (ka10058).

        Args:
            start_date: 시작일자 (``YYYYMMDD`` 형식).
            end_date: 종료일자 (``YYYYMMDD`` 형식).
            trade_type: 매매구분. ``"sell"``: 순매도, ``"buy"``: 순매수.
            investor_type: 투자자구분.
                ``"individual"``: 개인, ``"foreign"``: 외국인, ``"financial_inv"``: 금융투자,
                ``"trust"``: 투신, ``"private_fund"``: 사모펀드, ``"other_fin"``: 기타금융,
                ``"bank"``: 은행, ``"insurance"``: 보험, ``"pension"``: 연기금,
                ``"gov"``: 국가, ``"other_corp"``: 기타법인, ``"institution"``: 기관계.
            market_type: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            투자자별일별매매종목 리스트 ``InvestorDailyStocks``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "strt_dt": start_date,
                "end_dt": end_date,
                "trde_tp": _INSTITUTION_TRADE_CODE[trade_type],
                "mrkt_tp": _MRKT_TYPE3_CODE[market_type],
                "invsr_tp": _INVESTOR2_CODE[investor_type],
                "stex_tp": _MRKCOND_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10058"),
        ))
        items = [
            InvestorDailyStockItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                netslmt_qty=item.get("netslmt_qty", ""),
                netslmt_amt=item.get("netslmt_amt", ""),
                cur_prc=item.get("cur_prc", ""),
                pre_rt=item.get("pre_rt", ""),
            )
            for item in raw.get("invsr_daly_trde_stk", [])
        ]
        return InvestorDailyStocks(items=items)

    # -----------------------------------------------------------------------
    # ka10059 — 종목별투자자기관별요청
    # -----------------------------------------------------------------------

    def get_stock_investor_by_day(
        self,
        date: str,
        stock_code: str,
        trade_type: "InvestorTradeType" = "net_buy",
        amount_qty_type: "AmtQtyType" = "amount",
        unit_type: "UnitType" = "thousand",
    ) -> StockInvestorByDay:
        """종목별 투자자·기관별 일별 매매 현황을 조회한다 (ka10059).

        Args:
            date: 조회일자 (``YYYYMMDD`` 형식).
            stock_code: 거래소별 종목코드.
            trade_type: 매매구분. ``"net_buy"``: 순매수, ``"buy"``: 매수, ``"sell"``: 매도.
            amount_qty_type: 금액수량구분. ``"amount"``: 금액, ``"qty"``: 수량.
            unit_type: 단위구분. ``"thousand"``: 천주, ``"single"``: 단주.

        Returns:
            종목별투자자기관별 일별 리스트 ``StockInvestorByDay``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "dt": date,
                "stk_cd": stock_code,
                "amt_qty_tp": _AMT_QTY_CODE[amount_qty_type],
                "trde_tp": _INVESTOR_TRADE_CODE[trade_type],
                "unit_tp": _UNIT_CODE[unit_type],
            },
            headers=self._headers("ka10059"),
        ))
        items = [
            StockInvestorItem(
                dt=item.get("dt", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                ind_invsr=item.get("ind_invsr", ""),
                frgnr_invsr=item.get("frgnr_invsr", ""),
                orgn=item.get("orgn", ""),
                fnnc_invt=item.get("fnnc_invt", ""),
                bank=item.get("bank", ""),
                penfnd_etc=item.get("penfnd_etc", ""),
            )
            for item in raw.get("stk_invsr_orgn", [])
        ]
        return StockInvestorByDay(items=items)

    # -----------------------------------------------------------------------
    # ka10061 — 종목별투자자기관별합계요청
    # -----------------------------------------------------------------------

    def get_stock_investor_total(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        trade_type: "InvestorTradeType" = "net_buy",
        amount_qty_type: "AmtQtyType" = "amount",
        unit_type: "UnitType" = "thousand",
    ) -> StockInvestorTotal:
        """종목별 투자자·기관별 기간 합계를 조회한다 (ka10061).

        Args:
            stock_code: 거래소별 종목코드.
            start_date: 시작일자 (``YYYYMMDD`` 형식).
            end_date: 종료일자 (``YYYYMMDD`` 형식).
            trade_type: 매매구분. ``"net_buy"``: 순매수, ``"buy"``: 매수, ``"sell"``: 매도.
            amount_qty_type: 금액수량구분. ``"amount"``: 금액, ``"qty"``: 수량.
            unit_type: 단위구분. ``"thousand"``: 천주, ``"single"``: 단주.

        Returns:
            투자자·기관별 합계 ``StockInvestorTotal``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "stk_cd": stock_code,
                "strt_dt": start_date,
                "end_dt": end_date,
                "amt_qty_tp": _AMT_QTY_CODE[amount_qty_type],
                "trde_tp": _INVESTOR_TRADE_CODE[trade_type],
                "unit_tp": _UNIT_CODE[unit_type],
            },
            headers=self._headers("ka10061"),
        ))
        first = raw.get("stk_invsr_orgn_tot", [{}])[0] if raw.get("stk_invsr_orgn_tot") else {}
        return StockInvestorTotal(
            ind_invsr=first.get("ind_invsr", ""),
            frgnr_invsr=first.get("frgnr_invsr", ""),
            orgn=first.get("orgn", ""),
            fnnc_invt=first.get("fnnc_invt", ""),
            bank=first.get("bank", ""),
            penfnd_etc=first.get("penfnd_etc", ""),
            samo_fund=first.get("samo_fund", ""),
            natn=first.get("natn", ""),
            etc_corp=first.get("etc_corp", ""),
        )

    # -----------------------------------------------------------------------
    # ka10084 — 당일전일체결요청
    # -----------------------------------------------------------------------

    def get_today_prev_execution(
        self,
        stock_code: str,
        day_type: "TodayPrevType" = "today",
        tick_min: "TickMinType" = "tick",
        time: str = "",
    ) -> TodayPrevExecution:
        """당일·전일 체결 데이터를 조회한다 (ka10084).

        Args:
            stock_code: 거래소별 종목코드.
            day_type: 당일전일구분. ``"today"``: 당일, ``"prev"``: 전일.
            tick_min: 틱분. ``"tick"``: 틱, ``"minute"``: 분.
            time: 조회시간 (4자리 ``HHMM``). 예) 오전 9시 → ``"0900"``. 공백이면 전체.

        Returns:
            당일전일체결 리스트 ``TodayPrevExecution``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "stk_cd": stock_code,
                "tdy_pred": _TODAY_PREV_CODE[day_type],
                "tic_min": _TICK_MIN_CODE[tick_min],
                "tm": time,
            },
            headers=self._headers("ka10084"),
        ))
        items = [
            TodayPrevExecutionItem(
                tm=item.get("tm", ""),
                cur_prc=item.get("cur_prc", ""),
                cntr_trde_qty=item.get("cntr_trde_qty", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                cntr_str=item.get("cntr_str", ""),
                stex_tp=item.get("stex_tp", ""),
            )
            for item in raw.get("tdy_pred_cntr", [])
        ]
        return TodayPrevExecution(items=items)

    # -----------------------------------------------------------------------
    # ka10095 — 관심종목정보요청
    # -----------------------------------------------------------------------

    def get_watchlist_info(self, stock_codes: str) -> WatchlistInfo:
        """관심종목 정보(현재가·호가·시가총액 등)를 조회한다 (ka10095).

        Args:
            stock_codes: 종목코드. 여러 종목은 ``"|"`` 로 구분.
                예) ``"005930|000660|035720"``.

        Returns:
            관심종목 정보 리스트 ``WatchlistInfo``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {"stk_cd": stock_codes},
            headers=self._headers("ka10095"),
        ))
        items = [
            WatchlistStockItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                upl_pric=item.get("upl_pric", ""),
                lst_pric=item.get("lst_pric", ""),
            )
            for item in raw.get("atn_stk_infr", [])
        ]
        return WatchlistInfo(items=items)

    # -----------------------------------------------------------------------
    # ka10099 — 종목정보 리스트
    # -----------------------------------------------------------------------

    def get_stock_list(self, market_type: "StkMarketType" = "kospi") -> StockList:
        """시장별 상장 종목 리스트를 조회한다 (ka10099).

        Args:
            market_type: 시장구분.
                ``"kospi"``: 코스피, ``"kosdaq"``: 코스닥, ``"etf"``: ETF,
                ``"elw"``: ELW, ``"konex"``: 코넥스, ``"gold"``: 금현물 등.

        Returns:
            종목정보 리스트 ``StockList``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {"mrkt_tp": _STK_MARKET_CODE[market_type]},
            headers=self._headers("ka10099"),
        ))
        items = [
            StockListItem(
                code=item.get("code", ""),
                name=item.get("name", ""),
                list_count=item.get("listCount", ""),
                reg_day=item.get("regDay", ""),
                last_price=item.get("lastPrice", ""),
                state=item.get("state", ""),
                market_name=item.get("marketName", ""),
                up_name=item.get("upName", ""),
                nxt_enable=item.get("nxtEnable", ""),
            )
            for item in raw.get("list", [])
        ]
        return StockList(items=items)

    # -----------------------------------------------------------------------
    # ka10100 — 종목정보 조회
    # -----------------------------------------------------------------------

    def get_stock_detail(self, stock_code: str) -> StockDetail:
        """단일 종목의 상세 정보를 조회한다 (ka10100).

        Args:
            stock_code: 종목코드 (6자리 단축코드).

        Returns:
            종목 상세정보 ``StockDetail``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10100"),
        ))
        return StockDetail(
            code=raw.get("code", ""),
            name=raw.get("name", ""),
            list_count=raw.get("listCount", ""),
            reg_day=raw.get("regDay", ""),
            last_price=raw.get("lastPrice", ""),
            state=raw.get("state", ""),
            market_code=raw.get("marketCode", ""),
            market_name=raw.get("marketName", ""),
            up_name=raw.get("upName", ""),
            up_size_name=raw.get("upSizeName", ""),
            nxt_enable=raw.get("nxtEnable", ""),
        )

    # -----------------------------------------------------------------------
    # ka10101 — 업종코드 리스트
    # -----------------------------------------------------------------------

    def get_sector_list(self, market_type: "SectorMarketType" = "kospi") -> SectorList:
        """시장별 업종코드 리스트를 조회한다 (ka10101).

        Args:
            market_type: 시장구분.
                ``"kospi"``: 코스피(거래소), ``"kosdaq"``: 코스닥,
                ``"kospi200"``: KOSPI200, ``"kospi100"``: KOSPI100, ``"krx100"``: KRX100.

        Returns:
            업종코드 리스트 ``SectorList``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {"mrkt_tp": _SECTOR_MARKET_CODE[market_type]},
            headers=self._headers("ka10101"),
        ))
        items = [
            SectorItem(
                market_code=item.get("marketCode", ""),
                code=item.get("code", ""),
                name=item.get("name", ""),
                group=item.get("group", ""),
            )
            for item in raw.get("list", [])
        ]
        return SectorList(items=items)

    # -----------------------------------------------------------------------
    # ka10102 — 회원사 리스트
    # -----------------------------------------------------------------------

    def get_broker_list(self) -> BrokerList:
        """키움 API 회원사 리스트를 조회한다 (ka10102).

        Returns:
            회원사 리스트 ``BrokerList``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {},
            headers=self._headers("ka10102"),
        ))
        items = [
            BrokerItem(
                code=item.get("code", ""),
                name=item.get("name", ""),
                gb=item.get("gb", ""),
            )
            for item in raw.get("list", [])
        ]
        return BrokerList(items=items)

    # =======================================================================
    # 5단계 — 순위정보 (rkinfo)
    # =======================================================================

    # -----------------------------------------------------------------------
    # ka10020 — 호가잔량상위요청
    # -----------------------------------------------------------------------

    def get_bid_qty_upper(
        self,
        market: "RkinfoMarketType",
        sort_type: "RkinfoBidSortType",
        trade_qty_type: str,
        stock_cond: str,
        credit_cond: str,
        exchange: "RkinfoStexType",
    ) -> BidQtyUpper:
        """호가잔량 상위 종목을 조회한다 (ka10020).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            sort_type: 정렬구분.
                ``"net_buy_qty"``: 순매수잔량순, ``"net_sell_qty"``: 순매도잔량순,
                ``"buy_ratio"``: 매수비율순, ``"sell_ratio"``: 매도비율순.
            trade_qty_type: 거래량구분.
                ``"0000"``: 0주이상, ``"0010"``: 만주이상, ``"0050"``: 5만주이상, ``"00100"``: 10만주이상.
            stock_cond: 종목조건.
                ``"0"``: 전체, ``"1"``: 관리종목제외, ``"5"``~``"9"``: 증거금 조건.
            credit_cond: 신용조건.
                ``"0"``: 전체, ``"9"``: 신용융자전체, 기타 군별 코드.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            호가잔량상위 ``BidQtyUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":    _RKINFO_MARKET_CODE[market],
                "sort_tp":    _RKINFO_BID_SORT_CODE[sort_type],
                "trde_qty_tp": trade_qty_type,
                "stk_cnd":    stock_cond,
                "crd_cnd":    credit_cond,
                "stex_tp":    _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10020"),
        ))
        items = [
            BidQtyUpperItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                trde_qty=item.get("trde_qty", ""),
                tot_sel_req=item.get("tot_sel_req", ""),
                tot_buy_req=item.get("tot_buy_req", ""),
                netprps_req=item.get("netprps_req", ""),
                buy_rt=item.get("buy_rt", ""),
            )
            for item in raw.get("bid_req_upper", [])
        ]
        return BidQtyUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10021 — 호가잔량급증요청
    # -----------------------------------------------------------------------

    def get_bid_qty_surge(
        self,
        market: "RkinfoMarketType",
        trade_type: "RkinfoBidTradeType",
        sort_type: "RkinfoSurgeSort2Type",
        time_min: str,
        trade_qty_type: str,
        stock_cond: str,
        exchange: "RkinfoStexType",
    ) -> BidQtySurge:
        """호가잔량 급증 종목을 조회한다 (ka10021).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            trade_type: 매매구분. ``"buy"``: 매수잔량, ``"sell"``: 매도잔량.
            sort_type: 정렬구분. ``"surge_qty"``: 급증량, ``"surge_ratio"``: 급증률.
            time_min: 시간구분 (분 입력, 예: ``"30"``).
            trade_qty_type: 거래량구분.
                ``"1"``: 천주이상, ``"5"``: 5천주이상, ``"10"``: 만주이상, ``"50"``: 5만주이상.
            stock_cond: 종목조건 (``"0"``~``"9"``).
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            호가잔량급증 ``BidQtySurge``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":    _RKINFO_MARKET_CODE[market],
                "trde_tp":    _RKINFO_BID_TRADE_CODE[trade_type],
                "sort_tp":    _RKINFO_SURGE_SORT2_CODE[sort_type],
                "tm_tp":      time_min,
                "trde_qty_tp": trade_qty_type,
                "stk_cnd":    stock_cond,
                "stex_tp":    _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10021"),
        ))
        items = [
            BidQtySurgeItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                base_rt=item.get("int", ""),
                now=item.get("now", ""),
                sdnin_qty=item.get("sdnin_qty", ""),
                sdnin_rt=item.get("sdnin_rt", ""),
                tot_buy_qty=item.get("tot_buy_qty", ""),
            )
            for item in raw.get("bid_req_sdnin", [])
        ]
        return BidQtySurge(items=items)

    # -----------------------------------------------------------------------
    # ka10022 — 잔량율급증요청
    # -----------------------------------------------------------------------

    def get_qty_ratio_surge(
        self,
        market: "RkinfoMarketType",
        ratio_type: str,
        time_min: str,
        trade_qty_type: str,
        stock_cond: str,
        exchange: "RkinfoStexType",
    ) -> QtyRatioSurge:
        """잔량율 급증 종목을 조회한다 (ka10022).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            ratio_type: 비율구분. ``"1"``: 매수/매도비율, ``"2"``: 매도/매수비율.
            time_min: 시간구분 (분 입력, 예: ``"1"``).
            trade_qty_type: 거래량구분.
                ``"5"``: 5천주이상, ``"10"``: 만주이상, ``"50"``: 5만주이상.
            stock_cond: 종목조건 (``"0"``~``"9"``).
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            잔량율급증 ``QtyRatioSurge``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":    _RKINFO_MARKET_CODE[market],
                "rt_tp":      ratio_type,
                "tm_tp":      time_min,
                "trde_qty_tp": trade_qty_type,
                "stk_cnd":    stock_cond,
                "stex_tp":    _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10022"),
        ))
        items = [
            QtyRatioSurgeItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                base_rt=item.get("int", ""),
                now_rt=item.get("now_rt", ""),
                sdnin_rt=item.get("sdnin_rt", ""),
                tot_sel_req=item.get("tot_sel_req", ""),
                tot_buy_req=item.get("tot_buy_req", ""),
            )
            for item in raw.get("req_rt_sdnin", [])
        ]
        return QtyRatioSurge(items=items)

    # -----------------------------------------------------------------------
    # ka10023 — 거래량급증요청
    # -----------------------------------------------------------------------

    def get_trade_qty_surge(
        self,
        market: "RkinfoMarketType",
        sort_type: str,
        time_type: str,
        trade_qty_type: str,
        stock_cond: str,
        price_type: str,
        exchange: "RkinfoStexType",
        time: str = "",
    ) -> TradeQtySurge:
        """거래량 급증 종목을 조회한다 (ka10023).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            sort_type: 정렬구분.
                ``"1"``: 급증량, ``"2"``: 급증률, ``"3"``: 급감량, ``"4"``: 급감률.
            time_type: 시간구분. ``"1"``: 분, ``"2"``: 전일.
            trade_qty_type: 거래량구분 (``"5"``~``"1000"``).
            stock_cond: 종목조건 (``"0"``~``"20"``).
            price_type: 가격구분 (``"0"``~``"9"``).
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            time: 분 입력 (``time_type="1"``일 때만 유효, 기본 ``""``).

        Returns:
            거래량급증 ``TradeQtySurge``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":    _RKINFO_MARKET_CODE[market],
                "sort_tp":    sort_type,
                "tm_tp":      time_type,
                "trde_qty_tp": trade_qty_type,
                "tm":         time,
                "stk_cnd":    stock_cond,
                "pric_tp":    price_type,
                "stex_tp":    _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10023"),
        ))
        items = [
            TradeQtySurgeItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                prev_trde_qty=item.get("prev_trde_qty", ""),
                now_trde_qty=item.get("now_trde_qty", ""),
                sdnin_qty=item.get("sdnin_qty", ""),
                sdnin_rt=item.get("sdnin_rt", ""),
            )
            for item in raw.get("trde_qty_sdnin", [])
        ]
        return TradeQtySurge(items=items)

    # -----------------------------------------------------------------------
    # ka10027 — 전일대비등락률상위요청
    # -----------------------------------------------------------------------

    def get_price_change_upper(
        self,
        market: "RkinfoMarketType",
        sort_type: "RkinfoPriceChangeSortType",
        trade_qty_cond: str,
        stock_cond: str,
        credit_cond: str,
        updown_incls: str,
        price_cond: str,
        trade_amt_cond: str,
        exchange: "RkinfoStexType",
    ) -> PriceChangeUpper:
        """전일대비 등락률 상위 종목을 조회한다 (ka10027).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            sort_type: 정렬구분.
                ``"rise_ratio"``: 상승률, ``"rise_gap"``: 상승폭,
                ``"fall_ratio"``: 하락률, ``"fall_gap"``: 하락폭, ``"flat"``: 보합.
            trade_qty_cond: 거래량조건 (``"0000"``, ``"0010"``, …).
            stock_cond: 종목조건 (``"0"``~``"16"``).
            credit_cond: 신용조건 (``"0"``, ``"9"`` 등).
            updown_incls: 상하한포함. ``"0"``: 미포함, ``"1"``: 포함.
            price_cond: 가격조건 (``"0"``~``"10"``).
            trade_amt_cond: 거래대금조건 (``"0"``, ``"3"``~``"5000"``).
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            전일대비등락률상위 ``PriceChangeUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":        _RKINFO_MARKET_CODE[market],
                "sort_tp":        _RKINFO_PRICE_CHANGE_SORT_CODE[sort_type],
                "trde_qty_cnd":   trade_qty_cond,
                "stk_cnd":        stock_cond,
                "crd_cnd":        credit_cond,
                "updown_incls":   updown_incls,
                "pric_cnd":       price_cond,
                "trde_prica_cnd": trade_amt_cond,
                "stex_tp":        _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10027"),
        ))
        items = [
            PriceChangeUpperItem(
                stk_cls=item.get("stk_cls", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                sel_req=item.get("sel_req", ""),
                buy_req=item.get("buy_req", ""),
                now_trde_qty=item.get("now_trde_qty", ""),
                cntr_str=item.get("cntr_str", ""),
                cnt=item.get("cnt", ""),
            )
            for item in raw.get("pred_pre_flu_rt_upper", [])
        ]
        return PriceChangeUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10029 — 예상체결등락률상위요청
    # -----------------------------------------------------------------------

    def get_expected_trade_upper(
        self,
        market: "RkinfoMarketType",
        sort_type: str,
        trade_qty_cond: str,
        stock_cond: str,
        credit_cond: str,
        price_cond: str,
        exchange: "RkinfoStexType",
    ) -> ExpectedTradeUpper:
        """예상체결 등락률 상위 종목을 조회한다 (ka10029).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            sort_type: 정렬구분.
                ``"1"``: 상승률, ``"2"``: 상승폭, ``"3"``: 보합, ``"4"``: 하락률,
                ``"5"``: 하락폭, ``"6"``: 체결량, ``"7"``: 상한, ``"8"``: 하한.
            trade_qty_cond: 거래량조건 (``"0"``, ``"1"``, ``"3"``, ``"5"``, ``"10"``, ``"50"``, ``"100"``).
            stock_cond: 종목조건 (``"0"``~``"16"``).
            credit_cond: 신용조건 (``"0"``, ``"9"`` 등).
            price_cond: 가격조건 (``"0"``~``"10"``).
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            예상체결등락률상위 ``ExpectedTradeUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":      _RKINFO_MARKET_CODE[market],
                "sort_tp":      sort_type,
                "trde_qty_cnd": trade_qty_cond,
                "stk_cnd":      stock_cond,
                "crd_cnd":      credit_cond,
                "pric_cnd":     price_cond,
                "stex_tp":      _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10029"),
        ))
        items = [
            ExpectedTradeUpperItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                exp_cntr_pric=item.get("exp_cntr_pric", ""),
                base_pric=item.get("base_pric", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                exp_cntr_qty=item.get("exp_cntr_qty", ""),
                sel_req=item.get("sel_req", ""),
                sel_bid=item.get("sel_bid", ""),
                buy_bid=item.get("buy_bid", ""),
                buy_req=item.get("buy_req", ""),
            )
            for item in raw.get("exp_cntr_flu_rt_upper", [])
        ]
        return ExpectedTradeUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10030 — 당일거래량상위요청
    # -----------------------------------------------------------------------

    def get_daily_trade_qty_upper(
        self,
        market: "RkinfoMarketType",
        sort_type: str,
        stock_cond: str,
        credit_type: str,
        trade_qty_type: str,
        price_type: str,
        trade_amt_type: str,
        market_open_type: str,
        exchange: "RkinfoStexType",
    ) -> DailyTradeQtyUpper:
        """당일거래량 상위 종목을 조회한다 (ka10030).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            sort_type: 정렬구분. ``"1"``: 거래량, ``"2"``: 거래회전율, ``"3"``: 거래대금.
            stock_cond: 관리종목포함 (``"0"``~``"16"``).
            credit_type: 신용구분 (``"0"``, ``"9"`` 등).
            trade_qty_type: 거래량구분 (``"0"``, ``"5"``, ``"10"`` 등).
            price_type: 가격구분 (``"0"``~``"9"``).
            trade_amt_type: 거래대금구분 (``"0"``, ``"1"`` 등).
            market_open_type: 장운영구분. ``"0"``: 전체, ``"1"``: 장중, ``"2"``: 장전시간외, ``"3"``: 장후시간외.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            당일거래량상위 ``DailyTradeQtyUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":       _RKINFO_MARKET_CODE[market],
                "sort_tp":       sort_type,
                "mang_stk_incls": stock_cond,
                "crd_tp":        credit_type,
                "trde_qty_tp":   trade_qty_type,
                "pric_tp":       price_type,
                "trde_prica_tp": trade_amt_type,
                "mrkt_open_tp":  market_open_type,
                "stex_tp":       _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10030"),
        ))
        items = [
            DailyTradeQtyUpperItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                trde_qty=item.get("trde_qty", ""),
                pred_rt=item.get("pred_rt", ""),
                trde_tern_rt=item.get("trde_tern_rt", ""),
                trde_amt=item.get("trde_amt", ""),
                opmr_trde_qty=item.get("opmr_trde_qty", ""),
                opmr_pred_rt=item.get("opmr_pred_rt", ""),
                opmr_trde_rt=item.get("opmr_trde_rt", ""),
                opmr_trde_amt=item.get("opmr_trde_amt", ""),
                af_mkrt_trde_qty=item.get("af_mkrt_trde_qty", ""),
                af_mkrt_pred_rt=item.get("af_mkrt_pred_rt", ""),
                af_mkrt_trde_rt=item.get("af_mkrt_trde_rt", ""),
                af_mkrt_trde_amt=item.get("af_mkrt_trde_amt", ""),
                bf_mkrt_trde_qty=item.get("bf_mkrt_trde_qty", ""),
                bf_mkrt_pred_rt=item.get("bf_mkrt_pred_rt", ""),
                bf_mkrt_trde_rt=item.get("bf_mkrt_trde_rt", ""),
                bf_mkrt_trde_amt=item.get("bf_mkrt_trde_amt", ""),
            )
            for item in raw.get("tdy_trde_qty_upper", [])
        ]
        return DailyTradeQtyUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10031 — 전일거래량상위요청
    # -----------------------------------------------------------------------

    def get_prev_trade_qty_upper(
        self,
        market: "RkinfoMarketType",
        query_type: str,
        rank_start: str,
        rank_end: str,
        exchange: "RkinfoStexType",
    ) -> PrevTradeQtyUpper:
        """전일거래량 상위 종목을 조회한다 (ka10031).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            query_type: 조회구분. ``"1"``: 전일거래량 상위100, ``"2"``: 전일거래대금 상위100.
            rank_start: 순위시작 (``"0"``~``"100"`` 값 중 조회 시작 순위).
            rank_end: 순위끝 (``"0"``~``"100"`` 값 중 조회 끝 순위).
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            전일거래량상위 ``PrevTradeQtyUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":   _RKINFO_MARKET_CODE[market],
                "qry_tp":    query_type,
                "rank_strt": rank_start,
                "rank_end":  rank_end,
                "stex_tp":   _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10031"),
        ))
        items = [
            PrevTradeQtyUpperItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                trde_qty=item.get("trde_qty", ""),
            )
            for item in raw.get("pred_trde_qty_upper", [])
        ]
        return PrevTradeQtyUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10032 — 거래대금상위요청
    # -----------------------------------------------------------------------

    def get_trade_amt_upper(
        self,
        market: "RkinfoMarketType",
        include_managed: str,
        exchange: "RkinfoStexType",
    ) -> TradeAmtUpper:
        """거래대금 상위 종목을 조회한다 (ka10032).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            include_managed: 관리종목포함. ``"0"``: 미포함, ``"1"``: 포함.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            거래대금상위 ``TradeAmtUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":       _RKINFO_MARKET_CODE[market],
                "mang_stk_incls": include_managed,
                "stex_tp":       _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10032"),
        ))
        items = [
            TradeAmtUpperItem(
                stk_cd=item.get("stk_cd", ""),
                now_rank=item.get("now_rank", ""),
                pred_rank=item.get("pred_rank", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                sel_bid=item.get("sel_bid", ""),
                buy_bid=item.get("buy_bid", ""),
                now_trde_qty=item.get("now_trde_qty", ""),
                pred_trde_qty=item.get("pred_trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
            )
            for item in raw.get("trde_prica_upper", [])
        ]
        return TradeAmtUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10033 — 신용비율상위요청
    # -----------------------------------------------------------------------

    def get_credit_ratio_upper(
        self,
        market: "RkinfoMarketType",
        trade_qty_type: str,
        stock_cond: str,
        updown_incls: str,
        credit_cond: str,
        exchange: "RkinfoStexType",
    ) -> CreditRatioUpper:
        """신용비율 상위 종목을 조회한다 (ka10033).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            trade_qty_type: 거래량구분 (``"0"``, ``"10"`` 등).
            stock_cond: 종목조건 (``"0"``~``"9"``).
            updown_incls: 상하한포함. ``"0"``: 미포함, ``"1"``: 포함.
            credit_cond: 신용조건 (``"0"``, ``"9"`` 등).
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            신용비율상위 ``CreditRatioUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":     _RKINFO_MARKET_CODE[market],
                "trde_qty_tp": trade_qty_type,
                "stk_cnd":     stock_cond,
                "updown_incls": updown_incls,
                "crd_cnd":     credit_cond,
                "stex_tp":     _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10033"),
        ))
        items = [
            CreditRatioUpperItem(
                stk_infr=item.get("stk_infr", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                crd_rt=item.get("crd_rt", ""),
                sel_req=item.get("sel_req", ""),
                buy_req=item.get("buy_req", ""),
                now_trde_qty=item.get("now_trde_qty", ""),
            )
            for item in raw.get("crd_rt_upper", [])
        ]
        return CreditRatioUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10034 — 외인기간별매매상위요청
    # -----------------------------------------------------------------------

    def get_foreign_period_trade_upper(
        self,
        market: "RkinfoMarketType",
        trade_type: str,
        period: str,
        exchange: "RkinfoStexType",
    ) -> ForeignPeriodTradeUpper:
        """외국인 기간별 매매 상위 종목을 조회한다 (ka10034).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            trade_type: 매매구분. ``"1"``: 순매도, ``"2"``: 순매수, ``"3"``: 순매매.
            period: 기간. ``"0"``: 당일, ``"1"``: 전일, ``"5"``: 5일, ``"10"``: 10일, ``"20"``: 20일, ``"60"``: 60일.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            외인기간별매매상위 ``ForeignPeriodTradeUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp": _RKINFO_MARKET_CODE[market],
                "trde_tp": trade_type,
                "dt":      period,
                "stex_tp": _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10034"),
        ))
        items = [
            ForeignPeriodTradeUpperItem(
                rank=item.get("rank", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                sel_bid=item.get("sel_bid", ""),
                buy_bid=item.get("buy_bid", ""),
                trde_qty=item.get("trde_qty", ""),
                netprps_qty=item.get("netprps_qty", ""),
                gain_pos_stkcnt=item.get("gain_pos_stkcnt", ""),
            )
            for item in raw.get("for_dt_trde_upper", [])
        ]
        return ForeignPeriodTradeUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10035 — 외인연속순매매상위요청
    # -----------------------------------------------------------------------

    def get_foreign_consec_trade_upper(
        self,
        market: "RkinfoMarketType",
        trade_type: str,
        base_date: "RkinfoBaseDateType",
        exchange: "RkinfoStexType",
    ) -> ForeignConsecTradeUpper:
        """외국인 연속 순매매 상위 종목을 조회한다 (ka10035).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            trade_type: 매매구분. ``"1"``: 연속순매도, ``"2"``: 연속순매수.
            base_date: 기준일구분. ``"today"``: 당일기준, ``"prev"``: 전일기준.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            외인연속순매매상위 ``ForeignConsecTradeUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":    _RKINFO_MARKET_CODE[market],
                "trde_tp":    trade_type,
                "base_dt_tp": _RKINFO_BASE_DATE_CODE[base_date],
                "stex_tp":    _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10035"),
        ))
        items = [
            ForeignConsecTradeUpperItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                dm1=item.get("dm1", ""),
                dm2=item.get("dm2", ""),
                dm3=item.get("dm3", ""),
                tot=item.get("tot", ""),
                limit_exh_rt=item.get("limit_exh_rt", ""),
                pred_pre_1=item.get("pred_pre_1", ""),
                pred_pre_2=item.get("pred_pre_2", ""),
                pred_pre_3=item.get("pred_pre_3", ""),
            )
            for item in raw.get("for_cont_nettrde_upper", [])
        ]
        return ForeignConsecTradeUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10036 — 외인한도소진율증가상위
    # -----------------------------------------------------------------------

    def get_foreign_limit_exhaust_upper(
        self,
        market: "RkinfoMarketType",
        period: str,
        exchange: "RkinfoStexType",
    ) -> ForeignLimitExhaustUpper:
        """외국인 한도소진율 증가 상위 종목을 조회한다 (ka10036).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            period: 기간. ``"0"``: 당일, ``"1"``: 전일, ``"5"``: 5일, ``"10"``: 10일, ``"20"``: 20일, ``"60"``: 60일.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            외인한도소진율증가상위 ``ForeignLimitExhaustUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp": _RKINFO_MARKET_CODE[market],
                "dt":      period,
                "stex_tp": _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10036"),
        ))
        items = [
            ForeignLimitExhaustUpperItem(
                rank=item.get("rank", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                trde_qty=item.get("trde_qty", ""),
                poss_stkcnt=item.get("poss_stkcnt", ""),
                gain_pos_stkcnt=item.get("gain_pos_stkcnt", ""),
                base_limit_exh_rt=item.get("base_limit_exh_rt", ""),
                limit_exh_rt=item.get("limit_exh_rt", ""),
                exh_rt_incrs=item.get("exh_rt_incrs", ""),
            )
            for item in raw.get("for_limit_exh_rt_incrs_upper", [])
        ]
        return ForeignLimitExhaustUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10037 — 외국계창구매매상위요청
    # -----------------------------------------------------------------------

    def get_foreign_broker_trade_upper(
        self,
        market: "RkinfoMarketType",
        period: str,
        trade_type: str,
        sort_type: str,
        exchange: "RkinfoStexType",
    ) -> ForeignBrokerTradeUpper:
        """외국계 창구 매매 상위 종목을 조회한다 (ka10037).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            period: 기간. ``"0"``: 당일, ``"1"``: 전일, ``"5"``: 5일, ``"10"``: 10일, ``"20"``: 20일, ``"60"``: 60일.
            trade_type: 매매구분. ``"1"``: 순매수, ``"2"``: 순매도, ``"3"``: 매수, ``"4"``: 매도.
            sort_type: 정렬구분. ``"1"``: 금액, ``"2"``: 수량.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            외국계창구매매상위 ``ForeignBrokerTradeUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp": _RKINFO_MARKET_CODE[market],
                "dt":      period,
                "trde_tp": trade_type,
                "sort_tp": sort_type,
                "stex_tp": _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10037"),
        ))
        items = [
            ForeignBrokerTradeUpperItem(
                rank=item.get("rank", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                sel_trde_qty=item.get("sel_trde_qty", ""),
                buy_trde_qty=item.get("buy_trde_qty", ""),
                netprps_trde_qty=item.get("netprps_trde_qty", ""),
                netprps_prica=item.get("netprps_prica", ""),
                trde_qty=item.get("trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
            )
            for item in raw.get("frgn_wicket_trde_upper", [])
        ]
        return ForeignBrokerTradeUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10038 — 종목별증권사순위요청
    # -----------------------------------------------------------------------

    def get_stock_broker_rank(
        self,
        stock_code: str,
        query_type: str,
        period: str = "",
        start_date: str = "",
        end_date: str = "",
    ) -> StockBrokerRank:
        """종목별 증권사 순위를 조회한다 (ka10038).

        Args:
            stock_code: 종목코드 (예: ``"005930"``).
            query_type: 조회구분. ``"1"``: 순매도순위정렬, ``"2"``: 순매수순위정렬.
            period: 기간. ``"1"``: 전일, ``"4"``: 5일, ``"9"``: 10일, ``"19"``: 20일 등 (기본 ``""``).
            start_date: 시작일자 ``YYYYMMDD`` (기본 ``""``).
            end_date: 종료일자 ``YYYYMMDD`` (기본 ``""``).

        Returns:
            종목별증권사순위 ``StockBrokerRank``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "stk_cd":  stock_code,
                "strt_dt": start_date,
                "end_dt":  end_date,
                "qry_tp":  query_type,
                "dt":      period,
            },
            headers=self._headers("ka10038"),
        ))
        items = [
            StockBrokerRankItem(
                rank=item.get("rank", ""),
                mmcm_nm=item.get("mmcm_nm", ""),
                buy_qty=item.get("buy_qty", ""),
                sell_qty=item.get("sell_qty", ""),
                acc_netprps_qty=item.get("acc_netprps_qty", ""),
            )
            for item in raw.get("stk_sec_rank", [])
        ]
        return StockBrokerRank(
            rank_1=raw.get("rank_1", ""),
            rank_2=raw.get("rank_2", ""),
            rank_3=raw.get("rank_3", ""),
            prid_trde_qty=raw.get("prid_trde_qty", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka10039 — 증권사별매매상위요청
    # -----------------------------------------------------------------------

    def get_broker_trade_upper(
        self,
        broker_code: str,
        trade_qty_type: str,
        trade_type: str,
        period: str,
        exchange: "RkinfoStexType",
    ) -> BrokerTradeUpper:
        """증권사별 매매 상위 종목을 조회한다 (ka10039).

        Args:
            broker_code: 회원사코드 (ka10102로 조회, 예: ``"001"``).
            trade_qty_type: 거래량구분 (``"0"``, ``"5"``, ``"10"`` 등).
            trade_type: 매매구분. ``"1"``: 순매수, ``"2"``: 순매도.
            period: 기간. ``"1"``: 전일, ``"5"``: 5일, ``"10"``: 10일, ``"60"``: 60일.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.

        Returns:
            증권사별매매상위 ``BrokerTradeUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mmcm_cd":     broker_code,
                "trde_qty_tp": trade_qty_type,
                "trde_tp":     trade_type,
                "dt":          period,
                "stex_tp":     _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10039"),
        ))
        items = [
            BrokerTradeUpperItem(
                rank=item.get("rank", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                prid_stkpc_flu=item.get("prid_stkpc_flu", ""),
                flu_rt=item.get("flu_rt", ""),
                prid_trde_qty=item.get("prid_trde_qty", ""),
                netprps=item.get("netprps", ""),
                buy_trde_qty=item.get("buy_trde_qty", ""),
                sel_trde_qty=item.get("sel_trde_qty", ""),
                netprps_amt=item.get("netprps_amt", ""),
                buy_amt=item.get("buy_amt", ""),
                sell_amt=item.get("sell_amt", ""),
            )
            for item in raw.get("sec_trde_upper", [])
        ]
        return BrokerTradeUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10040 — 당일주요거래원요청
    # -----------------------------------------------------------------------

    def get_daily_main_broker(self, stock_code: str) -> DailyMainBroker:
        """종목의 당일 주요 거래원(매도/매수 상위 5개)을 조회한다 (ka10040).

        Args:
            stock_code: 종목코드 (예: ``"005930"``).

        Returns:
            당일주요거래원 ``DailyMainBroker``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10040"),
        ))
        exit_items = [
            DailyMainBrokerEntry(
                sel_scesn_tm=item.get("sel_scesn_tm", ""),
                sell_qty=item.get("sell_qty", ""),
                sel_upper_scesn_ori=item.get("sel_upper_scesn_ori", ""),
                buy_scesn_tm=item.get("buy_scesn_tm", ""),
                buy_qty=item.get("buy_qty", ""),
                buy_upper_scesn_ori=item.get("buy_upper_scesn_ori", ""),
                qry_dt=item.get("qry_dt", ""),
                qry_tm=item.get("qry_tm", ""),
            )
            for item in raw.get("tdy_main_trde_ori", [])
        ]
        return DailyMainBroker(
            sel_trde_ori_1=raw.get("sel_trde_ori_1", ""),
            sel_trde_ori_qty_1=raw.get("sel_trde_ori_qty_1", ""),
            sel_trde_ori_irds_1=raw.get("sel_trde_ori_irds_1", ""),
            buy_trde_ori_1=raw.get("buy_trde_ori_1", ""),
            buy_trde_ori_qty_1=raw.get("buy_trde_ori_qty_1", ""),
            buy_trde_ori_irds_1=raw.get("buy_trde_ori_irds_1", ""),
            sel_trde_ori_2=raw.get("sel_trde_ori_2", ""),
            sel_trde_ori_qty_2=raw.get("sel_trde_ori_qty_2", ""),
            sel_trde_ori_irds_2=raw.get("sel_trde_ori_irds_2", ""),
            buy_trde_ori_2=raw.get("buy_trde_ori_2", ""),
            buy_trde_ori_qty_2=raw.get("buy_trde_ori_qty_2", ""),
            buy_trde_ori_irds_2=raw.get("buy_trde_ori_irds_2", ""),
            sel_trde_ori_3=raw.get("sel_trde_ori_3", ""),
            sel_trde_ori_qty_3=raw.get("sel_trde_ori_qty_3", ""),
            sel_trde_ori_irds_3=raw.get("sel_trde_ori_irds_3", ""),
            buy_trde_ori_3=raw.get("buy_trde_ori_3", ""),
            buy_trde_ori_qty_3=raw.get("buy_trde_ori_qty_3", ""),
            buy_trde_ori_irds_3=raw.get("buy_trde_ori_irds_3", ""),
            sel_trde_ori_4=raw.get("sel_trde_ori_4", ""),
            sel_trde_ori_qty_4=raw.get("sel_trde_ori_qty_4", ""),
            sel_trde_ori_irds_4=raw.get("sel_trde_ori_irds_4", ""),
            buy_trde_ori_4=raw.get("buy_trde_ori_4", ""),
            buy_trde_ori_qty_4=raw.get("buy_trde_ori_qty_4", ""),
            buy_trde_ori_irds_4=raw.get("buy_trde_ori_irds_4", ""),
            sel_trde_ori_5=raw.get("sel_trde_ori_5", ""),
            sel_trde_ori_qty_5=raw.get("sel_trde_ori_qty_5", ""),
            sel_trde_ori_irds_5=raw.get("sel_trde_ori_irds_5", ""),
            buy_trde_ori_5=raw.get("buy_trde_ori_5", ""),
            buy_trde_ori_qty_5=raw.get("buy_trde_ori_qty_5", ""),
            buy_trde_ori_irds_5=raw.get("buy_trde_ori_irds_5", ""),
            frgn_sel_prsm_sum=raw.get("frgn_sel_prsm_sum", ""),
            frgn_sel_prsm_sum_chang=raw.get("frgn_sel_prsm_sum_chang", ""),
            frgn_buy_prsm_sum=raw.get("frgn_buy_prsm_sum", ""),
            frgn_buy_prsm_sum_chang=raw.get("frgn_buy_prsm_sum_chang", ""),
            items=exit_items,
        )

    # -----------------------------------------------------------------------
    # ka10042 — 순매수거래원순위요청
    # -----------------------------------------------------------------------

    def get_net_buy_broker_rank(
        self,
        stock_code: str,
        query_date_type: str,
        sort_base: str,
        period: str = "",
        start_date: str = "",
        end_date: str = "",
    ) -> NetBuyBrokerRank:
        """종목의 순매수 거래원 순위를 조회한다 (ka10042).

        Args:
            stock_code: 종목코드 (예: ``"005930"``).
            query_date_type: 조회기간구분.
                ``"0"``: 기간으로 조회, ``"1"``: 시작일자·종료일자로 조회.
            sort_base: 정렬기준. ``"1"``: 종가순, ``"2"``: 날짜순.
            period: 기간. ``"5"``: 5일, ``"10"``: 10일, ``"20"``: 20일 등 (기본 ``""``).
            start_date: 시작일자 ``YYYYMMDD`` (기본 ``""``).
            end_date: 종료일자 ``YYYYMMDD`` (기본 ``""``).

        Returns:
            순매수거래원순위 ``NetBuyBrokerRank``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "stk_cd":    stock_code,
                "strt_dt":   start_date,
                "end_dt":    end_date,
                "qry_dt_tp": query_date_type,
                "pot_tp":    "0",
                "dt":        period,
                "sort_base": sort_base,
            },
            headers=self._headers("ka10042"),
        ))
        items = [
            NetBuyBrokerRankItem(
                rank=item.get("rank", ""),
                mmcm_cd=item.get("mmcm_cd", ""),
                mmcm_nm=item.get("mmcm_nm", ""),
            )
            for item in raw.get("netprps_trde_ori_rank", [])
        ]
        return NetBuyBrokerRank(items=items)

    # -----------------------------------------------------------------------
    # ka10053 — 당일상위이탈원요청
    # -----------------------------------------------------------------------

    def get_daily_top_exit(self, stock_code: str) -> DailyTopExit:
        """종목의 당일 상위 이탈원 리스트를 조회한다 (ka10053).

        Args:
            stock_code: 종목코드 (예: ``"005930"``).

        Returns:
            당일상위이탈원 ``DailyTopExit``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10053"),
        ))
        items = [
            DailyTopExitItem(
                sel_scesn_tm=item.get("sel_scesn_tm", ""),
                sell_qty=item.get("sell_qty", ""),
                sel_upper_scesn_ori=item.get("sel_upper_scesn_ori", ""),
                buy_scesn_tm=item.get("buy_scesn_tm", ""),
                buy_qty=item.get("buy_qty", ""),
                buy_upper_scesn_ori=item.get("buy_upper_scesn_ori", ""),
                qry_dt=item.get("qry_dt", ""),
                qry_tm=item.get("qry_tm", ""),
            )
            for item in raw.get("tdy_upper_scesn_ori", [])
        ]
        return DailyTopExit(items=items)

    # -----------------------------------------------------------------------
    # ka10062 — 동일순매매순위요청
    # -----------------------------------------------------------------------

    def get_same_net_trade_rank(
        self,
        start_date: str,
        market: "RkinfoMarketType",
        trade_type: str,
        sort_cnd: "RkinfoSortCndType",
        unit_type: str,
        exchange: "RkinfoStexType",
        end_date: str = "",
    ) -> SameNetTradeRank:
        """기관·외국인 동일 순매매 순위를 조회한다 (ka10062).

        Args:
            start_date: 시작일자 ``YYYYMMDD``.
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            trade_type: 매매구분. ``"1"``: 순매수, ``"2"``: 순매도.
            sort_cnd: 정렬조건. ``"qty"``: 수량, ``"amount"``: 금액.
            unit_type: 단위구분. ``"1"``: 단주, ``"1000"``: 천주.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            end_date: 종료일자 ``YYYYMMDD`` (기본 ``""``).

        Returns:
            동일순매매순위 ``SameNetTradeRank``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "strt_dt":  start_date,
                "end_dt":   end_date,
                "mrkt_tp":  _RKINFO_MARKET_CODE[market],
                "trde_tp":  trade_type,
                "sort_cnd": _RKINFO_SORT_CND_CODE[sort_cnd],
                "unit_tp":  unit_type,
                "stex_tp":  _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka10062"),
        ))
        items = [
            SameNetTradeRankItem(
                stk_cd=item.get("stk_cd", ""),
                rank=item.get("rank", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pre_sig=item.get("pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                orgn_nettrde_qty=item.get("orgn_nettrde_qty", ""),
                orgn_nettrde_amt=item.get("orgn_nettrde_amt", ""),
                orgn_nettrde_avg_pric=item.get("orgn_nettrde_avg_pric", ""),
                for_nettrde_qty=item.get("for_nettrde_qty", ""),
                for_nettrde_amt=item.get("for_nettrde_amt", ""),
                for_nettrde_avg_pric=item.get("for_nettrde_avg_pric", ""),
                nettrde_qty=item.get("nettrde_qty", ""),
                nettrde_amt=item.get("nettrde_amt", ""),
            )
            for item in raw.get("eql_nettrde_rank", [])
        ]
        return SameNetTradeRank(items=items)

    # -----------------------------------------------------------------------
    # ka10065 — 장중투자자별매매상위요청
    # -----------------------------------------------------------------------

    def get_investor_trade_upper(
        self,
        trade_type: str,
        market: "RkinfoMarketType",
        org_type: "RkinfoOrgType",
    ) -> InvestorTradeUpper:
        """장중 투자자별 매매 상위 종목을 조회한다 (ka10065).

        Args:
            trade_type: 매매구분. ``"1"``: 순매수, ``"2"``: 순매도.
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            org_type: 기관구분.
                ``"foreign"``: 외국인, ``"institution"``: 기관계 등.

        Returns:
            장중투자자별매매상위 ``InvestorTradeUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "trde_tp": trade_type,
                "mrkt_tp": _RKINFO_MARKET_CODE[market],
                "orgn_tp": _RKINFO_ORG_TYPE_CODE[org_type],
            },
            headers=self._headers("ka10065"),
        ))
        items = [
            InvestorTradeUpperItem(
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                sel_qty=item.get("sel_qty", ""),
                buy_qty=item.get("buy_qty", ""),
                netslmt=item.get("netslmt", ""),
            )
            for item in raw.get("opmr_invsr_trde_upper", [])
        ]
        return InvestorTradeUpper(items=items)

    # -----------------------------------------------------------------------
    # ka10098 — 시간외단일가등락율순위요청
    # -----------------------------------------------------------------------

    def get_after_hours_rank(
        self,
        market: "RkinfoMarketType",
        sort_base: str,
        stock_cond: str,
        trade_qty_cond: str,
        credit_cond: str,
        trade_amt: str,
    ) -> AfterHoursRank:
        """시간외 단일가 등락율 순위를 조회한다 (ka10098).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            sort_base: 정렬기준.
                ``"1"``: 상승률, ``"2"``: 상승폭, ``"3"``: 하락률, ``"4"``: 하락폭, ``"5"``: 보합.
            stock_cond: 종목조건 (``"0"``~``"17"``).
            trade_qty_cond: 거래량조건 (``"0"``, ``"10"``, ``"50"`` 등).
            credit_cond: 신용조건 (``"0"``, ``"9"`` 등).
            trade_amt: 거래대금 (``"0"``, ``"5"``, ``"10"`` 등).

        Returns:
            시간외단일가등락율순위 ``AfterHoursRank``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":      _RKINFO_MARKET_CODE[market],
                "sort_base":    sort_base,
                "stk_cnd":      stock_cond,
                "trde_qty_cnd": trade_qty_cond,
                "crd_cnd":      credit_cond,
                "trde_prica":   trade_amt,
            },
            headers=self._headers("ka10098"),
        ))
        items = [
            AfterHoursRankItem(
                rank=item.get("rank", ""),
                stk_cd=item.get("stk_cd", ""),
                stk_nm=item.get("stk_nm", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                pred_pre=item.get("pred_pre", ""),
                flu_rt=item.get("flu_rt", ""),
                sel_tot_req=item.get("sel_tot_req", ""),
                buy_tot_req=item.get("buy_tot_req", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                acc_trde_prica=item.get("acc_trde_prica", ""),
                tdy_close_pric=item.get("tdy_close_pric", ""),
                tdy_close_pric_flu_rt=item.get("tdy_close_pric_flu_rt", ""),
            )
            for item in raw.get("ovt_sigpric_flu_rt_rank", [])
        ]
        return AfterHoursRank(items=items)

    # -----------------------------------------------------------------------
    # ka90009 — 외국인기관매매상위요청
    # -----------------------------------------------------------------------

    def get_foreign_institution_trade_upper(
        self,
        market: "RkinfoMarketType",
        amt_qty_type: str,
        query_date_type: str,
        exchange: "RkinfoStexType",
        date: str = "",
    ) -> ForeignInstitutionTradeUpper:
        """외국인·기관 매매 상위 종목을 조회한다 (ka90009).

        Args:
            market: 시장구분. ``"all"``, ``"kospi"``, ``"kosdaq"``.
            amt_qty_type: 금액수량구분. ``"1"``: 금액(천만), ``"2"``: 수량(천).
            query_date_type: 조회일자구분. ``"0"``: 조회일자 미포함, ``"1"``: 조회일자 포함.
            exchange: 거래소구분. ``"krx"``, ``"nxt"``, ``"all"``.
            date: 날짜 ``YYYYMMDD`` (기본 ``""``).

        Returns:
            외국인기관매매상위 ``ForeignInstitutionTradeUpper``.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류 또는 조회 실패.
        """
        raw = _check(self._api.post(
            self._RKINFO_PATH,
            {
                "mrkt_tp":    _RKINFO_MARKET_CODE[market],
                "amt_qty_tp": amt_qty_type,
                "qry_dt_tp":  query_date_type,
                "date":       date,
                "stex_tp":    _RKINFO_STEX_CODE[exchange],
            },
            headers=self._headers("ka90009"),
        ))
        items = [
            ForeignInstitutionTradeUpperItem(
                for_netslmt_stk_cd=item.get("for_netslmt_stk_cd", ""),
                for_netslmt_stk_nm=item.get("for_netslmt_stk_nm", ""),
                for_netslmt_amt=item.get("for_netslmt_amt", ""),
                for_netslmt_qty=item.get("for_netslmt_qty", ""),
                for_netprps_stk_cd=item.get("for_netprps_stk_cd", ""),
                for_netprps_stk_nm=item.get("for_netprps_stk_nm", ""),
                for_netprps_amt=item.get("for_netprps_amt", ""),
                for_netprps_qty=item.get("for_netprps_qty", ""),
                orgn_netslmt_stk_cd=item.get("orgn_netslmt_stk_cd", ""),
                orgn_netslmt_stk_nm=item.get("orgn_netslmt_stk_nm", ""),
                orgn_netslmt_amt=item.get("orgn_netslmt_amt", ""),
                orgn_netslmt_qty=item.get("orgn_netslmt_qty", ""),
                orgn_netprps_stk_cd=item.get("orgn_netprps_stk_cd", ""),
                orgn_netprps_stk_nm=item.get("orgn_netprps_stk_nm", ""),
                orgn_netprps_amt=item.get("orgn_netprps_amt", ""),
                orgn_netprps_qty=item.get("orgn_netprps_qty", ""),
            )
            for item in raw.get("frgnr_orgn_trde_upper", [])
        ]
        return ForeignInstitutionTradeUpper(items=items)

    # =======================================================================
    # 6단계 — 차트 (chart / sect)
    # =======================================================================

    # -----------------------------------------------------------------------
    # ka10079 — 주식틱차트조회요청
    # -----------------------------------------------------------------------

    def get_stock_tick_chart(
        self,
        stock_code: str,
        tick_scope: "ChartTickScope",
        adjusted: "ChartAdjustedPrice" = "adjusted",
    ) -> StockTickChart:
        """주식 틱 차트 데이터를 조회한다 (ka10079).

        Args:
            stock_code: 거래소별 종목코드 (예: ``"005930"``, ``"005930_NX"``).
            tick_scope: 틱 범위 (``"1"`` / ``"3"`` / ``"5"`` / ``"10"`` / ``"30"``).
            adjusted: 수정주가 반영 여부 (``"adjusted"`` 반영 / ``"raw"`` 미반영).

        Returns:
            :class:`~kiwoompy.models.StockTickChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "stk_cd":        stock_code,
                "tic_scope":     tick_scope,
                "upd_stkpc_tp":  _CHART_ADJ_CODE[adjusted],
            },
            headers=self._headers("ka10079"),
        ))
        items = [
            StockCandleItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                cntr_tm=item.get("cntr_tm", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                pred_pre=item.get("pred_pre", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
            )
            for item in raw.get("stk_tic_chart_qry", [])
        ]
        return StockTickChart(
            stk_cd=raw.get("stk_cd", ""),
            last_tic_cnt=raw.get("last_tic_cnt", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka10080 — 주식분봉차트조회요청
    # -----------------------------------------------------------------------

    def get_stock_min_chart(
        self,
        stock_code: str,
        min_scope: "ChartMinScope",
        adjusted: "ChartAdjustedPrice" = "adjusted",
        base_date: str = "",
    ) -> StockMinChart:
        """주식 분봉 차트 데이터를 조회한다 (ka10080).

        Args:
            stock_code: 거래소별 종목코드.
            min_scope: 분봉 범위 (``"1"`` / ``"3"`` / ``"5"`` / ``"10"`` / ``"15"`` / ``"30"`` / ``"45"`` / ``"60"``).
            adjusted: 수정주가 반영 여부.
            base_date: 기준일자 (``"YYYYMMDD"``, 생략 시 최신).

        Returns:
            :class:`~kiwoompy.models.StockMinChart` 인스턴스.
        """
        body: dict = {
            "stk_cd":       stock_code,
            "tic_scope":    min_scope,
            "upd_stkpc_tp": _CHART_ADJ_CODE[adjusted],
        }
        if base_date:
            body["base_dt"] = base_date
        raw = _check(self._api.post(
            self._CHART_PATH,
            body,
            headers=self._headers("ka10080"),
        ))
        items = [
            StockMinChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                cntr_tm=item.get("cntr_tm", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                pred_pre=item.get("pred_pre", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
            )
            for item in raw.get("stk_min_pole_chart_qry", [])
        ]
        return StockMinChart(stk_cd=raw.get("stk_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka10081 — 주식일봉차트조회요청
    # -----------------------------------------------------------------------

    def get_stock_day_chart(
        self,
        stock_code: str,
        base_date: str,
        adjusted: "ChartAdjustedPrice" = "adjusted",
    ) -> StockDayChart:
        """주식 일봉 차트 데이터를 조회한다 (ka10081).

        Args:
            stock_code: 거래소별 종목코드.
            base_date: 기준일자 (``"YYYYMMDD"``).
            adjusted: 수정주가 반영 여부.

        Returns:
            :class:`~kiwoompy.models.StockDayChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "stk_cd":       stock_code,
                "base_dt":      base_date,
                "upd_stkpc_tp": _CHART_ADJ_CODE[adjusted],
            },
            headers=self._headers("ka10081"),
        ))
        items = [
            StockDayChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
                dt=item.get("dt", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                pred_pre=item.get("pred_pre", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                trde_tern_rt=item.get("trde_tern_rt", ""),
            )
            for item in raw.get("stk_dt_pole_chart_qry", [])
        ]
        return StockDayChart(stk_cd=raw.get("stk_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka10082 — 주식주봉차트조회요청
    # -----------------------------------------------------------------------

    def get_stock_week_chart(
        self,
        stock_code: str,
        base_date: str,
        adjusted: "ChartAdjustedPrice" = "adjusted",
    ) -> StockWeekChart:
        """주식 주봉 차트 데이터를 조회한다 (ka10082).

        Args:
            stock_code: 거래소별 종목코드.
            base_date: 기준일자 (``"YYYYMMDD"``).
            adjusted: 수정주가 반영 여부.

        Returns:
            :class:`~kiwoompy.models.StockWeekChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "stk_cd":       stock_code,
                "base_dt":      base_date,
                "upd_stkpc_tp": _CHART_ADJ_CODE[adjusted],
            },
            headers=self._headers("ka10082"),
        ))
        items = [
            StockWeekChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
                dt=item.get("dt", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                pred_pre=item.get("pred_pre", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                trde_tern_rt=item.get("trde_tern_rt", ""),
            )
            for item in raw.get("stk_stk_pole_chart_qry", [])
        ]
        return StockWeekChart(stk_cd=raw.get("stk_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka10083 — 주식월봉차트조회요청
    # -----------------------------------------------------------------------

    def get_stock_month_chart(
        self,
        stock_code: str,
        base_date: str,
        adjusted: "ChartAdjustedPrice" = "adjusted",
    ) -> StockMonthChart:
        """주식 월봉 차트 데이터를 조회한다 (ka10083).

        Args:
            stock_code: 거래소별 종목코드.
            base_date: 기준일자 (``"YYYYMMDD"``).
            adjusted: 수정주가 반영 여부.

        Returns:
            :class:`~kiwoompy.models.StockMonthChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "stk_cd":       stock_code,
                "base_dt":      base_date,
                "upd_stkpc_tp": _CHART_ADJ_CODE[adjusted],
            },
            headers=self._headers("ka10083"),
        ))
        items = [
            StockMonthChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
                dt=item.get("dt", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                pred_pre=item.get("pred_pre", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
                trde_tern_rt=item.get("trde_tern_rt", ""),
            )
            for item in raw.get("stk_mth_pole_chart_qry", [])
        ]
        return StockMonthChart(stk_cd=raw.get("stk_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka10094 — 주식년봉차트조회요청
    # -----------------------------------------------------------------------

    def get_stock_year_chart(
        self,
        stock_code: str,
        base_date: str,
        adjusted: "ChartAdjustedPrice" = "adjusted",
    ) -> StockYearChart:
        """주식 년봉 차트 데이터를 조회한다 (ka10094).

        Args:
            stock_code: 거래소별 종목코드.
            base_date: 기준일자 (``"YYYYMMDD"``).
            adjusted: 수정주가 반영 여부.

        Returns:
            :class:`~kiwoompy.models.StockYearChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "stk_cd":       stock_code,
                "base_dt":      base_date,
                "upd_stkpc_tp": _CHART_ADJ_CODE[adjusted],
            },
            headers=self._headers("ka10094"),
        ))
        items = [
            StockYearChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                trde_prica=item.get("trde_prica", ""),
                dt=item.get("dt", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
            )
            for item in raw.get("stk_yr_pole_chart_qry", [])
        ]
        return StockYearChart(stk_cd=raw.get("stk_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka10060 — 종목별투자자기관별차트요청
    # -----------------------------------------------------------------------

    def get_investor_chart(
        self,
        date: str,
        stock_code: str,
        amt_qty_type: "ChartAmtQtyType",
        trade_type: "ChartTradeType",
        unit_type: "ChartUnitType",
    ) -> InvestorChart:
        """종목별 투자자기관별 차트 데이터를 조회한다 (ka10060).

        Args:
            date: 조회일자 (``"YYYYMMDD"``).
            stock_code: 거래소별 종목코드.
            amt_qty_type: 금액수량구분 (``"amount"`` 금액 / ``"qty"`` 수량).
            trade_type: 매매구분 (``"net_buy"`` 순매수 / ``"buy"`` 매수 / ``"sell"`` 매도).
            unit_type: 단위구분 (``"thousand"`` 천주 / ``"single"`` 단주).

        Returns:
            :class:`~kiwoompy.models.InvestorChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "dt":         date,
                "stk_cd":     stock_code,
                "amt_qty_tp": _CHART_AMT_QTY_CODE[amt_qty_type],
                "trde_tp":    _CHART_TRADE_CODE[trade_type],
                "unit_tp":    _CHART_UNIT_CODE[unit_type],
            },
            headers=self._headers("ka10060"),
        ))
        items = [
            InvestorChartItem(
                dt=item.get("dt", ""),
                cur_prc=item.get("cur_prc", ""),
                pred_pre=item.get("pred_pre", ""),
                acc_trde_prica=item.get("acc_trde_prica", ""),
                ind_invsr=item.get("ind_invsr", ""),
                frgnr_invsr=item.get("frgnr_invsr", ""),
                orgn=item.get("orgn", ""),
                fnnc_invt=item.get("fnnc_invt", ""),
                insrnc=item.get("insrnc", ""),
                invtrt=item.get("invtrt", ""),
                etc_fnnc=item.get("etc_fnnc", ""),
                bank=item.get("bank", ""),
                penfnd_etc=item.get("penfnd_etc", ""),
                samo_fund=item.get("samo_fund", ""),
                natn=item.get("natn", ""),
                etc_corp=item.get("etc_corp", ""),
                natfor=item.get("natfor", ""),
            )
            for item in raw.get("stk_invsr_orgn_chart", [])
        ]
        return InvestorChart(items=items)

    # -----------------------------------------------------------------------
    # ka10064 — 장중투자자별매매차트요청
    # -----------------------------------------------------------------------

    def get_intra_investor_chart(
        self,
        market: "ChartSectorMarket",
        stock_code: str,
        amt_qty_type: "ChartAmtQtyType",
        trade_type: "ChartTradeType",
    ) -> IntraInvestorChart:
        """장중 투자자별 매매 차트 데이터를 조회한다 (ka10064).

        Args:
            market: 시장구분 (``"kospi"`` / ``"kosdaq"`` / ``"kospi200"``).
            stock_code: 거래소별 종목코드.
            amt_qty_type: 금액수량구분 (``"amount"`` 금액 / ``"qty"`` 수량).
            trade_type: 매매구분 (``"net_buy"`` 순매수 / ``"buy"`` 매수 / ``"sell"`` 매도).

        Returns:
            :class:`~kiwoompy.models.IntraInvestorChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "mrkt_tp":    _CHART_SECTOR_MARKET_CODE[market],
                "amt_qty_tp": _CHART_AMT_QTY_CODE[amt_qty_type],
                "trde_tp":    _CHART_TRADE_CODE[trade_type],
                "stk_cd":     stock_code,
            },
            headers=self._headers("ka10064"),
        ))
        items = [
            IntraInvestorChartItem(
                tm=item.get("tm", ""),
                frgnr_invsr=item.get("frgnr_invsr", ""),
                orgn=item.get("orgn", ""),
                invtrt=item.get("invtrt", ""),
                insrnc=item.get("insrnc", ""),
                bank=item.get("bank", ""),
                penfnd_etc=item.get("penfnd_etc", ""),
                etc_corp=item.get("etc_corp", ""),
                natn=item.get("natn", ""),
            )
            for item in raw.get("opmr_invsr_trde_chart", [])
        ]
        return IntraInvestorChart(items=items)

    # -----------------------------------------------------------------------
    # ka20004 — 업종틱차트조회요청
    # -----------------------------------------------------------------------

    def get_sector_tick_chart(
        self,
        sector_code: str,
        tick_scope: "ChartTickScope",
    ) -> SectorTickChart:
        """업종 틱 차트 데이터를 조회한다 (ka20004).

        Args:
            sector_code: 업종코드 (예: ``"001"`` 종합KOSPI, ``"101"`` 종합KOSDAQ).
            tick_scope: 틱 범위 (``"1"`` / ``"3"`` / ``"5"`` / ``"10"`` / ``"30"``).

        Returns:
            :class:`~kiwoompy.models.SectorTickChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "inds_cd":   sector_code,
                "tic_scope": tick_scope,
            },
            headers=self._headers("ka20004"),
        ))
        items = [
            SectorCandleItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                cntr_tm=item.get("cntr_tm", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                pred_pre=item.get("pred_pre", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
            )
            for item in raw.get("inds_tic_chart_qry", [])
        ]
        return SectorTickChart(inds_cd=raw.get("inds_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka20005 — 업종분봉조회요청
    # -----------------------------------------------------------------------

    def get_sector_min_chart(
        self,
        sector_code: str,
        min_scope: "ChartMinScope",
        base_date: str = "",
    ) -> SectorMinChart:
        """업종 분봉 차트 데이터를 조회한다 (ka20005).

        Args:
            sector_code: 업종코드.
            min_scope: 분봉 범위 (``"1"`` / ``"3"`` / ``"5"`` / ``"10"`` / ``"15"`` / ``"30"`` / ``"45"`` / ``"60"``).
            base_date: 기준일자 (``"YYYYMMDD"``, 생략 시 최신).

        Returns:
            :class:`~kiwoompy.models.SectorMinChart` 인스턴스.
        """
        body: dict = {
            "inds_cd":   sector_code,
            "tic_scope": min_scope,
        }
        if base_date:
            body["base_dt"] = base_date
        raw = _check(self._api.post(
            self._CHART_PATH,
            body,
            headers=self._headers("ka20005"),
        ))
        items = [
            SectorMinChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                cntr_tm=item.get("cntr_tm", item.get("dt", "")),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                acc_trde_qty=item.get("acc_trde_qty", ""),
                pred_pre=item.get("pred_pre", ""),
                pred_pre_sig=item.get("pred_pre_sig", ""),
            )
            for item in raw.get("inds_min_pole_qry", [])
        ]
        return SectorMinChart(inds_cd=raw.get("inds_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka20006 — 업종일봉조회요청
    # -----------------------------------------------------------------------

    def get_sector_day_chart(
        self,
        sector_code: str,
        base_date: str,
    ) -> SectorDayChart:
        """업종 일봉 차트 데이터를 조회한다 (ka20006).

        Args:
            sector_code: 업종코드.
            base_date: 기준일자 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.SectorDayChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "inds_cd": sector_code,
                "base_dt": base_date,
            },
            headers=self._headers("ka20006"),
        ))
        items = [
            SectorDayChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                dt=item.get("dt", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                trde_prica=item.get("trde_prica", ""),
            )
            for item in raw.get("inds_dt_pole_qry", [])
        ]
        return SectorDayChart(inds_cd=raw.get("inds_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka20007 — 업종주봉조회요청
    # -----------------------------------------------------------------------

    def get_sector_week_chart(
        self,
        sector_code: str,
        base_date: str,
    ) -> SectorWeekChart:
        """업종 주봉 차트 데이터를 조회한다 (ka20007).

        Args:
            sector_code: 업종코드.
            base_date: 기준일자 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.SectorWeekChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "inds_cd": sector_code,
                "base_dt": base_date,
            },
            headers=self._headers("ka20007"),
        ))
        items = [
            SectorDayChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                dt=item.get("dt", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                trde_prica=item.get("trde_prica", ""),
            )
            for item in raw.get("inds_stk_pole_qry", [])
        ]
        return SectorWeekChart(inds_cd=raw.get("inds_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka20008 — 업종월봉조회요청
    # -----------------------------------------------------------------------

    def get_sector_month_chart(
        self,
        sector_code: str,
        base_date: str,
    ) -> SectorMonthChart:
        """업종 월봉 차트 데이터를 조회한다 (ka20008).

        Args:
            sector_code: 업종코드.
            base_date: 기준일자 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.SectorMonthChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "inds_cd": sector_code,
                "base_dt": base_date,
            },
            headers=self._headers("ka20008"),
        ))
        items = [
            SectorDayChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                dt=item.get("dt", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                trde_prica=item.get("trde_prica", ""),
            )
            for item in raw.get("inds_mth_pole_qry", [])
        ]
        return SectorMonthChart(inds_cd=raw.get("inds_cd", ""), items=items)

    # -----------------------------------------------------------------------
    # ka20019 — 업종년봉조회요청
    # -----------------------------------------------------------------------

    def get_sector_year_chart(
        self,
        sector_code: str,
        base_date: str,
    ) -> SectorYearChart:
        """업종 년봉 차트 데이터를 조회한다 (ka20019).

        Args:
            sector_code: 업종코드.
            base_date: 기준일자 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.SectorYearChart` 인스턴스.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {
                "inds_cd": sector_code,
                "base_dt": base_date,
            },
            headers=self._headers("ka20019"),
        ))
        items = [
            SectorDayChartItem(
                cur_prc=item.get("cur_prc", ""),
                trde_qty=item.get("trde_qty", ""),
                dt=item.get("dt", ""),
                open_pric=item.get("open_pric", ""),
                high_pric=item.get("high_pric", ""),
                low_pric=item.get("low_pric", ""),
                trde_prica=item.get("trde_prica", ""),
            )
            for item in raw.get("inds_yr_pole_qry", [])
        ]
        return SectorYearChart(inds_cd=raw.get("inds_cd", ""), items=items)

    # =======================================================================
    # 7단계 — 업종·기관/외국인·공매도·대차거래 (sect / frgnistt / shsa / slb)
    # =======================================================================

    # -----------------------------------------------------------------------
    # ka10010 — 업종프로그램요청
    # -----------------------------------------------------------------------

    def get_sector_program(self, stock_code: str) -> SectorProgram:
        """업종 프로그램 매매 정보를 조회한다 (ka10010).

        Args:
            stock_code: 거래소별 종목코드 (예: ``"005930"``, ``"039490_NX"``).

        Returns:
            :class:`~kiwoompy.models.SectorProgram` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SECT_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10010"),
        ))
        return SectorProgram(
            dfrt_trst_sell_qty=raw.get("dfrt_trst_sell_qty", ""),
            dfrt_trst_sell_amt=raw.get("dfrt_trst_sell_amt", ""),
            dfrt_trst_buy_qty=raw.get("dfrt_trst_buy_qty", ""),
            dfrt_trst_buy_amt=raw.get("dfrt_trst_buy_amt", ""),
            dfrt_trst_netprps_qty=raw.get("dfrt_trst_netprps_qty", ""),
            dfrt_trst_netprps_amt=raw.get("dfrt_trst_netprps_amt", ""),
            ndiffpro_trst_sell_qty=raw.get("ndiffpro_trst_sell_qty", ""),
            ndiffpro_trst_sell_amt=raw.get("ndiffpro_trst_sell_amt", ""),
            ndiffpro_trst_buy_qty=raw.get("ndiffpro_trst_buy_qty", ""),
            ndiffpro_trst_buy_amt=raw.get("ndiffpro_trst_buy_amt", ""),
            ndiffpro_trst_netprps_qty=raw.get("ndiffpro_trst_netprps_qty", ""),
            ndiffpro_trst_netprps_amt=raw.get("ndiffpro_trst_netprps_amt", ""),
            all_dfrt_trst_sell_qty=raw.get("all_dfrt_trst_sell_qty", ""),
            all_dfrt_trst_sell_amt=raw.get("all_dfrt_trst_sell_amt", ""),
            all_dfrt_trst_buy_qty=raw.get("all_dfrt_trst_buy_qty", ""),
            all_dfrt_trst_buy_amt=raw.get("all_dfrt_trst_buy_amt", ""),
            all_dfrt_trst_netprps_qty=raw.get("all_dfrt_trst_netprps_qty", ""),
            all_dfrt_trst_netprps_amt=raw.get("all_dfrt_trst_netprps_amt", ""),
        )

    # -----------------------------------------------------------------------
    # ka10051 — 업종별투자자순매수요청
    # -----------------------------------------------------------------------

    def get_sector_investor_net_buy(
        self,
        market: "SectMrktType",
        amt_qty: "SectAmtQtyType",
        base_date: str = "",
        exchange: "SectExchangeType" = "all",
    ) -> SectorInvestorNetBuy:
        """업종별 투자자 순매수 현황을 조회한다 (ka10051).

        Args:
            market: 시장구분 (``"kospi"`` / ``"kosdaq"`` / ``"kospi200"``).
            amt_qty: 금액수량구분 (``"amount"`` / ``"qty"``).
            base_date: 기준일자 (``"YYYYMMDD"``). 생략 시 당일.
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``). 기본 ``"all"``.

        Returns:
            :class:`~kiwoompy.models.SectorInvestorNetBuy` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SECT_PATH,
            {
                "mrkt_tp":   _SECT_MRKT_CODE[market],
                "amt_qty_tp": _SECT_AMT_QTY_CODE[amt_qty],
                "base_dt":   base_date,
                "stex_tp":   _SECT_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10051"),
        ))
        items = [
            SectorInvestorNetBuyItem(
                inds_cd=it.get("inds_cd", ""),
                inds_nm=it.get("inds_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_smbol=it.get("pre_smbol", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                sc_netprps=it.get("sc_netprps", ""),
                insrnc_netprps=it.get("insrnc_netprps", ""),
                invtrt_netprps=it.get("invtrt_netprps", ""),
                bank_netprps=it.get("bank_netprps", ""),
                jnsinkm_netprps=it.get("jnsinkm_netprps", ""),
                endw_netprps=it.get("endw_netprps", ""),
                etc_corp_netprps=it.get("etc_corp_netprps", ""),
                ind_netprps=it.get("ind_netprps", ""),
                frgnr_netprps=it.get("frgnr_netprps", ""),
                native_trmt_frgnr_netprps=it.get("native_trmt_frgnr_netprps", ""),
                natn_netprps=it.get("natn_netprps", ""),
                samo_fund_netprps=it.get("samo_fund_netprps", ""),
                orgn_netprps=it.get("orgn_netprps", ""),
            )
            for it in raw.get("inds_netprps", [])
        ]
        return SectorInvestorNetBuy(items=items)

    # -----------------------------------------------------------------------
    # ka20001 — 업종현재가요청
    # -----------------------------------------------------------------------

    def get_sector_price(
        self,
        market: "SectMrktType",
        sector_code: str,
    ) -> SectorPrice:
        """업종 현재가 정보를 조회한다 (ka20001).

        Args:
            market: 시장구분 (``"kospi"`` / ``"kosdaq"`` / ``"kospi200"``).
            sector_code: 업종코드 (예: ``"001"``).

        Returns:
            :class:`~kiwoompy.models.SectorPrice` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SECT_PATH,
            {
                "mrkt_tp": _SECT_MRKT_CODE[market],
                "inds_cd": sector_code,
            },
            headers=self._headers("ka20001"),
        ))
        items = [
            SectorPriceTmItem(
                tm_n=it.get("tm_n", ""),
                cur_prc_n=it.get("cur_prc_n", ""),
                pred_pre_sig_n=it.get("pred_pre_sig_n", ""),
                pred_pre_n=it.get("pred_pre_n", ""),
                flu_rt_n=it.get("flu_rt_n", ""),
                trde_qty_n=it.get("trde_qty_n", ""),
                acc_trde_qty_n=it.get("acc_trde_qty_n", ""),
            )
            for it in raw.get("inds_cur_prc_tm", [])
        ]
        return SectorPrice(
            cur_prc=raw.get("cur_prc", ""),
            pred_pre_sig=raw.get("pred_pre_sig", ""),
            pred_pre=raw.get("pred_pre", ""),
            flu_rt=raw.get("flu_rt", ""),
            trde_qty=raw.get("trde_qty", ""),
            trde_prica=raw.get("trde_prica", ""),
            trde_frmatn_stk_num=raw.get("trde_frmatn_stk_num", ""),
            trde_frmatn_rt=raw.get("trde_frmatn_rt", ""),
            open_pric=raw.get("open_pric", ""),
            high_pric=raw.get("high_pric", ""),
            low_pric=raw.get("low_pric", ""),
            upl=raw.get("upl", ""),
            rising=raw.get("rising", ""),
            stdns=raw.get("stdns", ""),
            fall=raw.get("fall", ""),
            lst=raw.get("lst", ""),
            wk52_hgst_pric=raw.get("52wk_hgst_pric", ""),
            wk52_hgst_pric_dt=raw.get("52wk_hgst_pric_dt", ""),
            wk52_hgst_pric_pre_rt=raw.get("52wk_hgst_pric_pre_rt", ""),
            wk52_lwst_pric=raw.get("52wk_lwst_pric", ""),
            wk52_lwst_pric_dt=raw.get("52wk_lwst_pric_dt", ""),
            wk52_lwst_pric_pre_rt=raw.get("52wk_lwst_pric_pre_rt", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka20002 — 업종별주가요청
    # -----------------------------------------------------------------------

    def get_sector_stock_prices(
        self,
        market: "SectMrktType",
        sector_code: str,
        exchange: "SectExchangeType" = "krx",
    ) -> SectorStockPrices:
        """업종 내 구성 종목별 주가를 조회한다 (ka20002).

        Args:
            market: 시장구분 (``"kospi"`` / ``"kosdaq"`` / ``"kospi200"``).
            sector_code: 업종코드 (예: ``"001"``).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``). 기본 ``"krx"``.

        Returns:
            :class:`~kiwoompy.models.SectorStockPrices` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SECT_PATH,
            {
                "mrkt_tp": _SECT_MRKT_CODE[market],
                "inds_cd": sector_code,
                "stex_tp": _SECT_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka20002"),
        ))
        items = [
            SectorStockPriceItem(
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                pred_pre_sig=it.get("pred_pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                now_trde_qty=it.get("now_trde_qty", ""),
                sel_bid=it.get("sel_bid", ""),
                buy_bid=it.get("buy_bid", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
            )
            for it in raw.get("inds_stkpc", [])
        ]
        return SectorStockPrices(items=items)

    # -----------------------------------------------------------------------
    # ka20003 — 전업종지수요청
    # -----------------------------------------------------------------------

    def get_all_sector_index(self, sector_code: str) -> AllSectorIndex:
        """전 업종 지수를 조회한다 (ka20003).

        Args:
            sector_code: 업종코드 (``"001"``: 코스피 종합, ``"101"``: 코스닥 종합).

        Returns:
            :class:`~kiwoompy.models.AllSectorIndex` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SECT_PATH,
            {"inds_cd": sector_code},
            headers=self._headers("ka20003"),
        ))
        items = [
            AllSectorIndexItem(
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                wght=it.get("wght", ""),
                trde_prica=it.get("trde_prica", ""),
                upl=it.get("upl", ""),
                rising=it.get("rising", ""),
                stdns=it.get("stdns", ""),
                fall=it.get("fall", ""),
                lst=it.get("lst", ""),
                flo_stk_num=it.get("flo_stk_num", ""),
            )
            for it in raw.get("all_inds_idex", [])
        ]
        return AllSectorIndex(items=items)

    # -----------------------------------------------------------------------
    # ka20009 — 업종현재가일별요청
    # -----------------------------------------------------------------------

    def get_sector_daily_price(
        self,
        market: "SectMrktType",
        sector_code: str,
    ) -> SectorDailyPrice:
        """업종 현재가 일별 데이터를 조회한다 (ka20009).

        Args:
            market: 시장구분 (``"kospi"`` / ``"kosdaq"`` / ``"kospi200"``).
            sector_code: 업종코드 (예: ``"001"``).

        Returns:
            :class:`~kiwoompy.models.SectorDailyPrice` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SECT_PATH,
            {
                "mrkt_tp": _SECT_MRKT_CODE[market],
                "inds_cd": sector_code,
            },
            headers=self._headers("ka20009"),
        ))
        items = [
            SectorDailyPriceItem(
                dt_n=it.get("dt_n", ""),
                cur_prc_n=it.get("cur_prc_n", ""),
                pred_pre_sig_n=it.get("pred_pre_sig_n", ""),
                pred_pre_n=it.get("pred_pre_n", ""),
                flu_rt_n=it.get("flu_rt_n", ""),
                acc_trde_qty_n=it.get("acc_trde_qty_n", ""),
            )
            for it in raw.get("inds_cur_prc_daly_rept", [])
        ]
        return SectorDailyPrice(
            cur_prc=raw.get("cur_prc", ""),
            pred_pre_sig=raw.get("pred_pre_sig", ""),
            pred_pre=raw.get("pred_pre", ""),
            flu_rt=raw.get("flu_rt", ""),
            trde_qty=raw.get("trde_qty", ""),
            trde_prica=raw.get("trde_prica", ""),
            trde_frmatn_stk_num=raw.get("trde_frmatn_stk_num", ""),
            trde_frmatn_rt=raw.get("trde_frmatn_rt", ""),
            open_pric=raw.get("open_pric", ""),
            high_pric=raw.get("high_pric", ""),
            low_pric=raw.get("low_pric", ""),
            upl=raw.get("upl", ""),
            rising=raw.get("rising", ""),
            stdns=raw.get("stdns", ""),
            fall=raw.get("fall", ""),
            lst=raw.get("lst", ""),
            wk52_hgst_pric=raw.get("52wk_hgst_pric", ""),
            wk52_hgst_pric_dt=raw.get("52wk_hgst_pric_dt", ""),
            wk52_hgst_pric_pre_rt=raw.get("52wk_hgst_pric_pre_rt", ""),
            wk52_lwst_pric=raw.get("52wk_lwst_pric", ""),
            wk52_lwst_pric_dt=raw.get("52wk_lwst_pric_dt", ""),
            wk52_lwst_pric_pre_rt=raw.get("52wk_lwst_pric_pre_rt", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka10008 — 주식외국인종목별매매동향
    # -----------------------------------------------------------------------

    def get_foreign_trade_trend(self, stock_code: str) -> ForeignTrade:
        """종목별 외국인 매매동향을 조회한다 (ka10008).

        Args:
            stock_code: 거래소별 종목코드 (예: ``"005930"``, ``"039490_NX"``).

        Returns:
            :class:`~kiwoompy.models.ForeignTrade` 인스턴스.
        """
        raw = _check(self._api.post(
            self._FRGNISTT_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10008"),
        ))
        items = [
            ForeignTradeItem(
                dt=it.get("dt", ""),
                close_pric=it.get("close_pric", ""),
                pred_pre=it.get("pred_pre", ""),
                trde_qty=it.get("trde_qty", ""),
                chg_qty=it.get("chg_qty", ""),
                poss_stkcnt=it.get("poss_stkcnt", ""),
                wght=it.get("wght", ""),
                gain_pos_stkcnt=it.get("gain_pos_stkcnt", ""),
                frgnr_limit=it.get("frgnr_limit", ""),
                frgnr_limit_irds=it.get("frgnr_limit_irds", ""),
                limit_exh_rt=it.get("limit_exh_rt", ""),
            )
            for it in raw.get("stk_frgnr", [])
        ]
        return ForeignTrade(items=items)

    # -----------------------------------------------------------------------
    # ka10009 — 주식기관요청
    # -----------------------------------------------------------------------

    def get_institution_trade(self, stock_code: str) -> InstitutionTrade:
        """종목별 기관 매매 현황을 조회한다 (ka10009).

        Args:
            stock_code: 거래소별 종목코드 (예: ``"005930"``, ``"039490_NX"``).

        Returns:
            :class:`~kiwoompy.models.InstitutionTrade` 인스턴스.
        """
        raw = _check(self._api.post(
            self._FRGNISTT_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10009"),
        ))
        return InstitutionTrade(
            date=raw.get("date", ""),
            close_pric=raw.get("close_pric", ""),
            pre=raw.get("pre", ""),
            orgn_dt_acc=raw.get("orgn_dt_acc", ""),
            orgn_daly_nettrde=raw.get("orgn_daly_nettrde", ""),
            frgnr_daly_nettrde=raw.get("frgnr_daly_nettrde", ""),
            frgnr_qota_rt=raw.get("frgnr_qota_rt", ""),
        )

    # -----------------------------------------------------------------------
    # ka10131 — 기관외국인연속매매현황요청
    # -----------------------------------------------------------------------

    def get_inst_frgn_consecutive_trade(
        self,
        duration: "FrgnDuration",
        market: str,
        stock_or_sector: "FrgnStockSectType",
        amt_qty: "SectAmtQtyType",
        exchange: "SectExchangeType" = "krx",
        start_date: str = "",
        end_date: str = "",
    ) -> InstFrgnConsecutiveTrade:
        """기관·외국인 연속 매매 현황을 조회한다 (ka10131).

        Args:
            duration: 기간 (``"1"`` / ``"3"`` / ``"5"`` / ``"10"`` / ``"20"``
                / ``"120"`` / ``"custom"``). ``"custom"`` 선택 시
                ``start_date`` / ``end_date`` 필수.
            market: 장구분 코드 (``"001"``: 코스피, ``"101"``: 코스닥).
            stock_or_sector: 종목업종구분 (``"stock"`` / ``"sector"``).
            amt_qty: 금액수량구분 (``"amount"`` / ``"qty"``).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``). 기본 ``"krx"``.
            start_date: 시작일자 (``"YYYYMMDD"``). ``duration="custom"`` 일 때 사용.
            end_date: 종료일자 (``"YYYYMMDD"``). ``duration="custom"`` 일 때 사용.

        Returns:
            :class:`~kiwoompy.models.InstFrgnConsecutiveTrade` 인스턴스.
        """
        raw = _check(self._api.post(
            self._FRGNISTT_PATH,
            {
                "dt":          _FRGN_DURATION_CODE[duration],
                "strt_dt":     start_date,
                "end_dt":      end_date,
                "mrkt_tp":     market,
                "netslmt_tp":  "2",
                "stk_inds_tp": _FRGN_STK_SECT_CODE[stock_or_sector],
                "amt_qty_tp":  _SECT_AMT_QTY_CODE[amt_qty],
                "stex_tp":     _SECT_EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka10131"),
        ))
        items = [
            InstFrgnConsecutiveItem(
                rank=it.get("rank", ""),
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                prid_stkpc_flu_rt=it.get("prid_stkpc_flu_rt", ""),
                orgn_nettrde_amt=it.get("orgn_nettrde_amt", ""),
                orgn_nettrde_qty=it.get("orgn_nettrde_qty", ""),
                orgn_cont_netprps_dys=it.get("orgn_cont_netprps_dys", ""),
                orgn_cont_netprps_qty=it.get("orgn_cont_netprps_qty", ""),
                orgn_cont_netprps_amt=it.get("orgn_cont_netprps_amt", ""),
                frgnr_nettrde_qty=it.get("frgnr_nettrde_qty", ""),
                frgnr_nettrde_amt=it.get("frgnr_nettrde_amt", ""),
                frgnr_cont_netprps_dys=it.get("frgnr_cont_netprps_dys", ""),
                frgnr_cont_netprps_qty=it.get("frgnr_cont_netprps_qty", ""),
                frgnr_cont_netprps_amt=it.get("frgnr_cont_netprps_amt", ""),
                nettrde_qty=it.get("nettrde_qty", ""),
                nettrde_amt=it.get("nettrde_amt", ""),
                tot_cont_netprps_dys=it.get("tot_cont_netprps_dys", ""),
                tot_cont_nettrde_qty=it.get("tot_cont_nettrde_qty", ""),
                tot_cont_netprps_amt=it.get("tot_cont_netprps_amt", ""),
            )
            for it in raw.get("orgn_frgnr_cont_trde_prst", [])
        ]
        return InstFrgnConsecutiveTrade(items=items)

    # -----------------------------------------------------------------------
    # ka10014 — 공매도추이요청
    # -----------------------------------------------------------------------

    def get_short_sell_trend(
        self,
        stock_code: str,
        start_date: str,
        end_date: str,
        time_type: str = "1",
    ) -> ShortSellTrend:
        """종목별 공매도 추이를 조회한다 (ka10014).

        Args:
            stock_code: 거래소별 종목코드 (예: ``"005930"``).
            start_date: 시작일자 (``"YYYYMMDD"``).
            end_date: 종료일자 (``"YYYYMMDD"``).
            time_type: 시간구분 (``"0"``: 시작일, ``"1"``: 기간). 기본 ``"1"``.

        Returns:
            :class:`~kiwoompy.models.ShortSellTrend` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SHSA_PATH,
            {
                "stk_cd":  stock_code,
                "tm_tp":   time_type,
                "strt_dt": start_date,
                "end_dt":  end_date,
            },
            headers=self._headers("ka10014"),
        ))
        items = [
            ShortSellItem(
                dt=it.get("dt", ""),
                close_pric=it.get("close_pric", ""),
                pred_pre_sig=it.get("pred_pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                shrts_qty=it.get("shrts_qty", ""),
                ovr_shrts_qty=it.get("ovr_shrts_qty", ""),
                trde_wght=it.get("trde_wght", ""),
                shrts_trde_prica=it.get("shrts_trde_prica", ""),
                shrts_avg_pric=it.get("shrts_avg_pric", ""),
            )
            for it in raw.get("shrts_trnsn", [])
        ]
        return ShortSellTrend(items=items)

    # -----------------------------------------------------------------------
    # ka10068 — 대차거래추이요청
    # -----------------------------------------------------------------------

    def get_stock_loan_trend(
        self,
        start_date: str = "",
        end_date: str = "",
    ) -> StockLoanTrend:
        """전체 대차거래 추이를 조회한다 (ka10068).

        Args:
            start_date: 시작일자 (``"YYYYMMDD"``).
            end_date: 종료일자 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.StockLoanTrend` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SLB_PATH,
            {
                "strt_dt": start_date,
                "end_dt":  end_date,
                "all_tp":  "1",
            },
            headers=self._headers("ka10068"),
        ))
        items = [
            StockLoanItem(
                dt=it.get("dt", ""),
                dbrt_trde_cntrcnt=it.get("dbrt_trde_cntrcnt", ""),
                dbrt_trde_rpy=it.get("dbrt_trde_rpy", ""),
                dbrt_trde_irds=it.get("dbrt_trde_irds", ""),
                rmnd=it.get("rmnd", ""),
                remn_amt=it.get("remn_amt", ""),
            )
            for it in raw.get("dbrt_trde_trnsn", [])
        ]
        return StockLoanTrend(items=items)

    # -----------------------------------------------------------------------
    # ka10069 — 대차거래상위10종목요청
    # -----------------------------------------------------------------------

    def get_stock_loan_top10(
        self,
        start_date: str,
        market: "SlbMrktType",
        end_date: str = "",
    ) -> StockLoanTop10:
        """대차거래 상위 10종목을 조회한다 (ka10069).

        Args:
            start_date: 시작일자 (``"YYYYMMDD"``).
            market: 시장구분 (``"kospi"`` / ``"kosdaq"``).
            end_date: 종료일자 (``"YYYYMMDD"``). 생략 가능.

        Returns:
            :class:`~kiwoompy.models.StockLoanTop10` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SLB_PATH,
            {
                "strt_dt": start_date,
                "end_dt":  end_date,
                "mrkt_tp": _SLB_MRKT_CODE[market],
            },
            headers=self._headers("ka10069"),
        ))
        items = [
            StockLoanTop10Item(
                stk_nm=it.get("stk_nm", ""),
                stk_cd=it.get("stk_cd", ""),
                dbrt_trde_cntrcnt=it.get("dbrt_trde_cntrcnt", ""),
                dbrt_trde_rpy=it.get("dbrt_trde_rpy", ""),
                rmnd=it.get("rmnd", ""),
                remn_amt=it.get("remn_amt", ""),
            )
            for it in raw.get("dbrt_trde_upper_10stk", [])
        ]
        return StockLoanTop10(
            dbrt_trde_cntrcnt_sum=raw.get("dbrt_trde_cntrcnt_sum", ""),
            dbrt_trde_rpy_sum=raw.get("dbrt_trde_rpy_sum", ""),
            rmnd_sum=raw.get("rmnd_sum", ""),
            remn_amt_sum=raw.get("remn_amt_sum", ""),
            dbrt_trde_cntrcnt_rt=raw.get("dbrt_trde_cntrcnt_rt", ""),
            dbrt_trde_rpy_rt=raw.get("dbrt_trde_rpy_rt", ""),
            rmnd_rt=raw.get("rmnd_rt", ""),
            remn_amt_rt=raw.get("remn_amt_rt", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka20068 — 대차거래추이요청(종목별)
    # -----------------------------------------------------------------------

    def get_stock_loan_trend_by_stock(
        self,
        stock_code: str,
        start_date: str = "",
        end_date: str = "",
    ) -> StockLoanByStock:
        """종목별 대차거래 추이를 조회한다 (ka20068).

        Args:
            stock_code: 종목코드 (예: ``"005930"``).
            start_date: 시작일자 (``"YYYYMMDD"``).
            end_date: 종료일자 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.StockLoanByStock` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SLB_PATH,
            {
                "strt_dt": start_date,
                "end_dt":  end_date,
                "all_tp":  "0",
                "stk_cd":  stock_code,
            },
            headers=self._headers("ka20068"),
        ))
        items = [
            StockLoanByStockItem(
                dt=it.get("dt", ""),
                dbrt_trde_cntrcnt=it.get("dbrt_trde_cntrcnt", ""),
                dbrt_trde_rpy=it.get("dbrt_trde_rpy", ""),
                dbrt_trde_irds=it.get("dbrt_trde_irds", ""),
                rmnd=it.get("rmnd", ""),
                remn_amt=it.get("remn_amt", ""),
            )
            for it in raw.get("dbrt_trde_trnsn", [])
        ]
        return StockLoanByStock(items=items)

    # -----------------------------------------------------------------------
    # ka90012 — 대차거래내역요청
    # -----------------------------------------------------------------------

    def get_stock_loan_history(
        self,
        date: str,
        market: "SlbMrktType",
    ) -> StockLoanHistory:
        """일자별 대차거래 내역을 조회한다 (ka90012).

        Args:
            date: 조회일자 (``"YYYYMMDD"``).
            market: 시장구분 (``"kospi"`` / ``"kosdaq"``).

        Returns:
            :class:`~kiwoompy.models.StockLoanHistory` 인스턴스.
        """
        raw = _check(self._api.post(
            self._SLB_PATH,
            {
                "dt":      date,
                "mrkt_tp": _SLB_MRKT_CODE[market],
            },
            headers=self._headers("ka90012"),
        ))
        items = [
            StockLoanHistoryItem(
                stk_nm=it.get("stk_nm", ""),
                stk_cd=it.get("stk_cd", ""),
                dbrt_trde_cntrcnt=it.get("dbrt_trde_cntrcnt", ""),
                dbrt_trde_rpy=it.get("dbrt_trde_rpy", ""),
                rmnd=it.get("rmnd", ""),
                remn_amt=it.get("remn_amt", ""),
            )
            for it in raw.get("dbrt_trde_prps", [])
        ]
        return StockLoanHistory(items=items)

    # =======================================================================
    # 8단계 — ETF·ELW·테마·프로그램매매 (etf / elw / thme / mrkcond / stkinfo)
    # =======================================================================

    # -----------------------------------------------------------------------
    # ka40001 — ETF수익율요청
    # -----------------------------------------------------------------------

    def get_etf_return(
        self,
        stock_code: str,
        index_code: str,
        duration: "EtfDuration",
    ) -> EtfReturn:
        """ETF 수익율을 조회한다 (ka40001).

        Args:
            stock_code: ETF 종목코드 (예: ``"069500"``).
            index_code: ETF 대상지수코드 (예: ``"207"``).
            duration: 기간 (``"1w"`` / ``"1m"`` / ``"6m"`` / ``"1y"``).

        Returns:
            :class:`~kiwoompy.models.EtfReturn` 인스턴스.
        """
        from kiwoompy.models import EtfDuration  # noqa: F401
        raw = _check(self._api.post(
            self._ETF_PATH,
            {
                "stk_cd":          stock_code,
                "etfobjt_idex_cd": index_code,
                "dt":              _ETF_DURATION_CODE[duration],
            },
            headers=self._headers("ka40001"),
        ))
        items = [
            EtfReturnItem(
                etfprft_rt=it.get("etfprft_rt", ""),
                cntr_prft_rt=it.get("cntr_prft_rt", ""),
                for_netprps_qty=it.get("for_netprps_qty", ""),
                orgn_netprps_qty=it.get("orgn_netprps_qty", ""),
            )
            for it in raw.get("etfprft_rt_lst", [])
        ]
        return EtfReturn(items=items)

    # -----------------------------------------------------------------------
    # ka40002 — ETF종목정보요청
    # -----------------------------------------------------------------------

    def get_etf_info(self, stock_code: str) -> EtfInfo:
        """ETF 종목 기본정보를 조회한다 (ka40002).

        Args:
            stock_code: ETF 종목코드 (예: ``"069500"``).

        Returns:
            :class:`~kiwoompy.models.EtfInfo` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ETF_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka40002"),
        ))
        return EtfInfo(
            stk_nm=raw.get("stk_nm", ""),
            etfobjt_idex_nm=raw.get("etfobjt_idex_nm", ""),
            wonju_pric=raw.get("wonju_pric", ""),
            etftxon_type=raw.get("etftxon_type", ""),
            etntxon_type=raw.get("etntxon_type", ""),
        )

    # -----------------------------------------------------------------------
    # ka40003 — ETF일별추이요청
    # -----------------------------------------------------------------------

    def get_etf_daily_trend(self, stock_code: str) -> EtfDailyTrend:
        """ETF 일별 추이를 조회한다 (ka40003).

        Args:
            stock_code: ETF 종목코드 (예: ``"069500"``).

        Returns:
            :class:`~kiwoompy.models.EtfDailyTrend` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ETF_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka40003"),
        ))
        items = [
            EtfDailyTrendItem(
                cntr_dt=it.get("cntr_dt", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                pre_rt=it.get("pre_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                nav=it.get("nav", ""),
                acc_trde_prica=it.get("acc_trde_prica", ""),
                navidex_dispty_rt=it.get("navidex_dispty_rt", ""),
                navetfdispty_rt=it.get("navetfdispty_rt", ""),
                trace_eor_rt=it.get("trace_eor_rt", ""),
                trace_cur_prc=it.get("trace_cur_prc", ""),
                trace_pred_pre=it.get("trace_pred_pre", ""),
                trace_pre_sig=it.get("trace_pre_sig", ""),
            )
            for it in raw.get("etfdaly_trnsn", [])
        ]
        return EtfDailyTrend(items=items)

    # -----------------------------------------------------------------------
    # ka40004 — ETF전체시세요청
    # -----------------------------------------------------------------------

    def get_etf_all_quote(
        self,
        tax_type: str,
        nav_compare: str,
        asset_manager: str,
        tax_yn: str,
        tracking_index: str,
        exchange: "ExchangeType",
    ) -> EtfAllQuote:
        """ETF 전체 시세를 조회한다 (ka40004).

        Args:
            tax_type: 과세유형 (``"0"``전체 / ``"1"``비과세 / ``"2"``보유기간과세 / ``"3"``회사형 / ``"4"``외국 / ``"5"``비과세해외).
            nav_compare: NAV대비 (``"0"``전체 / ``"1"``NAV>전일종가 / ``"2"``NAV<전일종가).
            asset_manager: 운용사코드 (``"0000"``전체 / ``"3020"``KODEX 등).
            tax_yn: 과세여부 (``"0"``전체 / ``"1"``과세 / ``"2"``비과세).
            tracking_index: 추적지수 (``"0"``전체).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).

        Returns:
            :class:`~kiwoompy.models.EtfAllQuote` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ETF_PATH,
            {
                "txon_type":  tax_type,
                "navpre":     nav_compare,
                "mngmcomp":   asset_manager,
                "txon_yn":    tax_yn,
                "trace_idex": tracking_index,
                "stex_tp":    _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka40004"),
        ))
        items = [
            EtfAllQuoteItem(
                stk_cd=it.get("stk_cd", ""),
                stk_cls=it.get("stk_cls", ""),
                stk_nm=it.get("stk_nm", ""),
                close_pric=it.get("close_pric", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                pre_rt=it.get("pre_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                nav=it.get("nav", ""),
                trace_eor_rt=it.get("trace_eor_rt", ""),
                txbs=it.get("txbs", ""),
                dvid_bf_base=it.get("dvid_bf_base", ""),
                pred_dvida=it.get("pred_dvida", ""),
                trace_idex_nm=it.get("trace_idex_nm", ""),
                drng=it.get("drng", ""),
                trace_idex_cd=it.get("trace_idex_cd", ""),
                trace_idex=it.get("trace_idex", ""),
                trace_flu_rt=it.get("trace_flu_rt", ""),
            )
            for it in raw.get("etfall_mrpr", [])
        ]
        return EtfAllQuote(items=items)

    # -----------------------------------------------------------------------
    # ka40006 — ETF시간대별추이요청
    # -----------------------------------------------------------------------

    def get_etf_time_trend(self, stock_code: str) -> EtfTimeTrend:
        """ETF 시간대별 추이를 조회한다 (ka40006).

        Args:
            stock_code: ETF 종목코드 (예: ``"069500"``).

        Returns:
            :class:`~kiwoompy.models.EtfTimeTrend` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ETF_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka40006"),
        ))
        items = [
            EtfTimeTrendItem(
                tm=it.get("tm", ""),
                close_pric=it.get("close_pric", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                nav=it.get("nav", ""),
                trde_prica=it.get("trde_prica", ""),
                navidex=it.get("navidex", ""),
                navetf=it.get("navetf", ""),
                trace=it.get("trace", ""),
                trace_idex=it.get("trace_idex", ""),
                trace_idex_pred_pre=it.get("trace_idex_pred_pre", ""),
                trace_idex_pred_pre_sig=it.get("trace_idex_pred_pre_sig", ""),
            )
            for it in raw.get("etftisl_trnsn", [])
        ]
        return EtfTimeTrend(
            stk_nm=raw.get("stk_nm", ""),
            etfobjt_idex_nm=raw.get("etfobjt_idex_nm", ""),
            wonju_pric=raw.get("wonju_pric", ""),
            etftxon_type=raw.get("etftxon_type", ""),
            etntxon_type=raw.get("etntxon_type", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka40007 — ETF시간대별체결요청
    # -----------------------------------------------------------------------

    def get_etf_time_fill(self, stock_code: str) -> EtfTimeFill:
        """ETF 시간대별 체결을 조회한다 (ka40007).

        Args:
            stock_code: ETF 종목코드 (예: ``"069500"``).

        Returns:
            :class:`~kiwoompy.models.EtfTimeFill` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ETF_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka40007"),
        ))
        items = [
            EtfTimeFillItem(
                cntr_tm=it.get("cntr_tm", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                trde_qty=it.get("trde_qty", ""),
                stex_tp=it.get("stex_tp", ""),
            )
            for it in raw.get("etftisl_cntr_array", [])
        ]
        return EtfTimeFill(
            stk_cls=raw.get("stk_cls", ""),
            stk_nm=raw.get("stk_nm", ""),
            etfobjt_idex_nm=raw.get("etfobjt_idex_nm", ""),
            etfobjt_idex_cd=raw.get("etfobjt_idex_cd", ""),
            objt_idex_pre_rt=raw.get("objt_idex_pre_rt", ""),
            wonju_pric=raw.get("wonju_pric", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka40008 — ETF일자별체결요청
    # -----------------------------------------------------------------------

    def get_etf_daily_fill(self, stock_code: str) -> EtfDailyFill:
        """ETF 일자별 체결을 조회한다 (ka40008).

        Args:
            stock_code: ETF 종목코드 (예: ``"069500"``).

        Returns:
            :class:`~kiwoompy.models.EtfDailyFill` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ETF_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka40008"),
        ))
        items = [
            EtfDailyFillItem(
                dt=it.get("dt", ""),
                cur_prc_n=it.get("cur_prc_n", ""),
                pre_sig_n=it.get("pre_sig_n", ""),
                pred_pre_n=it.get("pred_pre_n", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                for_netprps_qty=it.get("for_netprps_qty", ""),
                orgn_netprps_qty=it.get("orgn_netprps_qty", ""),
            )
            for it in raw.get("etfnetprps_qty_array", [])
        ]
        return EtfDailyFill(
            cntr_tm=raw.get("cntr_tm", ""),
            cur_prc=raw.get("cur_prc", ""),
            pre_sig=raw.get("pre_sig", ""),
            pred_pre=raw.get("pred_pre", ""),
            trde_qty=raw.get("trde_qty", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka40009 — ETF시간대별체결요청 (NAV)
    # -----------------------------------------------------------------------

    def get_etf_nav(self, stock_code: str) -> EtfNav:
        """ETF NAV 데이터를 조회한다 (ka40009).

        Args:
            stock_code: ETF 종목코드 (예: ``"069500"``).

        Returns:
            :class:`~kiwoompy.models.EtfNav` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ETF_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka40009"),
        ))
        items = [
            EtfNavItem(
                nav=it.get("nav", ""),
                navpred_pre=it.get("navpred_pre", ""),
                navflu_rt=it.get("navflu_rt", ""),
                trace_eor_rt=it.get("trace_eor_rt", ""),
                dispty_rt=it.get("dispty_rt", ""),
                stkcnt=it.get("stkcnt", ""),
                base_pric=it.get("base_pric", ""),
                for_rmnd_qty=it.get("for_rmnd_qty", ""),
                repl_pric=it.get("repl_pric", ""),
                conv_pric=it.get("conv_pric", ""),
                drstk=it.get("drstk", ""),
                wonju_pric=it.get("wonju_pric", ""),
            )
            for it in raw.get("etfnavarray", [])
        ]
        return EtfNav(items=items)

    # -----------------------------------------------------------------------
    # ka40010 — ETF시간대별추이요청 (외인순매수)
    # -----------------------------------------------------------------------

    def get_etf_time_trend2(self, stock_code: str) -> EtfTimeTrend2:
        """ETF 시간대별 추이(외인순매수 포함)를 조회한다 (ka40010).

        Args:
            stock_code: ETF 종목코드 (예: ``"069500"``).

        Returns:
            :class:`~kiwoompy.models.EtfTimeTrend2` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ETF_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka40010"),
        ))
        items = [
            EtfTimeTrend2Item(
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                trde_qty=it.get("trde_qty", ""),
                for_netprps=it.get("for_netprps", ""),
            )
            for it in raw.get("etftisl_trnsn", [])
        ]
        return EtfTimeTrend2(items=items)

    # -----------------------------------------------------------------------
    # ka10048 — ELW일별민감도지표요청
    # -----------------------------------------------------------------------

    def get_elw_daily_sens(self, stock_code: str) -> ElwDailySens:
        """ELW 일별 민감도 지표를 조회한다 (ka10048).

        Args:
            stock_code: ELW 종목코드 (예: ``"57JBHH"``).

        Returns:
            :class:`~kiwoompy.models.ElwDailySens` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10048"),
        ))
        items = [
            ElwDailySensItem(
                dt=it.get("dt", ""),
                iv=it.get("iv", ""),
                delta=it.get("delta", ""),
                gam=it.get("gam", ""),
                theta=it.get("theta", ""),
                vega=it.get("vega", ""),
                law=it.get("law", ""),
                lp=it.get("lp", ""),
            )
            for it in raw.get("elwdaly_snst_ix", [])
        ]
        return ElwDailySens(items=items)

    # -----------------------------------------------------------------------
    # ka10050 — ELW민감도지표요청
    # -----------------------------------------------------------------------

    def get_elw_sens(self, stock_code: str) -> ElwSens:
        """ELW 민감도 지표를 조회한다 (ka10050).

        Args:
            stock_code: ELW 종목코드 (예: ``"57JBHH"``).

        Returns:
            :class:`~kiwoompy.models.ElwSens` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka10050"),
        ))
        items = [
            ElwSensItem(
                cntr_tm=it.get("cntr_tm", ""),
                cur_prc=it.get("cur_prc", ""),
                elwtheory_pric=it.get("elwtheory_pric", ""),
                iv=it.get("iv", ""),
                delta=it.get("delta", ""),
                gam=it.get("gam", ""),
                theta=it.get("theta", ""),
                vega=it.get("vega", ""),
                law=it.get("law", ""),
                lp=it.get("lp", ""),
            )
            for it in raw.get("elwsnst_ix_array", [])
        ]
        return ElwSens(items=items)

    # -----------------------------------------------------------------------
    # ka30001 — ELW가격급등락요청
    # -----------------------------------------------------------------------

    def get_elw_price_surge(
        self,
        fluc_type: "ElwFlucType",
        time_type: str,
        time: str,
        volume_type: str,
        issuer_code: str,
        base_asset_code: str,
        right_type: "ElwRightType",
        lp_code: str,
        exclude_ended: str,
    ) -> ElwPriceSurge:
        """ELW 가격급등락 종목을 조회한다 (ka30001).

        Args:
            fluc_type: 등락구분 (``"surge"`` / ``"plunge"``).
            time_type: 시간구분 (``"1"``분전 / ``"2"``일전).
            time: 시간 (분 또는 일, 예: ``"5"``).
            volume_type: 거래량구분 (``"0"``전체 / ``"10"``만주이상 등).
            issuer_code: 발행사코드 12자리 (전체: ``"000000000000"``).
            base_asset_code: 기초자산코드 12자리 (전체: ``"000000000000"``).
            right_type: 권리구분 (``"all"`` / ``"call"`` / ``"put"`` 등).
            lp_code: LP코드 12자리 (전체: ``"000000000000"``).
            exclude_ended: 거래종료ELW제외 (``"0"``포함 / ``"1"``제외).

        Returns:
            :class:`~kiwoompy.models.ElwPriceSurge` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {
                "flu_tp":           _ELW_FLUC_CODE[fluc_type],
                "tm_tp":            time_type,
                "tm":               time,
                "trde_qty_tp":      volume_type,
                "isscomp_cd":       issuer_code,
                "bsis_aset_cd":     base_asset_code,
                "rght_tp":          _ELW_RIGHT_CODE[right_type],
                "lpcd":             lp_code,
                "trde_end_elwskip": exclude_ended,
            },
            headers=self._headers("ka30001"),
        ))
        items = [
            ElwPriceSurgeItem(
                stk_cd=it.get("stk_cd", ""),
                rank=it.get("rank", ""),
                stk_nm=it.get("stk_nm", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                trde_end_elwbase_pric=it.get("trde_end_elwbase_pric", ""),
                cur_prc=it.get("cur_prc", ""),
                base_pre=it.get("base_pre", ""),
                trde_qty=it.get("trde_qty", ""),
                jmp_rt=it.get("jmp_rt", ""),
            )
            for it in raw.get("elwpric_jmpflu", [])
        ]
        return ElwPriceSurge(
            base_pric_tm=raw.get("base_pric_tm", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka30002 — 거래원별ELW순매매상위요청
    # -----------------------------------------------------------------------

    def get_elw_broker_net_trade(
        self,
        issuer_code: str,
        volume_type: str,
        trade_type: str,
        duration: str,
        exclude_ended: str,
    ) -> ElwBrokerNetTrade:
        """거래원별 ELW 순매매 상위 종목을 조회한다 (ka30002).

        Args:
            issuer_code: 발행사코드 3자리 (예: ``"003"``한국투자증권).
            volume_type: 거래량구분 (``"0"``전체 / ``"5"``5천주 / ``"10"``만주 등).
            trade_type: 매매구분 (``"1"``순매수 / ``"2"``순매도).
            duration: 기간 (``"1"``전일 / ``"5"``5일 / ``"10"``10일 / ``"40"``40일 / ``"60"``60일).
            exclude_ended: 거래종료ELW제외 (``"0"``포함 / ``"1"``제외).

        Returns:
            :class:`~kiwoompy.models.ElwBrokerNetTrade` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {
                "isscomp_cd":       issuer_code,
                "trde_qty_tp":      volume_type,
                "trde_tp":          trade_type,
                "dt":               duration,
                "trde_end_elwskip": exclude_ended,
            },
            headers=self._headers("ka30002"),
        ))
        items = [
            ElwBrokerNetTradeItem(
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                stkpc_flu=it.get("stkpc_flu", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                netprps=it.get("netprps", ""),
                buy_trde_qty=it.get("buy_trde_qty", ""),
                sel_trde_qty=it.get("sel_trde_qty", ""),
            )
            for it in raw.get("trde_ori_elwnettrde_upper", [])
        ]
        return ElwBrokerNetTrade(items=items)

    # -----------------------------------------------------------------------
    # ka30003 — ELWLP보유일별추이요청
    # -----------------------------------------------------------------------

    def get_elw_lp_daily(self, base_asset_code: str, base_date: str) -> ElwLpDaily:
        """ELW LP 보유 일별 추이를 조회한다 (ka30003).

        Args:
            base_asset_code: 기초자산코드 (예: ``"57KJ99"``).
            base_date: 기준일자 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.ElwLpDaily` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {
                "bsis_aset_cd": base_asset_code,
                "base_dt":      base_date,
            },
            headers=self._headers("ka30003"),
        ))
        items = [
            ElwLpDailyItem(
                dt=it.get("dt", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_tp=it.get("pre_tp", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                trde_prica=it.get("trde_prica", ""),
                chg_qty=it.get("chg_qty", ""),
                lprmnd_qty=it.get("lprmnd_qty", ""),
                wght=it.get("wght", ""),
            )
            for it in raw.get("elwlpposs_daly_trnsn", [])
        ]
        return ElwLpDaily(items=items)

    # -----------------------------------------------------------------------
    # ka30004 — ELW괴리율요청
    # -----------------------------------------------------------------------

    def get_elw_gap(
        self,
        issuer_code: str,
        base_asset_code: str,
        right_type: "ElwRightType",
        lp_code: str,
        exclude_ended: str,
    ) -> ElwGap:
        """ELW 괴리율을 조회한다 (ka30004).

        Args:
            issuer_code: 발행사코드 12자리 (전체: ``"000000000000"``).
            base_asset_code: 기초자산코드 12자리 (전체: ``"000000000000"``).
            right_type: 권리구분 (``"all"`` / ``"call"`` / ``"put"`` 등).
            lp_code: LP코드 12자리 (전체: ``"000000000000"``).
            exclude_ended: 거래종료ELW제외 (``"1"``제외 / ``"0"``포함).

        Returns:
            :class:`~kiwoompy.models.ElwGap` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {
                "isscomp_cd":       issuer_code,
                "bsis_aset_cd":     base_asset_code,
                "rght_tp":          _ELW_RIGHT_CODE[right_type],
                "lpcd":             lp_code,
                "trde_end_elwskip": exclude_ended,
            },
            headers=self._headers("ka30004"),
        ))
        items = [
            ElwGapItem(
                stk_cd=it.get("stk_cd", ""),
                isscomp_nm=it.get("isscomp_nm", ""),
                sqnc=it.get("sqnc", ""),
                base_aset_nm=it.get("base_aset_nm", ""),
                rght_tp=it.get("rght_tp", ""),
                dispty_rt=it.get("dispty_rt", ""),
                basis=it.get("basis", ""),
                srvive_dys=it.get("srvive_dys", ""),
                theory_pric=it.get("theory_pric", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_tp=it.get("pre_tp", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                stk_nm=it.get("stk_nm", ""),
            )
            for it in raw.get("elwdispty_rt", [])
        ]
        return ElwGap(items=items)

    # -----------------------------------------------------------------------
    # ka30005 — ELW조건검색요청
    # -----------------------------------------------------------------------

    def get_elw_search(
        self,
        issuer_code: str,
        base_asset_code: str,
        right_type: "ElwRightType",
        lp_code: str,
        sort_type: "ElwSortType",
    ) -> ElwSearch:
        """ELW 조건검색을 수행한다 (ka30005).

        Args:
            issuer_code: 발행사코드 12자리 (전체: ``"000000000000"``).
            base_asset_code: 기초자산코드 12자리 (전체: ``"000000000000"``).
            right_type: 권리구분 (``"all"`` / ``"call"`` / ``"put"`` 등).
            lp_code: LP코드 12자리 (전체: ``"000000000000"``).
            sort_type: 정렬구분 (``"rise_rate"`` / ``"volume"`` 등).

        Returns:
            :class:`~kiwoompy.models.ElwSearch` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {
                "isscomp_cd":   issuer_code,
                "bsis_aset_cd": base_asset_code,
                "rght_tp":      _ELW_RIGHT_CODE[right_type][0],  # 단자리
                "lpcd":         lp_code,
                "sort_tp":      _ELW_SORT_CODE[sort_type],
            },
            headers=self._headers("ka30005"),
        ))
        items = [
            ElwSearchItem(
                stk_cd=it.get("stk_cd", ""),
                isscomp_nm=it.get("isscomp_nm", ""),
                sqnc=it.get("sqnc", ""),
                base_aset_nm=it.get("base_aset_nm", ""),
                rght_tp=it.get("rght_tp", ""),
                expr_dt=it.get("expr_dt", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_tp=it.get("pre_tp", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                trde_qty_pre=it.get("trde_qty_pre", ""),
                trde_prica=it.get("trde_prica", ""),
                pred_trde_qty=it.get("pred_trde_qty", ""),
                sel_bid=it.get("sel_bid", ""),
                buy_bid=it.get("buy_bid", ""),
                prty=it.get("prty", ""),
                gear_rt=it.get("gear_rt", ""),
                pl_qutr_rt=it.get("pl_qutr_rt", ""),
                cfp=it.get("cfp", ""),
                theory_pric=it.get("theory_pric", ""),
                innr_vltl=it.get("innr_vltl", ""),
                delta=it.get("delta", ""),
                lvrg=it.get("lvrg", ""),
                exec_pric=it.get("exec_pric", ""),
                cnvt_rt=it.get("cnvt_rt", ""),
                lpposs_rt=it.get("lpposs_rt", ""),
                pl_qutr_pt=it.get("pl_qutr_pt", ""),
                fin_trde_dt=it.get("fin_trde_dt", ""),
                flo_dt=it.get("flo_dt", ""),
                lpinitlast_suply_dt=it.get("lpinitlast_suply_dt", ""),
                stk_nm=it.get("stk_nm", ""),
                srvive_dys=it.get("srvive_dys", ""),
                dispty_rt=it.get("dispty_rt", ""),
                lpmmcm_nm=it.get("lpmmcm_nm", ""),
                lpmmcm_nm_1=it.get("lpmmcm_nm_1", ""),
                lpmmcm_nm_2=it.get("lpmmcm_nm_2", ""),
                xraymont_cntr_qty_arng_trde_tp=it.get("xraymont_cntr_qty_arng_trde_tp", ""),
                xraymont_cntr_qty_profa_100tp=it.get("xraymont_cntr_qty_profa_100tp", ""),
            )
            for it in raw.get("elwcnd_qry", [])
        ]
        return ElwSearch(items=items)

    # -----------------------------------------------------------------------
    # ka30009 — ELW등락율순위요청
    # -----------------------------------------------------------------------

    def get_elw_fluc_rank(
        self,
        sort_type: "ElwSortType",
        right_type: "ElwRightType",
        exclude_ended: str,
    ) -> ElwFlucRank:
        """ELW 등락율 순위를 조회한다 (ka30009).

        Args:
            sort_type: 정렬구분 (``"rise_rate"`` / ``"rise_gap"`` / ``"fall_rate"`` / ``"fall_gap"``).
            right_type: 권리구분 (``"all"`` / ``"call"`` / ``"put"`` 등).
            exclude_ended: 거래종료제외 (``"1"``제외 / ``"0"``포함).

        Returns:
            :class:`~kiwoompy.models.ElwFlucRank` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {
                "sort_tp":       _ELW_SORT_CODE[sort_type],
                "rght_tp":       _ELW_RIGHT_CODE[right_type],
                "trde_end_skip": exclude_ended,
            },
            headers=self._headers("ka30009"),
        ))
        items = [
            ElwFlucRankItem(
                rank=it.get("rank", ""),
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                sel_req=it.get("sel_req", ""),
                buy_req=it.get("buy_req", ""),
                trde_qty=it.get("trde_qty", ""),
                trde_prica=it.get("trde_prica", ""),
            )
            for it in raw.get("elwflu_rt_rank", [])
        ]
        return ElwFlucRank(items=items)

    # -----------------------------------------------------------------------
    # ka30010 — ELW잔량순위요청
    # -----------------------------------------------------------------------

    def get_elw_bal_rank(
        self,
        sort_type: str,
        right_type: "ElwRightType",
        exclude_ended: str,
    ) -> ElwBalRank:
        """ELW 잔량 순위를 조회한다 (ka30010).

        Args:
            sort_type: 정렬구분 (``"1"``순매수잔량상위 / ``"2"``순매도잔량상위).
            right_type: 권리구분 (``"all"`` / ``"call"`` / ``"put"`` 등).
            exclude_ended: 거래종료제외 (``"1"``제외 / ``"0"``포함).

        Returns:
            :class:`~kiwoompy.models.ElwBalRank` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {
                "sort_tp":       sort_type,
                "rght_tp":       _ELW_RIGHT_CODE[right_type],
                "trde_end_skip": exclude_ended,
            },
            headers=self._headers("ka30010"),
        ))
        items = [
            ElwBalRankItem(
                stk_cd=it.get("stk_cd", ""),
                rank=it.get("rank", ""),
                stk_nm=it.get("stk_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                sel_req=it.get("sel_req", ""),
                buy_req=it.get("buy_req", ""),
                netprps_req=it.get("netprps_req", ""),
                trde_prica=it.get("trde_prica", ""),
            )
            for it in raw.get("elwreq_rank", [])
        ]
        return ElwBalRank(items=items)

    # -----------------------------------------------------------------------
    # ka30011 — ELW근접율요청
    # -----------------------------------------------------------------------

    def get_elw_access_rate(self, stock_code: str) -> ElwAccessRate:
        """ELW 근접율을 조회한다 (ka30011).

        Args:
            stock_code: ELW 종목코드 (예: ``"57JBHH"``).

        Returns:
            :class:`~kiwoompy.models.ElwAccessRate` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka30011"),
        ))
        items = [
            ElwAccessRateItem(
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                alacc_rt=it.get("alacc_rt", ""),
            )
            for it in raw.get("elwalacc_rt", [])
        ]
        return ElwAccessRate(items=items)

    # -----------------------------------------------------------------------
    # ka30012 — ELW종목상세정보요청
    # -----------------------------------------------------------------------

    def get_elw_detail(self, stock_code: str) -> ElwDetail:
        """ELW 종목 상세 정보를 조회한다 (ka30012).

        Args:
            stock_code: ELW 종목코드 (예: ``"57JBHH"``).

        Returns:
            :class:`~kiwoompy.models.ElwDetail` 인스턴스.
        """
        raw = _check(self._api.post(
            self._ELW_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka30012"),
        ))
        return ElwDetail(
            aset_cd=raw.get("aset_cd", ""),
            cur_prc=raw.get("cur_prc", ""),
            pred_pre_sig=raw.get("pred_pre_sig", ""),
            pred_pre=raw.get("pred_pre", ""),
            flu_rt=raw.get("flu_rt", ""),
            lpmmcm_nm=raw.get("lpmmcm_nm", ""),
            lpmmcm_nm_1=raw.get("lpmmcm_nm_1", ""),
            lpmmcm_nm_2=raw.get("lpmmcm_nm_2", ""),
            elwrght_cntn=raw.get("elwrght_cntn", ""),
            elwexpr_evlt_pric=raw.get("elwexpr_evlt_pric", ""),
            elwtheory_pric=raw.get("elwtheory_pric", ""),
            dispty_rt=raw.get("dispty_rt", ""),
            elwinnr_vltl=raw.get("elwinnr_vltl", ""),
            exp_rght_pric=raw.get("exp_rght_pric", ""),
            elwpl_qutr_rt=raw.get("elwpl_qutr_rt", ""),
            elwexec_pric=raw.get("elwexec_pric", ""),
            elwcnvt_rt=raw.get("elwcnvt_rt", ""),
            elwcmpn_rt=raw.get("elwcmpn_rt", ""),
            elwpric_rising_part_rt=raw.get("elwpric_rising_part_rt", ""),
            elwrght_type=raw.get("elwrght_type", ""),
            elwsrvive_dys=raw.get("elwsrvive_dys", ""),
            stkcnt=raw.get("stkcnt", ""),
            elwlpord_pos=raw.get("elwlpord_pos", ""),
            lpposs_rt=raw.get("lpposs_rt", ""),
            lprmnd_qty=raw.get("lprmnd_qty", ""),
            elwspread=raw.get("elwspread", ""),
            elwprty=raw.get("elwprty", ""),
            elwgear=raw.get("elwgear", ""),
            elwflo_dt=raw.get("elwflo_dt", ""),
            elwfin_trde_dt=raw.get("elwfin_trde_dt", ""),
            expr_dt=raw.get("expr_dt", ""),
            exec_dt=raw.get("exec_dt", ""),
            lpsuply_end_dt=raw.get("lpsuply_end_dt", ""),
            elwpay_dt=raw.get("elwpay_dt", ""),
            elwinvt_ix_comput=raw.get("elwinvt_ix_comput", ""),
            elwpay_agnt=raw.get("elwpay_agnt", ""),
            elwappr_way=raw.get("elwappr_way", ""),
            elwrght_exec_way=raw.get("elwrght_exec_way", ""),
            elwpblicte_orgn=raw.get("elwpblicte_orgn", ""),
            dcsn_pay_amt=raw.get("dcsn_pay_amt", ""),
            kobarr=raw.get("kobarr", ""),
            iv=raw.get("iv", ""),
            clsprd_end_elwocr=raw.get("clsprd_end_elwocr", ""),
            bsis_aset_1=raw.get("bsis_aset_1", ""),
            bsis_aset_comp_rt_1=raw.get("bsis_aset_comp_rt_1", ""),
            bsis_aset_2=raw.get("bsis_aset_2", ""),
            bsis_aset_comp_rt_2=raw.get("bsis_aset_comp_rt_2", ""),
            bsis_aset_3=raw.get("bsis_aset_3", ""),
            bsis_aset_comp_rt_3=raw.get("bsis_aset_comp_rt_3", ""),
            bsis_aset_4=raw.get("bsis_aset_4", ""),
            bsis_aset_comp_rt_4=raw.get("bsis_aset_comp_rt_4", ""),
            bsis_aset_5=raw.get("bsis_aset_5", ""),
            bsis_aset_comp_rt_5=raw.get("bsis_aset_comp_rt_5", ""),
            fr_dt=raw.get("fr_dt", ""),
            to_dt=raw.get("to_dt", ""),
            fr_tm=raw.get("fr_tm", ""),
            evlt_end_tm=raw.get("evlt_end_tm", ""),
            evlt_pric=raw.get("evlt_pric", ""),
            evlt_fnsh_yn=raw.get("evlt_fnsh_yn", ""),
            all_hgst_pric=raw.get("all_hgst_pric", ""),
            all_lwst_pric=raw.get("all_lwst_pric", ""),
            imaf_hgst_pric=raw.get("imaf_hgst_pric", ""),
            imaf_lwst_pric=raw.get("imaf_lwst_pric", ""),
            sndhalf_mrkt_hgst_pric=raw.get("sndhalf_mrkt_hgst_pric", ""),
            sndhalf_mrkt_lwst_pric=raw.get("sndhalf_mrkt_lwst_pric", ""),
        )

    # -----------------------------------------------------------------------
    # ka90001 — 테마그룹별요청
    # -----------------------------------------------------------------------

    def get_theme_group(
        self,
        search_type: "ThemeSearchType",
        days: str,
        profit_type: str,
        exchange: "ExchangeType",
        stock_code: str = "",
        theme_name: str = "",
    ) -> ThemeGroup:
        """테마 그룹별 정보를 조회한다 (ka90001).

        Args:
            search_type: 검색구분 (``"all"`` / ``"theme"`` / ``"stock"``).
            days: 날짜구분 — n일 전 (``"1"`` ~ ``"99"``).
            profit_type: 등락수익구분 (``"1"``상위기간수익률 / ``"2"``하위기간수익률 / ``"3"``상위등락률 / ``"4"``하위등락률).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).
            stock_code: 검색 종목코드 (종목검색 시 사용, 기본값: ``""``).
            theme_name: 검색 테마명 (테마검색 시 사용, 기본값: ``""``).

        Returns:
            :class:`~kiwoompy.models.ThemeGroup` 인스턴스.
        """
        raw = _check(self._api.post(
            self._THME_PATH,
            {
                "qry_tp":       _THEME_SEARCH_CODE[search_type],
                "stk_cd":       stock_code,
                "date_tp":      days,
                "thema_nm":     theme_name,
                "flu_pl_amt_tp": profit_type,
                "stex_tp":      _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka90001"),
        ))
        items = [
            ThemeGroupItem(
                thema_grp_cd=it.get("thema_grp_cd", ""),
                thema_nm=it.get("thema_nm", ""),
                stk_num=it.get("stk_num", ""),
                flu_sig=it.get("flu_sig", ""),
                flu_rt=it.get("flu_rt", ""),
                rising_stk_num=it.get("rising_stk_num", ""),
                fall_stk_num=it.get("fall_stk_num", ""),
                dt_prft_rt=it.get("dt_prft_rt", ""),
                main_stk=it.get("main_stk", ""),
            )
            for it in raw.get("thema_grp", [])
        ]
        return ThemeGroup(items=items)

    # -----------------------------------------------------------------------
    # ka90002 — 테마구성종목요청
    # -----------------------------------------------------------------------

    def get_theme_stocks(
        self,
        theme_group_code: str,
        exchange: "ExchangeType",
        days: str = "",
    ) -> ThemeStocks:
        """테마 구성 종목을 조회한다 (ka90002).

        Args:
            theme_group_code: 테마그룹코드 (예: ``"100"``).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).
            days: 날짜구분 — n일 전 (기본값: ``""``).

        Returns:
            :class:`~kiwoompy.models.ThemeStocks` 인스턴스.
        """
        raw = _check(self._api.post(
            self._THME_PATH,
            {
                "date_tp":      days,
                "thema_grp_cd": theme_group_code,
                "stex_tp":      _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka90002"),
        ))
        items = [
            ThemeStockItem(
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                flu_sig=it.get("flu_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                sel_bid=it.get("sel_bid", ""),
                sel_req=it.get("sel_req", ""),
                buy_bid=it.get("buy_bid", ""),
                buy_req=it.get("buy_req", ""),
                dt_prft_rt_n=it.get("dt_prft_rt_n", ""),
            )
            for it in raw.get("thema_comp_stk", [])
        ]
        return ThemeStocks(
            flu_rt=raw.get("flu_rt", ""),
            dt_prft_rt=raw.get("dt_prft_rt", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka90003 — 프로그램순매수상위50요청
    # -----------------------------------------------------------------------

    def get_program_top50(
        self,
        trade_upper_type: str,
        amt_qty_type: str,
        market_type: str,
        exchange: "ExchangeType",
    ) -> ProgramTop50:
        """프로그램 순매수 상위 50 종목을 조회한다 (ka90003).

        Args:
            trade_upper_type: 매매상위구분 (``"1"``순매도상위 / ``"2"``순매수상위).
            amt_qty_type: 금액수량구분 (``"1"``금액 / ``"2"``수량).
            market_type: 시장구분 (``"P00101"``코스피 / ``"P10102"``코스닥).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).

        Returns:
            :class:`~kiwoompy.models.ProgramTop50` 인스턴스.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "trde_upper_tp": trade_upper_type,
                "amt_qty_tp":    amt_qty_type,
                "mrkt_tp":       market_type,
                "stex_tp":       _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka90003"),
        ))
        items = [
            ProgramTop50Item(
                rank=it.get("rank", ""),
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                flu_sig=it.get("flu_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                prm_sell_amt=it.get("prm_sell_amt", ""),
                prm_buy_amt=it.get("prm_buy_amt", ""),
                prm_netprps_amt=it.get("prm_netprps_amt", ""),
            )
            for it in raw.get("prm_netprps_upper_50", [])
        ]
        return ProgramTop50(items=items)

    # -----------------------------------------------------------------------
    # ka90004 — 종목별프로그램매매현황요청
    # -----------------------------------------------------------------------

    def get_stock_program_status(
        self,
        date: str,
        market_type: str,
        exchange: "ExchangeType",
    ) -> StockProgramStatus:
        """종목별 프로그램 매매 현황을 조회한다 (ka90004).

        Args:
            date: 일자 (``"YYYYMMDD"``).
            market_type: 시장구분 (``"P00101"``코스피 / ``"P10102"``코스닥).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).

        Returns:
            :class:`~kiwoompy.models.StockProgramStatus` 인스턴스.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {
                "dt":      date,
                "mrkt_tp": market_type,
                "stex_tp": _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka90004"),
        ))
        items = [
            StockProgramStatusItem(
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                cur_prc=it.get("cur_prc", ""),
                flu_sig=it.get("flu_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                buy_cntr_qty=it.get("buy_cntr_qty", ""),
                buy_cntr_amt=it.get("buy_cntr_amt", ""),
                sel_cntr_qty=it.get("sel_cntr_qty", ""),
                sel_cntr_amt=it.get("sel_cntr_amt", ""),
                netprps_prica=it.get("netprps_prica", ""),
                all_trde_rt=it.get("all_trde_rt", ""),
            )
            for it in raw.get("stk_prm_trde_prst", [])
        ]
        return StockProgramStatus(
            tot_1=raw.get("tot_1", ""),
            tot_2=raw.get("tot_2", ""),
            tot_3=raw.get("tot_3", ""),
            tot_4=raw.get("tot_4", ""),
            tot_5=raw.get("tot_5", ""),
            tot_6=raw.get("tot_6", ""),
            items=items,
        )

    # -----------------------------------------------------------------------
    # ka90005 — 프로그램매매추이요청 시간대별
    # -----------------------------------------------------------------------

    def get_program_trend_by_time(
        self,
        date: str,
        amt_qty_type: str,
        market_type: str,
        min_tic_type: str,
        exchange: "ExchangeType",
    ) -> ProgramTrend:
        """프로그램 매매 추이(시간대별)를 조회한다 (ka90005).

        Args:
            date: 날짜 (``"YYYYMMDD"``).
            amt_qty_type: 금액수량구분 (``"1"``금액(백만원) / ``"2"``수량(천주)).
            market_type: 시장구분 (``"P00101"``코스피KRX 등).
            min_tic_type: 분틱구분 (``"0"``틱 / ``"1"``분).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).

        Returns:
            :class:`~kiwoompy.models.ProgramTrend` 인스턴스.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "date":       date,
                "amt_qty_tp": amt_qty_type,
                "mrkt_tp":    market_type,
                "min_tic_tp": min_tic_type,
                "stex_tp":    _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka90005"),
        ))
        items = [
            ProgramTrendItem(
                cntr_tm=it.get("cntr_tm", ""),
                dfrt_trde_sel=it.get("dfrt_trde_sel", ""),
                dfrt_trde_buy=it.get("dfrt_trde_buy", ""),
                dfrt_trde_netprps=it.get("dfrt_trde_netprps", ""),
                ndiffpro_trde_sel=it.get("ndiffpro_trde_sel", ""),
                ndiffpro_trde_buy=it.get("ndiffpro_trde_buy", ""),
                ndiffpro_trde_netprps=it.get("ndiffpro_trde_netprps", ""),
                dfrt_trde_sell_qty=it.get("dfrt_trde_sell_qty", ""),
                dfrt_trde_buy_qty=it.get("dfrt_trde_buy_qty", ""),
                dfrt_trde_netprps_qty=it.get("dfrt_trde_netprps_qty", ""),
                ndiffpro_trde_sell_qty=it.get("ndiffpro_trde_sell_qty", ""),
                ndiffpro_trde_buy_qty=it.get("ndiffpro_trde_buy_qty", ""),
                ndiffpro_trde_netprps_qty=it.get("ndiffpro_trde_netprps_qty", ""),
                all_sel=it.get("all_sel", ""),
                all_buy=it.get("all_buy", ""),
                all_netprps=it.get("all_netprps", ""),
                kospi200=it.get("kospi200", ""),
                basis=it.get("basis", ""),
            )
            for it in raw.get("prm_trde_trnsn", [])
        ]
        return ProgramTrend(items=items)

    # -----------------------------------------------------------------------
    # ka90006 — 프로그램매매차익잔고추이요청
    # -----------------------------------------------------------------------

    def get_program_arbitrage_bal(
        self,
        date: str,
        exchange: "ExchangeType",
    ) -> ProgramArbitrageBal:
        """프로그램 매매 차익 잔고 추이를 조회한다 (ka90006).

        Args:
            date: 날짜 (``"YYYYMMDD"``).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).

        Returns:
            :class:`~kiwoompy.models.ProgramArbitrageBal` 인스턴스.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "date":    date,
                "stex_tp": _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka90006"),
        ))
        items = [
            ProgramArbitrageBalItem(
                dt=it.get("dt", ""),
                buy_dfrt_trde_qty=it.get("buy_dfrt_trde_qty", ""),
                buy_dfrt_trde_amt=it.get("buy_dfrt_trde_amt", ""),
                buy_dfrt_trde_irds_amt=it.get("buy_dfrt_trde_irds_amt", ""),
                sel_dfrt_trde_qty=it.get("sel_dfrt_trde_qty", ""),
                sel_dfrt_trde_amt=it.get("sel_dfrt_trde_amt", ""),
                sel_dfrt_trde_irds_amt=it.get("sel_dfrt_trde_irds_amt", ""),
            )
            for it in raw.get("prm_trde_dfrt_remn_trnsn", [])
        ]
        return ProgramArbitrageBal(items=items)

    # -----------------------------------------------------------------------
    # ka90007 — 프로그램매매누적추이요청
    # -----------------------------------------------------------------------

    def get_program_acc_trend(
        self,
        date: str,
        amt_qty_type: str,
        market_type: str,
        exchange: "ExchangeType",
    ) -> ProgramAccTrend:
        """프로그램 매매 누적 추이를 조회한다 (ka90007).

        Args:
            date: 날짜 (``"YYYYMMDD"``).
            amt_qty_type: 금액수량구분 (``"1"``금액 / ``"2"``수량).
            market_type: 시장구분 (``"0"``코스피 / ``"1"``코스닥).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).

        Returns:
            :class:`~kiwoompy.models.ProgramAccTrend` 인스턴스.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "date":       date,
                "amt_qty_tp": amt_qty_type,
                "mrkt_tp":    market_type,
                "stex_tp":    _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka90007"),
        ))
        items = [
            ProgramAccTrendItem(
                dt=it.get("dt", ""),
                kospi200=it.get("kospi200", ""),
                basis=it.get("basis", ""),
                dfrt_trde_tdy=it.get("dfrt_trde_tdy", ""),
                dfrt_trde_acc=it.get("dfrt_trde_acc", ""),
                ndiffpro_trde_tdy=it.get("ndiffpro_trde_tdy", ""),
                ndiffpro_trde_acc=it.get("ndiffpro_trde_acc", ""),
                all_tdy=it.get("all_tdy", ""),
                all_acc=it.get("all_acc", ""),
            )
            for it in raw.get("prm_trde_acc_trnsn", [])
        ]
        return ProgramAccTrend(items=items)

    # -----------------------------------------------------------------------
    # ka90008 — 종목시간별프로그램매매추이요청
    # -----------------------------------------------------------------------

    def get_stock_time_program(
        self,
        amt_qty_type: str,
        stock_code: str,
        date: str,
    ) -> StockTimeProgram:
        """종목 시간별 프로그램 매매 추이를 조회한다 (ka90008).

        Args:
            amt_qty_type: 금액수량구분 (``"1"``금액 / ``"2"``수량).
            stock_code: 종목코드 (예: ``"005930"``).
            date: 날짜 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.StockTimeProgram` 인스턴스.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "amt_qty_tp": amt_qty_type,
                "stk_cd":     stock_code,
                "date":       date,
            },
            headers=self._headers("ka90008"),
        ))
        items = [
            StockTimeProgramItem(
                tm=it.get("tm", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                prm_sell_amt=it.get("prm_sell_amt", ""),
                prm_buy_amt=it.get("prm_buy_amt", ""),
                prm_netprps_amt=it.get("prm_netprps_amt", ""),
                prm_netprps_amt_irds=it.get("prm_netprps_amt_irds", ""),
                prm_sell_qty=it.get("prm_sell_qty", ""),
                prm_buy_qty=it.get("prm_buy_qty", ""),
                prm_netprps_qty=it.get("prm_netprps_qty", ""),
                prm_netprps_qty_irds=it.get("prm_netprps_qty_irds", ""),
                base_pric_tm=it.get("base_pric_tm", ""),
                dbrt_trde_rpy_sum=it.get("dbrt_trde_rpy_sum", ""),
                remn_rcvord_sum=it.get("remn_rcvord_sum", ""),
                stex_tp=it.get("stex_tp", ""),
            )
            for it in raw.get("stk_tm_prm_trde_trnsn", [])
        ]
        return StockTimeProgram(items=items)

    # -----------------------------------------------------------------------
    # ka90010 — 프로그램매매추이요청 일자별
    # -----------------------------------------------------------------------

    def get_program_trend_by_day(
        self,
        date: str,
        amt_qty_type: str,
        market_type: str,
        min_tic_type: str,
        exchange: "ExchangeType",
    ) -> ProgramTrend:
        """프로그램 매매 추이(일자별)를 조회한다 (ka90010).

        Args:
            date: 날짜 (``"YYYYMMDD"``).
            amt_qty_type: 금액수량구분 (``"1"``금액(백만원) / ``"2"``수량(천주)).
            market_type: 시장구분 (``"P00101"``코스피KRX 등).
            min_tic_type: 분틱구분 (``"0"``틱 / ``"1"``분).
            exchange: 거래소구분 (``"krx"`` / ``"nxt"`` / ``"all"``).

        Returns:
            :class:`~kiwoompy.models.ProgramTrend` 인스턴스.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "date":       date,
                "amt_qty_tp": amt_qty_type,
                "mrkt_tp":    market_type,
                "min_tic_tp": min_tic_type,
                "stex_tp":    _EXCHANGE_CODE[exchange],
            },
            headers=self._headers("ka90010"),
        ))
        items = [
            ProgramTrendItem(
                cntr_tm=it.get("cntr_tm", ""),
                dfrt_trde_sel=it.get("dfrt_trde_sel", ""),
                dfrt_trde_buy=it.get("dfrt_trde_buy", ""),
                dfrt_trde_netprps=it.get("dfrt_trde_netprps", ""),
                ndiffpro_trde_sel=it.get("ndiffpro_trde_sel", ""),
                ndiffpro_trde_buy=it.get("ndiffpro_trde_buy", ""),
                ndiffpro_trde_netprps=it.get("ndiffpro_trde_netprps", ""),
                dfrt_trde_sell_qty=it.get("dfrt_trde_sell_qty", ""),
                dfrt_trde_buy_qty=it.get("dfrt_trde_buy_qty", ""),
                dfrt_trde_netprps_qty=it.get("dfrt_trde_netprps_qty", ""),
                ndiffpro_trde_sell_qty=it.get("ndiffpro_trde_sell_qty", ""),
                ndiffpro_trde_buy_qty=it.get("ndiffpro_trde_buy_qty", ""),
                ndiffpro_trde_netprps_qty=it.get("ndiffpro_trde_netprps_qty", ""),
                all_sel=it.get("all_sel", ""),
                all_buy=it.get("all_buy", ""),
                all_netprps=it.get("all_netprps", ""),
                kospi200=it.get("kospi200", ""),
                basis=it.get("basis", ""),
            )
            for it in raw.get("prm_trde_trnsn", [])
        ]
        return ProgramTrend(items=items)

    # -----------------------------------------------------------------------
    # ka90013 — 종목일별프로그램매매추이요청
    # -----------------------------------------------------------------------

    def get_stock_daily_program(
        self,
        stock_code: str,
        amt_qty_type: str = "",
        date: str = "",
    ) -> StockDailyProgram:
        """종목 일별 프로그램 매매 추이를 조회한다 (ka90013).

        Args:
            stock_code: 종목코드 (예: ``"005930"``).
            amt_qty_type: 금액수량구분 (``"1"``금액 / ``"2"``수량, 기본값: ``""``).
            date: 날짜 (``"YYYYMMDD"``, 기본값: ``""``).

        Returns:
            :class:`~kiwoompy.models.StockDailyProgram` 인스턴스.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {
                "amt_qty_tp": amt_qty_type,
                "stk_cd":     stock_code,
                "date":       date,
            },
            headers=self._headers("ka90013"),
        ))
        items = [
            StockDailyProgramItem(
                dt=it.get("dt", ""),
                cur_prc=it.get("cur_prc", ""),
                pre_sig=it.get("pre_sig", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                prm_sell_amt=it.get("prm_sell_amt", ""),
                prm_buy_amt=it.get("prm_buy_amt", ""),
                prm_netprps_amt=it.get("prm_netprps_amt", ""),
                prm_netprps_amt_irds=it.get("prm_netprps_amt_irds", ""),
                prm_sell_qty=it.get("prm_sell_qty", ""),
                prm_buy_qty=it.get("prm_buy_qty", ""),
                prm_netprps_qty=it.get("prm_netprps_qty", ""),
                prm_netprps_qty_irds=it.get("prm_netprps_qty_irds", ""),
                base_pric_tm=it.get("base_pric_tm", ""),
                dbrt_trde_rpy_sum=it.get("dbrt_trde_rpy_sum", ""),
                remn_rcvord_sum=it.get("remn_rcvord_sum", ""),
                stex_tp=it.get("stex_tp", ""),
            )
            for it in raw.get("stk_daly_prm_trde_trnsn", [])
        ]
        return StockDailyProgram(items=items)

    # ──────────────────────────────────────────────────────────
    # 9단계 — 금현물 (ka50xxx, ka52xxx)
    # ──────────────────────────────────────────────────────────

    def gold_contract_trend(self, stock_code: GoldStockCode) -> GoldContractTrend:
        """금현물체결추이를 조회한다 (ka50010).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).

        Returns:
            :class:`~kiwoompy.models.GoldContractTrend` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka50010"),
        ))
        items = [
            GoldContractTrendItem(
                cntr_pric=it.get("cntr_pric", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                acc_trde_prica=it.get("acc_trde_prica", ""),
                cntr_trde_qty=it.get("cntr_trde_qty", ""),
                tm=it.get("tm", ""),
                pre_sig=it.get("pre_sig", ""),
                pri_sel_bid_unit=it.get("pri_sel_bid_unit", ""),
                pri_buy_bid_unit=it.get("pri_buy_bid_unit", ""),
                trde_pre=it.get("trde_pre", ""),
                trde_tern_rt=it.get("trde_tern_rt", ""),
                cntr_str=it.get("cntr_str", ""),
            )
            for it in raw.get("gold_cntr", [])
        ]
        return GoldContractTrend(items=items)

    def gold_daily_trend(
        self,
        stock_code: GoldStockCode,
        base_date: str,
    ) -> GoldDailyTrend:
        """금현물일별추이를 조회한다 (ka50012).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            base_date: 기준일자 (``"YYYYMMDD"``).

        Returns:
            :class:`~kiwoompy.models.GoldDailyTrend` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code, "base_dt": base_date},
            headers=self._headers("ka50012"),
        ))
        items = [
            GoldDailyTrendItem(
                cur_prc=it.get("cur_prc", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                acc_trde_prica=it.get("acc_trde_prica", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
                dt=it.get("dt", ""),
                pre_sig=it.get("pre_sig", ""),
                orgn_netprps=it.get("orgn_netprps", ""),
                for_netprps=it.get("for_netprps", ""),
                ind_netprps=it.get("ind_netprps", ""),
            )
            for it in raw.get("gold_daly_trnsn", [])
        ]
        return GoldDailyTrend(items=items)

    def gold_expected_contract(self, stock_code: GoldStockCode) -> GoldExpectedContract:
        """금현물예상체결을 조회한다 (ka50087).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).

        Returns:
            :class:`~kiwoompy.models.GoldExpectedContract` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka50087"),
        ))
        items = [
            GoldExpectedContractItem(
                exp_cntr_pric=it.get("exp_cntr_pric", ""),
                exp_pred_pre=it.get("exp_pred_pre", ""),
                exp_flu_rt=it.get("exp_flu_rt", ""),
                exp_acc_trde_qty=it.get("exp_acc_trde_qty", ""),
                exp_cntr_trde_qty=it.get("exp_cntr_trde_qty", ""),
                exp_tm=it.get("exp_tm", ""),
                exp_pre_sig=it.get("exp_pre_sig", ""),
                stex_tp=it.get("stex_tp", ""),
            )
            for it in raw.get("gold_expt_exec", [])
        ]
        return GoldExpectedContract(items=items)

    def gold_market_info(self, stock_code: GoldStockCode) -> GoldMarketInfo:
        """금현물 시세정보를 조회한다 (ka50100).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).

        Returns:
            :class:`~kiwoompy.models.GoldMarketInfo` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code},
            headers=self._headers("ka50100"),
        ))
        return GoldMarketInfo(
            pred_pre_sig=raw.get("pred_pre_sig", ""),
            pred_pre=raw.get("pred_pre", ""),
            flu_rt=raw.get("flu_rt", ""),
            trde_qty=raw.get("trde_qty", ""),
            open_pric=raw.get("open_pric", ""),
            high_pric=raw.get("high_pric", ""),
            low_pric=raw.get("low_pric", ""),
            pred_rt=raw.get("pred_rt", ""),
            upl_pric=raw.get("upl_pric", ""),
            lst_pric=raw.get("lst_pric", ""),
            pred_close_pric=raw.get("pred_close_pric", ""),
        )

    def gold_bid(
        self,
        stock_code: GoldStockCode,
        tick_scope: str,
    ) -> GoldBid:
        """금현물 호가를 조회한다 (ka50101).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            tick_scope: 틱범위. ``"1"``:1틱, ``"3"``:3틱, ``"5"``:5틱, ``"10"``:10틱, ``"30"``:30틱.

        Returns:
            :class:`~kiwoompy.models.GoldBid` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._MRKCOND_PATH,
            {"stk_cd": stock_code, "tic_scope": tick_scope},
            headers=self._headers("ka50101"),
        ))
        items = [
            GoldBidItem(
                cntr_pric=it.get("cntr_pric", ""),
                pred_pre=it.get("pred_pre", ""),
                flu_rt=it.get("flu_rt", ""),
                trde_qty=it.get("trde_qty", ""),
                acc_trde_prica=it.get("acc_trde_prica", ""),
                cntr_trde_qty=it.get("cntr_trde_qty", ""),
                tm=it.get("tm", ""),
                pre_sig=it.get("pre_sig", ""),
                pri_sel_bid_unit=it.get("pri_sel_bid_unit", ""),
                pri_buy_bid_unit=it.get("pri_buy_bid_unit", ""),
                trde_pre=it.get("trde_pre", ""),
                trde_tern_rt=it.get("trde_tern_rt", ""),
                cntr_str=it.get("cntr_str", ""),
                lpmmcm_nm_1=it.get("lpmmcm_nm_1", ""),
                stex_tp=it.get("stex_tp", ""),
            )
            for it in raw.get("gold_bid", [])
        ]
        return GoldBid(items=items)

    def gold_investor_status(self) -> GoldInvestorStatus:
        """금현물투자자현황을 조회한다 (ka52301).

        Returns:
            :class:`~kiwoompy.models.GoldInvestorStatus` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._FRGNISTT_PATH,
            {},
            headers=self._headers("ka52301"),
        ))
        items = [
            GoldInvestorStatusItem(
                stk_nm=it.get("stk_nm", ""),
                stk_cd=it.get("stk_cd", ""),
                all_dfrt_trst_sell_qty=it.get("all_dfrt_trst_sell_qty", ""),
                sell_qty_irds=it.get("sell_qty_irds", ""),
                all_dfrt_trst_sell_amt=it.get("all_dfrt_trst_sell_amt", ""),
                sell_amt_irds=it.get("sell_amt_irds", ""),
                all_dfrt_trst_buy_qty=it.get("all_dfrt_trst_buy_qty", ""),
                buy_qty_irds=it.get("buy_qty_irds", ""),
                all_dfrt_trst_buy_amt=it.get("all_dfrt_trst_buy_amt", ""),
                buy_amt_irds=it.get("buy_amt_irds", ""),
                all_dfrt_trst_netprps_qty=it.get("all_dfrt_trst_netprps_qty", ""),
                netprps_qty_irds=it.get("netprps_qty_irds", ""),
                all_dfrt_trst_netprps_amt=it.get("all_dfrt_trst_netprps_amt", ""),
                netprps_amt_irds=it.get("netprps_amt_irds", ""),
                sell_uv=it.get("sell_uv", ""),
                buy_uv=it.get("buy_uv", ""),
                acc_netprps_amt=it.get("acc_netprps_amt", ""),
                acc_netprps_qty=it.get("acc_netprps_qty", ""),
            )
            for it in raw.get("inve_trad_stat", [])
        ]
        return GoldInvestorStatus(items=items)

    def gold_tick_chart(
        self,
        stock_code: GoldStockCode,
        tick_scope: str,
        adjust_price: str = "1",
    ) -> GoldTickChart:
        """금현물틱차트를 조회한다 (ka50079).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            tick_scope: 틱범위. ``"1"``:1틱, ``"3"``:3틱, ``"5"``:5틱, ``"10"``:10틱, ``"30"``:30틱.
            adjust_price: 수정주가구분. ``"0"`` 또는 ``"1"``. 기본값 ``"1"``.

        Returns:
            :class:`~kiwoompy.models.GoldTickChart` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {"stk_cd": stock_code, "tic_scope": tick_scope, "upd_stkpc_tp": adjust_price},
            headers=self._headers("ka50079"),
        ))
        items = [
            GoldTickChartItem(
                cur_prc=it.get("cur_prc", ""),
                pred_pre=it.get("pred_pre", ""),
                trde_qty=it.get("trde_qty", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
                cntr_tm=it.get("cntr_tm", ""),
                dt=it.get("dt", ""),
                pred_pre_sig=it.get("pred_pre_sig", ""),
            )
            for it in raw.get("gds_tic_chart_qry", [])
        ]
        return GoldTickChart(items=items)

    def gold_minute_chart(
        self,
        stock_code: GoldStockCode,
        tick_scope: str,
        adjust_price: str = "1",
    ) -> GoldMinuteChart:
        """금현물분봉차트를 조회한다 (ka50080).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            tick_scope: 틱범위(분). ``"1"``:1분, ``"3"``:3분, ``"5"``:5분, ``"10"``:10분,
                ``"15"``:15분, ``"30"``:30분, ``"45"``:45분, ``"60"``:60분.
            adjust_price: 수정주가구분. ``"0"`` 또는 ``"1"``. 기본값 ``"1"``.

        Returns:
            :class:`~kiwoompy.models.GoldMinuteChart` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {"stk_cd": stock_code, "tic_scope": tick_scope, "upd_stkpc_tp": adjust_price},
            headers=self._headers("ka50080"),
        ))
        items = [
            GoldMinuteChartItem(
                cur_prc=it.get("cur_prc", ""),
                pred_pre=it.get("pred_pre", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                trde_qty=it.get("trde_qty", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
                cntr_tm=it.get("cntr_tm", ""),
                dt=it.get("dt", ""),
                pred_pre_sig=it.get("pred_pre_sig", ""),
            )
            for it in raw.get("gds_min_chart_qry", [])
        ]
        return GoldMinuteChart(items=items)

    def gold_daily_chart(
        self,
        stock_code: GoldStockCode,
        base_date: str,
        adjust_price: str = "1",
    ) -> GoldDailyChart:
        """금현물일봉차트를 조회한다 (ka50081).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            base_date: 기준일자 (``"YYYYMMDD"``).
            adjust_price: 수정주가구분. ``"0"`` 또는 ``"1"``. 기본값 ``"1"``.

        Returns:
            :class:`~kiwoompy.models.GoldDailyChart` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {"stk_cd": stock_code, "base_dt": base_date, "upd_stkpc_tp": adjust_price},
            headers=self._headers("ka50081"),
        ))
        items = [
            GoldDailyChartItem(
                cur_prc=it.get("cur_prc", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                acc_trde_prica=it.get("acc_trde_prica", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
                dt=it.get("dt", ""),
                pred_pre_sig=it.get("pred_pre_sig", ""),
            )
            for it in raw.get("gds_day_chart_qry", [])
        ]
        return GoldDailyChart(items=items)

    def gold_weekly_chart(
        self,
        stock_code: GoldStockCode,
        base_date: str,
        adjust_price: str = "1",
    ) -> GoldWeeklyChart:
        """금현물주봉차트를 조회한다 (ka50082).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            base_date: 기준일자 (``"YYYYMMDD"``).
            adjust_price: 수정주가구분. ``"0"`` 또는 ``"1"``. 기본값 ``"1"``.

        Returns:
            :class:`~kiwoompy.models.GoldWeeklyChart` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {"stk_cd": stock_code, "base_dt": base_date, "upd_stkpc_tp": adjust_price},
            headers=self._headers("ka50082"),
        ))
        items = [
            GoldWeeklyChartItem(
                cur_prc=it.get("cur_prc", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                acc_trde_prica=it.get("acc_trde_prica", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
                dt=it.get("dt", ""),
            )
            for it in raw.get("gds_week_chart_qry", [])
        ]
        return GoldWeeklyChart(items=items)

    def gold_monthly_chart(
        self,
        stock_code: GoldStockCode,
        base_date: str,
        adjust_price: str = "1",
    ) -> GoldMonthlyChart:
        """금현물월봉차트를 조회한다 (ka50083).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            base_date: 기준일자 (``"YYYYMMDD"``).
            adjust_price: 수정주가구분. ``"0"`` 또는 ``"1"``. 기본값 ``"1"``.

        Returns:
            :class:`~kiwoompy.models.GoldMonthlyChart` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {"stk_cd": stock_code, "base_dt": base_date, "upd_stkpc_tp": adjust_price},
            headers=self._headers("ka50083"),
        ))
        items = [
            GoldMonthlyChartItem(
                cur_prc=it.get("cur_prc", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                acc_trde_prica=it.get("acc_trde_prica", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
                dt=it.get("dt", ""),
            )
            for it in raw.get("gds_month_chart_qry", [])
        ]
        return GoldMonthlyChart(items=items)

    def gold_daily_tick_chart(
        self,
        stock_code: GoldStockCode,
        tick_scope: str,
    ) -> GoldDailyTickChart:
        """금현물당일틱차트를 조회한다 (ka50091).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            tick_scope: 틱범위. ``"1"``:1틱, ``"3"``:3틱, ``"5"``:5틱, ``"10"``:10틱, ``"30"``:30틱.

        Returns:
            :class:`~kiwoompy.models.GoldDailyTickChart` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {"stk_cd": stock_code, "tic_scope": tick_scope},
            headers=self._headers("ka50091"),
        ))
        items = [
            GoldDailyTickChartItem(
                cntr_pric=it.get("cntr_pric", ""),
                pred_pre=it.get("pred_pre", ""),
                trde_qty=it.get("trde_qty", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
                cntr_tm=it.get("cntr_tm", ""),
                dt=it.get("dt", ""),
                pred_pre_sig=it.get("pred_pre_sig", ""),
            )
            for it in raw.get("gds_tic_chart_qry", [])
        ]
        return GoldDailyTickChart(items=items)

    def gold_daily_minute_chart(
        self,
        stock_code: GoldStockCode,
        tick_scope: str,
    ) -> GoldDailyMinuteChart:
        """금현물당일분봉차트를 조회한다 (ka50092).

        Args:
            stock_code: 금현물 종목코드.
                ``"M04020000"`` (금 99.99_1kg) 또는 ``"M04020100"`` (미니금 99.99_100g).
            tick_scope: 틱범위(분). ``"1"``:1분, ``"3"``:3분, ``"5"``:5분, ``"10"``:10분, ``"30"``:30분.

        Returns:
            :class:`~kiwoompy.models.GoldDailyMinuteChart` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._CHART_PATH,
            {"stk_cd": stock_code, "tic_scope": tick_scope},
            headers=self._headers("ka50092"),
        ))
        items = [
            GoldDailyMinuteChartItem(
                cntr_pric=it.get("cntr_pric", ""),
                pred_pre=it.get("pred_pre", ""),
                acc_trde_qty=it.get("acc_trde_qty", ""),
                acc_trde_prica=it.get("acc_trde_prica", ""),
                trde_qty=it.get("trde_qty", ""),
                open_pric=it.get("open_pric", ""),
                high_pric=it.get("high_pric", ""),
                low_pric=it.get("low_pric", ""),
                cntr_tm=it.get("cntr_tm", ""),
                dt=it.get("dt", ""),
                pred_pre_sig=it.get("pred_pre_sig", ""),
            )
            for it in raw.get("gds_min_chart_qry", [])
        ]
        return GoldDailyMinuteChart(items=items)

    # ──────────────────────────────────────────────────────────
    # 11단계 — 신용주문 관련 종목정보 (kt20xxx)
    # ──────────────────────────────────────────────────────────

    _STKINFO_PATH = "/api/dostk/stkinfo"

    def credit_loan_stocks(
        self,
        mrkt_deal_tp: CreditMarketType,
        *,
        crd_stk_grde_tp: CreditStockGradeType = "%",
        stk_cd: str = "",
    ) -> CreditLoanStocks:
        """신용융자 가능종목을 조회한다 (kt20016).

        Args:
            mrkt_deal_tp: 시장거래구분.
                ``"%"`` (전체), ``"1"`` (코스피), ``"0"`` (코스닥).
            crd_stk_grde_tp: 신용종목등급구분 (기본값 ``"%"`` — 전체).
                ``"A"`` ~ ``"E"`` 로 등급 필터 가능.
            stk_cd: 종목코드. 빈 문자열이면 전체 조회.

        Returns:
            :class:`~kiwoompy.models.CreditLoanStocks` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        body: dict = {"mrkt_deal_tp": mrkt_deal_tp, "crd_stk_grde_tp": crd_stk_grde_tp}
        if stk_cd:
            body["stk_cd"] = stk_cd
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            body,
            headers=self._headers("kt20016"),
        ))
        items = [
            CreditLoanStockItem(
                stk_cd=it.get("stk_cd", ""),
                stk_nm=it.get("stk_nm", ""),
                crd_assr_rt=it.get("crd_assr_rt", ""),
                repl_pric=it.get("repl_pric", ""),
                pred_close_pric=it.get("pred_close_pric", ""),
                crd_limit_over_yn=it.get("crd_limit_over_yn", ""),
                crd_limit_over_txt=it.get("crd_limit_over_txt", ""),
            )
            for it in raw.get("crd_loan_pos_stk", [])
        ]
        return CreditLoanStocks(
            crd_loan_able=raw.get("crd_loan_able", ""),
            items=items,
        )

    def credit_loan_availability(self, stk_cd: str) -> CreditLoanAvailability:
        """종목의 신용융자 가능 여부를 조회한다 (kt20017).

        Args:
            stk_cd: 종목코드 (예: ``"039490"``).

        Returns:
            :class:`~kiwoompy.models.CreditLoanAvailability` 인스턴스.

        Raises:
            KiwoomAuthError: 토큰 미발급 또는 인증 실패.
            KiwoomApiError: 서버 오류.
        """
        raw = _check(self._api.post(
            self._STKINFO_PATH,
            {"stk_cd": stk_cd},
            headers=self._headers("kt20017"),
        ))
        return CreditLoanAvailability(crd_alow_yn=raw.get("crd_alow_yn", ""))
