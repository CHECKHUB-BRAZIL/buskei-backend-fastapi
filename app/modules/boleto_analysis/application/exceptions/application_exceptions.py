from app.modules.boleto_analysis.domain.exceptions.exceptions import (
    BoletoDomainError,
    InvalidAmountError,
    InvalidBoletoCodeError,
    UnsupportedBoletoTypeError,
)


# ==========================================================
# BASE
# ==========================================================

class BoletoApplicationError(Exception):
    """
    Exceção base da camada de aplicação.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ) -> None:
        self.message = message
        self.status_code = status_code

        super().__init__(message)


# ==========================================================
# VALIDAÇÃO / INPUT
# ==========================================================

class BoletoValidationError(BoletoApplicationError):
    """
    Erros estruturais do boleto:
    - parsing
    - tamanho inválido
    - valor inválido
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=400,
        )


# ==========================================================
# TIPO NÃO SUPORTADO
# ==========================================================

class BoletoUnsupportedTypeError(BoletoApplicationError):
    """
    Tipo de boleto não suportado.
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=422,
        )


# ==========================================================
# FALLBACK
# ==========================================================

class BoletoInternalError(BoletoApplicationError):
    """
    Erro interno inesperado.
    """

    def __init__(
        self,
        message: str = "Erro interno ao processar boleto.",
    ) -> None:
        super().__init__(
            message=message,
            status_code=500,
        )


# ==========================================================
# DOMAIN -> APPLICATION
# ==========================================================

def map_domain_exception(
    exc: BoletoDomainError,
) -> BoletoApplicationError:
    """
    Traduz erros do domínio para erros HTTP/application.
    """

    mapping = {
        InvalidBoletoCodeError:
            lambda e: BoletoValidationError(str(e)),

        InvalidAmountError:
            lambda e: BoletoValidationError(str(e)),

        UnsupportedBoletoTypeError:
            lambda e: BoletoUnsupportedTypeError(str(e)),
    }

    handler = mapping.get(type(exc))

    if handler:
        return handler(exc)

    return BoletoInternalError(str(exc))
