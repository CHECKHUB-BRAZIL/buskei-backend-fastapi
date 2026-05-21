from abc import ABC
from abc import abstractmethod

from app.modules.qrcode.domain.value_objects.qrcode_data import (
    QRCodeData,
)


class QRCodeAnalyzerService(ABC):
    """
    Serviço de domínio responsável por:

    - decodificar QRCode
    - validar estrutura
    - detectar fraude
    - analisar risco
    """

    @abstractmethod
    def analyze(
        self,
        image_bytes: bytes,
    ) -> QRCodeData:
        """
        Analisa um QRCode e retorna
        os dados antifraude.
        """
        pass
