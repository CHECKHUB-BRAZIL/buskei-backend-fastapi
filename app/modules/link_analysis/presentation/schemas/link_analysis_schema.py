from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Requests
# ---------------------------------------------------------------------------

class AnalyzeLinkRequest(BaseModel):
    """Payload de entrada para analise de um link."""

    url: str = Field(
        ...,
        min_length=1,
        max_length=2083,
        examples=["https://www.google.com"],
        description="URL completa a ser analisada (deve incluir scheme http/https).",
    )

    @field_validator("url")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        return v.strip()


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------

class AnalyzeLinkResponse(BaseModel):
    """Resposta padrao para operacoes de analise."""

    url: str
    risk: str = Field(description="Nivel de risco: safe | medium | high")
    reasons: List[str] = Field(description="Motivos que levaram ao risco identificado.")
    created_at: datetime

    model_config = {"from_attributes": True}


class ErrorResponse(BaseModel):
    """Formato padrao de erro retornado pela API."""

    error: str
    detail: str
    status_code: int
