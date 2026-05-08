from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional


# ---------------------------------------------------------------------------
# Requests
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ValidateBoletoInputDTO:
    """
    Dados de entrada para o caso de uso de validação de boleto.
    Recebe o código bruto da apresentação — a aplicação valida e converte.
    """
    code: str
    user_id: str


@dataclass(frozen=True)
class GetBoletoValidationInputDTO:
    """Dados de entrada para buscar uma validação já existente por código."""
    code: str
    user_id: str


@dataclass(frozen=True)
class DeleteBoletoValidationInputDTO:
    """Dados de entrada para remover uma validação por código."""
    code: str
    user_id: str


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ValidateBoletoOutputDTO:
    """
    Dados de saída após a validação de um boleto.
    Todos os tipos são primitivos Python — sem Value Objects de domínio.
    """

    code: str
    original_code: str
    boleto_type: str
    amount: Decimal
    amount_formatted: str
    due_date: Optional[date]
    due_date_formatted: str
    is_expired: bool
    days_overdue: int
    days_until_due: Optional[int]
    status: str
    reasons: List[str]
    created_at: datetime


@dataclass(frozen=True)
class BoletoValidationSummaryDTO:
    """
    Versão resumida para listagens — menos campos para economizar payload.
    """

    code: str
    boleto_type: str
    amount_formatted: str
    due_date_formatted: str
    status: str
    created_at: datetime

@dataclass(frozen=True)
class ListBoletoValidationsInputDTO:
    user_id: str

@dataclass(frozen=True)
class ListBoletoValidationsOutputDTO:
    """Envelope de listagem com total e itens resumidos."""

    total: int
    items: List[BoletoValidationSummaryDTO]
