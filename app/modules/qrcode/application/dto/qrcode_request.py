from pydantic import BaseModel
from pydantic import Field


class QRCodeAnalyzeRequest(BaseModel):
    """
    DTO de entrada para análise
    antifraude de QRCode.
    """

    content: str = Field(
        ...,
        examples=[
            "https://google.com",
            "00020126580014BR.GOV.BCB.PIX...",
        ],
        description=(
            "Conteúdo textual extraído "
            "do QRCode."
        ),
    )

    model_config = {
        "from_attributes": True,
    }
