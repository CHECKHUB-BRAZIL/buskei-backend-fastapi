from pydantic import BaseModel
from pydantic import Field


class QRCodeResponseSchema(BaseModel):
    """
    Schema HTTP de resposta da análise
    antifraude do QRCode.
    """

    raw_value: str = Field(
        ...,
        description="Conteúdo bruto encontrado no QRCode",
        examples=[
            "https://google.com",
            "00020126580014BR.GOV.BCB.PIX...",
        ],
    )

    qr_type: str = Field(
        ...,
        description="Tipo identificado do QRCode",
        examples=[
            "pix",
            "url",
            "text",
        ],
    )

    is_safe: bool = Field(
        ...,
        description="Indica se o QRCode aparenta ser seguro",
    )

    risk_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Pontuação de risco antifraude",
        examples=[15, 72],
    )

    status: str = Field(
        ...,
        description=(
            "Status da análise "
            "(safe | suspicious | malicious)"
        ),
        examples=[
            "safe",
            "suspicious",
            "malicious",
        ],
    )

    reasons: list[str] = Field(
        default_factory=list,
        description="Motivos e alertas detectados",
    )

    class Config:
        from_attributes = True
