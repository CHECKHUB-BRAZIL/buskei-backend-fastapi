from typing import List

from pydantic import BaseModel, Field, field_validator


# ==========================================================
# REQUEST
# ==========================================================

class AnalyzeLinkRequest(BaseModel):
    """
    Payload de entrada para análise de link.
    """

    url: str = Field(
        ...,
        min_length=1,
        max_length=2083,
        examples=[
            "https://google.com",
            "https://secure-login-bank.xyz/login",
        ],
        description=(
            "URL completa a ser analisada. "
            "Deve incluir http:// ou https://."
        ),
    )

    @field_validator("url")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()


# ==========================================================
# RESPONSE
# ==========================================================

class AnalyzeLinkResponse(BaseModel):
    """
    Resultado da análise antifraude do link.
    """

    url: str

    risk: str = Field(
        description="LOW | MEDIUM | HIGH"
    )

    risk_score: int = Field(
        description="Pontuação numérica de risco."
    )

    reasons: List[str] = Field(
        description="Motivos de risco identificados."
    )

    positives: List[str] = Field(
        description="Indicadores positivos encontrados."
    )

    model_config = {
        "from_attributes": True
    }


# ==========================================================
# ERROR RESPONSE
# ==========================================================

class ErrorResponse(BaseModel):
    """
    Formato padrão de erro da API.
    """

    error: str
    detail: str
    status_code: int
