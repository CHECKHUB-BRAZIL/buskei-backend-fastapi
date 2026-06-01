from pydantic import BaseModel
from pydantic import Field


class QRCodeAnalyzeRequest(BaseModel):
    """
    DTO de entrada para análise
    antifraude de QRCode.
    """

    content: str = Field(
        ...,
        min_length=1,
        description=(
            "Conteúdo textual extraído "
            "do QRCode."
        ),
        examples=[
            "https://google.com",
            "00020126360014BR.GOV.BCB.PIX...",
        ],
    )

    model_config = {
        "from_attributes": True,
    }
