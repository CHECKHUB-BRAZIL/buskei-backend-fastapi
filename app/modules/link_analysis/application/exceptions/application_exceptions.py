from app.modules.link_analysis.domain.exceptions.exceptions import (
    InvalidURLError,
    LinkAnalysisDomainError,
    URLTooLongError,
    UnsupportedSchemeError,
)


# ==========================================================
# BASE
# ==========================================================

class LinkAnalysisApplicationError(Exception):
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
# VALIDATION
# ==========================================================

class LinkValidationError(LinkAnalysisApplicationError):
    """
    Erros estruturais da URL:
    - URL inválida
    - tamanho excessivo
    - scheme não suportado
    """

    def __init__(self, message: str) -> None:
        super().__init__(
            message=message,
            status_code=400,
        )


# ==========================================================
# INTERNAL
# ==========================================================

class LinkAnalysisInternalError(LinkAnalysisApplicationError):
    """
    Erro interno inesperado.
    """

    def __init__(
        self,
        message: str = "Erro interno ao analisar link.",
    ) -> None:
        super().__init__(
            message=message,
            status_code=500,
        )


# ==========================================================
# DOMAIN -> APPLICATION
# ==========================================================

def map_domain_exception(
    exc: LinkAnalysisDomainError,
) -> LinkAnalysisApplicationError:
    """
    Traduz erros do domínio para erros HTTP/application.
    """

    mapping = {
        InvalidURLError:
            lambda e: LinkValidationError(str(e)),

        URLTooLongError:
            lambda e: LinkValidationError(str(e)),

        UnsupportedSchemeError:
            lambda e: LinkValidationError(str(e)),
    }

    handler = mapping.get(type(exc))

    if handler:
        return handler(exc)

    return LinkAnalysisInternalError(str(exc))
