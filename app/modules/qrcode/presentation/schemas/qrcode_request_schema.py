from pydantic import BaseModel


class QRCodeAnalyzeRequest(BaseModel):
    content: str
