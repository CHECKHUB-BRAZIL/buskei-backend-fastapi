from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Requests
# ---------------------------------------------------------------------------

class ValidateBoletoRequest(BaseModel):
    """Payload de entrada para validação de um boleto."""

    code: str = Field(
        ...,
        min_length=44,
        max_length=48,
        examples=[
            "34191.09008 63521.480908 24115.690001 6 94550000123456",
            "34191090086352148090824115690001694550000123456",
        ],
        description=(
            "Código de barras (44 dígitos) ou linha digitável (47/48 dígitos). "
            "Espaços, pontos e hífens são aceitos e removidos automaticamente."
        ),
    )

    @field_validator("code")
    @classmethod
    def normalize_code(cls, v: str) -> str:
        """Remove espaços, pontos e hífens antes de repassar ao use case."""
        import re
        return re.sub(r"[\s.\-]", "", v.strip())


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------

class BoletoValidationResponse(BaseModel):
    """Resposta completa de uma validação de boleto."""

    code: str = Field(description="Código de barras normalizado (44 dígitos).")
    original_code: str = Field(description="Entrada original enviada pelo usuário.")
    boleto_type: str = Field(description="Tipo do boleto: 'cobranca' | 'convenio'.")
    amount: Decimal = Field(description="Valor em Decimal com 2 casas decimais.")
    amount_formatted: str = Field(description="Valor formatado. Ex: 'R$ 125,00'.")
    due_date: Optional[date] = Field(description="Data de vencimento. None se sem vencimento.")
    due_date_formatted: str = Field(description="Ex: '15/06/2025' ou 'Sem vencimento'.")
    is_expired: bool = Field(description="True se o boleto está vencido.")
    days_overdue: int = Field(description="Dias de atraso. 0 se não vencido.")
    days_until_due: Optional[int] = Field(
        description="Dias até o vencimento. None se sem data ou já vencido."
    )
    status: str = Field(description="Status: 'valid' | 'expired' | 'suspicious'.")
    reasons: List[str] = Field(description="Motivos que justificam o status.")
    created_at: datetime

    model_config = {"from_attributes": True}


class BoletoValidationSummaryResponse(BaseModel):
    """Versão resumida para listagens."""

    code: str
    boleto_type: str
    amount_formatted: str
    due_date_formatted: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class BoletoValidationListResponse(BaseModel):
    """Envelope de listagem com total e itens resumidos."""

    total: int
    items: List[BoletoValidationSummaryResponse]


class DeleteBoletoValidationResponse(BaseModel):
    """Confirmação de exclusão de uma validação."""

    message: str
    code: str


class ErrorResponse(BaseModel):
    """Formato padrão de erro retornado pela API."""

    error: str
    detail: str
    status_code: int
