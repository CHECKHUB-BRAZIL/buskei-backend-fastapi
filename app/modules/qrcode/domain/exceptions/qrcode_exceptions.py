class QRCodeDomainException(Exception):
    """
    Exceção base do domínio de QRCode.
    """

    def __init__(self, message: str):
        self.message = message

        super().__init__(message)


class InvalidQRCodeException(QRCodeDomainException):
    """
    Conteúdo de QRCode inválido.
    """

    def __init__(self):
        super().__init__(
            "O conteúdo do QRCode é inválido."
        )

class SuspiciousQRCodeException(QRCodeDomainException):
    """
    QRCode considerado suspeito.
    """

    def __init__(self, reason: str):
        super().__init__(
            f"QRCode suspeito detectado: {reason}"
        )


class UnsupportedQRCodeTypeException(
    QRCodeDomainException,
):
    """
    Tipo de QRCode não suportado.
    """

    def __init__(self, qrcode_type: str):
        super().__init__(
            f"Tipo de QRCode não suportado: {qrcode_type}"
        )


class MaliciousURLException(
    QRCodeDomainException,
):
    """
    URL maliciosa detectada no QRCode.
    """

    def __init__(self, url: str):
        super().__init__(
            f"URL suspeita detectada: {url}"
        )
