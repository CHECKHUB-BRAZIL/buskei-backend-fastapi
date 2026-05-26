class QRCodeApplicationException(Exception):
    """
    Exceção base da camada de application
    do módulo de QRCode.
    """

    def __init__(
        self,
        message: str = (
            "Erro na aplicação de QRCode."
        ),
    ):
        self.message = message

        super().__init__(message)


class QRCodeAnalysisFailedException(
    QRCodeApplicationException,
):
    """
    Erro ao executar análise do QRCode.
    """

    def __init__(
        self,
        message: str = (
            "Falha ao analisar QRCode."
        ),
    ):
        super().__init__(message)


class QRCodeImageReadException(
    QRCodeApplicationException,
):
    """
    Erro ao ler/processar imagem enviada.
    """

    def __init__(
        self,
        message: str = (
            "Não foi possível processar "
            "a imagem do QRCode."
        ),
    ):
        super().__init__(message)
