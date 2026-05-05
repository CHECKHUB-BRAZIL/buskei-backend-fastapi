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
    code: str  # código de barras (44) ou linha digitável (47/48) — string bruta


@dataclass(frozen=True)
class GetBoletoValidationInputDTO:
    """Dados de entrada para buscar uma validação já existente por código."""
    code: str


@dataclass(frozen=True)
class DeleteBoletoValidationInputDTO:
    """Dados de entrada para remover uma validação por código."""
    code: str


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ValidateBoletoOutputDTO:
    """
    Dados de saída após a validação de um boleto.
    Todos os tipos são primitivos Python — sem Value Objects de domínio.
    """
    code: str                       # código de barras normalizado (44 dígitos)
    original_code: str              # entrada original do usuário
    boleto_type: str                # 'cobranca' | 'convenio'
    amount: Decimal                 # valor em Decimal com 2 casas
    amount_formatted: str           # ex: "R$ 125,00"
    due_date: Optional[date]        # None = sem vencimento
    due_date_formatted: str         # ex: "15/06/2025" ou "Sem vencimento"
    is_expired: bool
    days_overdue: int               # 0 se não vencido
    days_until_due: Optional[int]   # None se sem data ou já vencido
    status: str                     # 'valid' | 'expired' | 'suspicious'
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
class ListBoletoValidationsOutputDTO:
    """Envelope de listagem com total e itens resumidos."""
    total: int
    items: List[BoletoValidationSummaryDTO]
