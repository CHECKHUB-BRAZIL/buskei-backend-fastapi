from abc import ABC
from abc import abstractmethod

from app.modules.qrcode.domain.value_objects.qrcode_data import (
    QRCodeData,
)


class QRCodeAnalyzerService(ABC):
    """
    Serviço de domínio responsável por:

    - validar estrutura do QRCode
    - detectar fraude
    - analisar risco
    """

    @abstractmethod
    def analyze(
        self,
        content: str,
    ) -> QRCodeData:
        """
        Analisa conteúdo de um QRCode
        e retorna os dados antifraude.
        """
        pass
