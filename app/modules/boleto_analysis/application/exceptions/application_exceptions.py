from app.modules.boleto_analysis.domain.exceptions.exceptions import (
    BoletoDomainError,
    BoletoValidationNotFoundError,
    DuplicateBoletoValidationError,
    InvalidAmountError,
    InvalidBoletoCodeError,
    UnsupportedBoletoTypeError,
)


# ---------------------------------------------------------------------------
# Hierarquia de exceções da camada de aplicação
# ---------------------------------------------------------------------------

class BoletoApplicationError(Exception):
    """
    Exceção base da camada de aplicação de boletos.
    Carrega o HTTP status code sugerido para a apresentação.
    """

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class BoletoValidationError(BoletoApplicationError):
    """Erro de validação de entrada — código malformado, valor inválido (400)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)


class BoletoNotFoundError(BoletoApplicationError):
    """Validação não encontrada para o código informado (404)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=404)


class BoletoConflictError(BoletoApplicationError):
    """Tentativa de persistir validação duplicada (409)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=409)


class BoletoUnsupportedTypeError(BoletoApplicationError):
    """Tipo de boleto não suportado pelo sistema (422)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=422)


# ---------------------------------------------------------------------------
# Mapeador: exceções de domínio → exceções de aplicação
# ---------------------------------------------------------------------------

def map_domain_exception(exc: BoletoDomainError) -> BoletoApplicationError:
    """
    Traduz exceções de domínio para exceções da camada de aplicação.

    Centraliza a conversão em um único ponto, mantendo os use cases
    e a apresentação desacoplados do domínio.

    Usage:
        except BoletoDomainError as exc:
            raise map_domain_exception(exc)
    """
    mapping = {
        InvalidBoletoCodeError:       lambda e: BoletoValidationError(str(e)),
        InvalidAmountError:           lambda e: BoletoValidationError(str(e)),
        UnsupportedBoletoTypeError:   lambda e: BoletoUnsupportedTypeError(str(e)),
        BoletoValidationNotFoundError: lambda e: BoletoNotFoundError(str(e)),
        DuplicateBoletoValidationError: lambda e: BoletoConflictError(str(e)),
    }

    handler = mapping.get(type(exc))
    if handler:
        return handler(exc)

    return BoletoApplicationError(str(exc), status_code=500)
