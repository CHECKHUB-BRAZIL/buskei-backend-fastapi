from typing import Optional

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
        examples=[
            "pix",
            "url",
            "generic",
            "payment",
        ],
        description="Tipo identificado do QRCode.",
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
        examples=[
            "safe",
            "suspicious",
            "fraud_suspect",
        ],
        description="Status antifraude.",
    )

    reason: Optional[str] = Field(
        default=None,
        description="Motivo da classificação.",
    )

    # PIX
    pix_key: Optional[str] = Field(
        default=None,
        description="Chave PIX detectada.",
    )

    merchant_name: Optional[str] = Field(
        default=None,
        description="Nome do recebedor.",
    )

    amount: Optional[float] = Field(
        default=None,
        description="Valor detectado.",
    )

    # URLs
    detected_url: Optional[str] = Field(
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
        "from_attributes": True
    }
