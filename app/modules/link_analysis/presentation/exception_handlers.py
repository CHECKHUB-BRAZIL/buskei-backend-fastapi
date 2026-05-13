from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modules.link_analysis.application.exceptions.application_exceptions import (
    LinkAnalysisApplicationError,
    LinkAnalysisInternalError,
    LinkValidationError,
    map_domain_exception,
)

from app.modules.link_analysis.domain.exceptions.exceptions import (
    LinkAnalysisDomainError,
)

from app.modules.link_analysis.presentation.schemas.link_analysis_schema import (
    ErrorResponse,
)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra os handlers globais do módulo link_analysis.

    Ordem:
    - validação (400)
    - erro base de aplicação
    - erro de domínio (mapeado)
    - fallback 500
    """

    # ======================================================
    # 400 - Validation
    # ======================================================

    @app.exception_handler(LinkValidationError)
    def validation_error_handler(
        request: Request,
        exc: LinkValidationError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="LinkValidationError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    # ======================================================
    # Base application error
    # ======================================================

    @app.exception_handler(LinkAnalysisApplicationError)
    def application_error_handler(
        request: Request,
        exc: LinkAnalysisApplicationError,
    ) -> JSONResponse:

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=type(exc).__name__,
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    # ======================================================
    # Domain -> Application mapping
    # ======================================================

    @app.exception_handler(LinkAnalysisDomainError)
    def domain_error_handler(
        request: Request,
        exc: LinkAnalysisDomainError,
    ) -> JSONResponse:

        mapped = map_domain_exception(exc)

        return JSONResponse(
            status_code=mapped.status_code,
            content=ErrorResponse(
                error=type(exc).__name__,
                detail=mapped.message,
                status_code=mapped.status_code,
            ).model_dump(),
        )

    # ======================================================
    # Fallback
    # ======================================================

    @app.exception_handler(Exception)
    def unhandled_error_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        internal = LinkAnalysisInternalError()

        return JSONResponse(
            status_code=internal.status_code,
            content=ErrorResponse(
                error="InternalServerError",
                detail=internal.message,
                status_code=internal.status_code,
            ).model_dump(),
        )
