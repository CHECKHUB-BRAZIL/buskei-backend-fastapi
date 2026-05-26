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
    )

    qrcode_type: str = Field(
        ...,
        description="Tipo identificado do QRCode",
        examples=[
            "pix",
            "url",
            "text",
        ],
    )

    is_valid: bool = Field(
        ...,
        description="Indica se o QRCode é válido",
    )

    risk_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Pontuação de risco antifraude",
    )

    status: str = Field(
        ...,
        description="Status da análise",
        examples=[
            "safe",
            "suspicious",
            "malicious",
        ],
    )

    reason: str | None = Field(
        default=None,
        description="Motivo principal da análise",
    )

    pix_key: str | None = Field(
        default=None,
        description="Chave PIX detectada",
    )

    merchant_name: str | None = Field(
        default=None,
        description="Nome do recebedor",
    )

    amount: float | None = Field(
        default=None,
        description="Valor identificado",
    )

    detected_url: str | None = Field(
        default=None,
        description="URL detectada no QRCode",
    )

    is_suspicious_url: bool = Field(
        default=False,
        description="Indica se a URL é suspeita",
    )

    has_unknown_domain: bool = Field(
        default=False,
        description="Indica domínio desconhecido",
    )

    class Config:
        from_attributes = True
