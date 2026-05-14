from typing import List

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Requests
# ---------------------------------------------------------------------------

class AnalyzeLinkRequest(BaseModel):
    url: str = Field(
        ...,
        min_length=1,
        max_length=2083,
        examples=["https://www.google.com"],
        description="URL completa a ser analisada.",
    )

    @field_validator("url")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------

class AnalyzeLinkResponse(BaseModel):
    url: str

    risk: str = Field(
        description="Nivel de risco: LOW | MEDIUM | HIGH"
    )

    risk_score: int = Field(
        description="Pontuação numérica de risco."
    )

    reasons: List[str] = Field(
        description="Motivos de risco encontrados."
    )

    positives: List[str] = Field(
        description="Indicadores positivos encontrados."
    )

    model_config = {
        "from_attributes": True
    }


class ErrorResponse(BaseModel):
    error: str
    detail: str
    status_code: int
