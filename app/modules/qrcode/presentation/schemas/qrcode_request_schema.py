from pydantic import BaseModel
from pydantic import Field


class QRCodeAnalyzeRequest(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        description="Conteúdo extraído do QRCode",
        examples=[
            "https://google.com",
            "00020126360014BR.GOV.BCB.PIX...",
        ],
    )
