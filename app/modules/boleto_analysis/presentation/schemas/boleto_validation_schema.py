from datetime import date
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


# ==========================================================
# REQUEST
# ==========================================================

class ValidateBoletoRequest(BaseModel):
    """
    Payload de entrada para análise antifraude de boleto.
    """

    code: str = Field(
        ...,
        min_length=44,
        max_length=48,
        examples=[
            "34191.09008 63521.480908 24115.690001 6 94550000123456",
            "34191090086352148090824115690001694550000123456",
        ],
        description=(
            "Código de barras (44 dígitos) ou linha digitável "
            "(47/48 dígitos)."
        ),
    )

    @field_validator("code", mode="before")
    @classmethod
    def normalize_code(cls, v: str) -> str:
        import re

        return re.sub(r"[\s.\-]", "", v.strip())


# ==========================================================
# RESPONSE
# ==========================================================

class BoletoValidationResponse(BaseModel):
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

    status: str = Field(
        description="valid | suspicious | fraud_suspect"
    )

    # explicabilidade
    reasons: List[str]

    model_config = {
        "from_attributes": True
    }


# ==========================================================
# ERROR
# ==========================================================

class ErrorResponse(BaseModel):
    """
    Formato padrão de erro retornado pela API.
    """

    error: str
    detail: str
    status_code: int
