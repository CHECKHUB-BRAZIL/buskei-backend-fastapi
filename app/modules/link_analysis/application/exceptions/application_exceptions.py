from app.modules.link_analysis.domain.exceptions.exceptions import (
    AnalysisNotFoundError,
    DuplicateAnalysisError,
    InvalidURLError,
    LinkAnalysisDomainError,
    URLTooLongError,
    UnsupportedSchemeError,
)


class ApplicationError(Exception):
    """
    Exceção base da camada de aplicação.
    Carrega um código de status HTTP sugerido para a apresentação.
    """

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ValidationError(ApplicationError):
    """Erro de validação de entrada (400)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)


class NotFoundError(ApplicationError):
    """Recurso não encontrado (404)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=404)


class ConflictError(ApplicationError):
    """Conflito de dados, ex: duplicata (409)."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=409)


# ---------------------------------------------------------------------------
# Mapeador: exceções de domínio → exceções de aplicação
# ---------------------------------------------------------------------------

def map_domain_exception(exc: LinkAnalysisDomainError) -> ApplicationError:
    """
    Traduz exceções de domínio para exceções da camada de aplicação.

    Centraliza a conversão em um único ponto, mantendo os casos de uso
    limpos e a apresentação desacoplada do domínio.

    Usage (dentro de um use case ou na apresentação):
        except LinkAnalysisDomainError as exc:
            raise map_domain_exception(exc)
    """
    mapping = {
        InvalidURLError: lambda e: ValidationError(str(e)),
        URLTooLongError: lambda e: ValidationError(str(e)),
        UnsupportedSchemeError: lambda e: ValidationError(str(e)),
        AnalysisNotFoundError: lambda e: NotFoundError(str(e)),
        DuplicateAnalysisError: lambda e: ConflictError(str(e)),
    }

    handler = mapping.get(type(exc))
    if handler:
        return handler(exc)

    # fallback genérico para exceções de domínio não mapeadas
    return ApplicationError(str(exc), status_code=500)
