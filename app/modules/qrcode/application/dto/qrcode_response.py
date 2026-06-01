from pydantic import BaseModel
from pydantic import Field


class QRCodeResponse(BaseModel):
    """
    Resposta da análise antifraude
    de QRCode.
    """

    # valor original
    raw_value: str = Field(
        ...,
        description="Conteúdo bruto do QRCode.",
    )

    # tipo detectado
    qrcode_type: str = Field(
        ...,
        description="Tipo identificado do QRCode.",
        examples=[
            "pix",
            "url",
            "generic",
        ],
    )

    # validação
    is_valid: bool = Field(
        ...,
        description="Indica se o QRCode é válido.",
    )

    # antifraude
    risk_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Pontuação de risco do QRCode.",
    )

    status: str = Field(
        ...,
        description="Status da análise.",
        examples=[
            "safe",
            "attention",
            "suspicious",
            "fraud_suspect",
        ],
    )

    reasons: list[str] = Field(
        default_factory=list,
        description="Motivos que aumentaram o risco.",
    )

    positives: list[str] = Field(
        default_factory=list,
        description="Aspectos considerados seguros.",
    )

    # PIX
    pix_key: str | None = Field(
        default=None,
        description="Chave PIX detectada.",
    )

    merchant_name: str | None = Field(
        default=None,
        description="Nome do recebedor.",
    )

    amount: float | None = Field(
        default=None,
        description="Valor detectado.",
    )

    # URLs
    detected_url: str | None = Field(
        default=None,
        description="URL encontrada no QRCode.",
    )

    is_suspicious_url: bool = Field(
        default=False,
        description="Indica se a URL parece suspeita.",
    )

    has_unknown_domain: bool = Field(
        default=False,
        description="Indica domínio desconhecido.",
    )

    model_config = {
        "from_attributes": True,
    }
