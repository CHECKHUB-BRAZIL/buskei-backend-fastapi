from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List, Optional


# ==========================================================
# REQUEST
# ==========================================================

@dataclass(frozen=True)
class ValidateBoletoInputDTO:
    """
    Entrada da análise antifraude de boleto.
    """

    code: str


# ==========================================================
# RESPONSE
# ==========================================================

@dataclass(frozen=True)
class ValidateBoletoOutputDTO:
    """
    Resultado da análise antifraude do boleto.
    """

    # identificação
    code: str
    original_code: str
    boleto_type: str

    # integridade
    is_real: bool

    # financeiro
    amount: Decimal
    amount_formatted: str

    # vencimento
    due_date: Optional[date]
    due_date_formatted: str
    is_expired: bool
    days_overdue: int
    days_until_due: Optional[int]

    # antifraude
    risk_score: int
    status: str

    # explicabilidade
    reasons: List[str]
