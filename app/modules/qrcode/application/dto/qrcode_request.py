from pydantic import BaseModel
from pydantic import Field


class QRCodeRequest(BaseModel):
    """
    DTO de entrada para análise antifraude
    de QRCode.
    """

    filename: str = Field(
        ...,
        examples=["qrcode.png"],
        description="Nome do arquivo enviado.",
    )

    content_type: str = Field(
        ...,
        examples=["image/png"],
        description="Tipo MIME da imagem.",
    )

    model_config = {
        "from_attributes": True
    }
