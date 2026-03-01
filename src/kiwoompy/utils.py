"""kiwoompy 공통 유틸리티 — 입력값 정규화, 로깅 등."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

_ACCOUNT_NO_FULL = re.compile(r"^\d{8}-\d{2}$")
_ACCOUNT_NO_SHORT = re.compile(r"^\d{8}$")

DEFAULT_PRODUCT_CODE = "01"
"""계좌번호 상품코드 기본값. 미입력 시 자동으로 붙여준다."""


def normalize_account_no(account_no: str, product_code: str = DEFAULT_PRODUCT_CODE) -> str:
    """계좌번호를 ``"12345678-01"`` 형식으로 정규화한다.

    계좌번호 상품코드(``-01`` 부분)가 없는 경우 ``product_code``를 붙여주고
    경고 로그를 남긴다. 사용자의 실수를 라이브러리가 보완하기 위한 처리다.

    Args:
        account_no: 사용자가 입력한 계좌번호.
            ``"12345678-01"`` (완전한 형식) 또는 ``"12345678"`` (상품코드 생략) 허용.
        product_code: 상품코드가 없을 때 사용할 기본값. 기본값은 ``"01"``.

    Returns:
        ``"12345678-01"`` 형식의 계좌번호.

    Raises:
        ValueError: 계좌번호 형식이 ``"12345678"`` / ``"12345678-01"`` 둘 다 아닌 경우.

    Examples:
        >>> normalize_account_no("12345678")
        '12345678-01'
        >>> normalize_account_no("12345678-01")
        '12345678-01'
        >>> normalize_account_no("12345678", product_code="02")
        '12345678-02'
    """
    if _ACCOUNT_NO_FULL.match(account_no):
        return account_no

    if _ACCOUNT_NO_SHORT.match(account_no):
        normalized = f"{account_no}-{product_code}"
        logger.warning(
            "계좌번호 상품코드가 없습니다. 기본값 '%s'를 사용합니다: %s → %s",
            product_code,
            account_no,
            normalized,
        )
        return normalized

    raise ValueError(
        f"올바르지 않은 계좌번호 형식입니다: {account_no!r}\n"
        f"  올바른 형식: '12345678' 또는 '12345678-01'"
    )
