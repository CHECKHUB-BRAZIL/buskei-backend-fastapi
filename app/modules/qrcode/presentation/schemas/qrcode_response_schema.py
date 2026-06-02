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
        description="Tipo identificado",
        examples=[
            "pix",
            "url",
            "generic",
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
        description="Pontuação de risco",
    )

    status: str = Field(
        ...,
        description="Resultado da análise",
        examples=[
            "safe",
            "attention",
            "suspicious",
            "fraud_suspect",
        ],
    )

    reasons: list[str] = Field(
        default_factory=list,
        description="Motivos que aumentaram o risco",
    )

    positives: list[str] = Field(
        default_factory=list,
        description="Aspectos considerados seguros",
    )

    pix_key: str | None = Field(
        default=None,
        description="Chave PIX identificada",
    )

    merchant_name: str | None = Field(
        default=None,
        description="Nome do recebedor",
    )

    city: str | None = Field(
        default=None,
        description="Cidade do recebedor identificada no PIX",
    )

    amount: float | None = Field(
        default=None,
        description="Valor encontrado",
    )

    txid: str | None = Field(
        default=None,
        description="TXID encontrado no payload PIX",
    )

    is_valid_crc: bool | None = Field(
        default=None,
        description="Indica se o checksum CRC16 do PIX é válido",
    )

    detected_url: str | None = Field(
        default=None,
        description="URL identificada",
    )

    is_suspicious_url: bool = Field(
        default=False,
        description="Indica URL suspeita",
    )

    has_unknown_domain: bool = Field(
        default=False,
        description="Indica domínio desconhecido",
    )

    model_config = {
        "from_attributes": True,
    }
