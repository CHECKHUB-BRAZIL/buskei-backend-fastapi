from fastapi import File
from fastapi import UploadFile


class QRCodeRequestSchema:
    """
    Schema de entrada para upload da imagem
    contendo o QRCode.
    """

    file: UploadFile = File(
        ...,
        description="Imagem contendo o QRCode",
    )
