from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modules.link_analysis.application.exceptions.application_exceptions import (
    ApplicationError,
    ConflictError,
    NotFoundError,
    ValidationError,
    map_domain_exception,
)
from app.modules.link_analysis.domain.exceptions.exceptions import LinkAnalysisDomainError
from app.modules.link_analysis.presentation.schemas.link_analysis_schema import ErrorResponse


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra os handlers globais de excecao na instancia FastAPI.

    Ordem de captura (do mais especifico ao mais generico):
        1. Erros de validacao da camada de aplicacao  → 400
        2. Erros de nao encontrado                    → 404
        3. Erros de conflito                          → 409
        4. Qualquer ApplicationError remanescente     → status do erro
        5. Erros de dominio nao tratados              → 422
        6. Excecoes nao previstas                     → 500

    Usage (em main.py ou app factory):
        from presentation.exception_handlers import register_exception_handlers
        register_exception_handlers(app)
    """

    @app.exception_handler(ValidationError)
    def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="ValidationError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(NotFoundError)
    def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="NotFoundError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(ConflictError)
    def conflict_error_handler(request: Request, exc: ConflictError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="ConflictError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(ApplicationError)
    def application_error_handler(request: Request, exc: ApplicationError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="ApplicationError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(LinkAnalysisDomainError)
    def domain_error_handler(
        request: Request, exc: LinkAnalysisDomainError
    ) -> JSONResponse:
        # Dominio escapou sem ser mapeado — converte e responde
        mapped = map_domain_exception(exc)
        return JSONResponse(
            status_code=mapped.status_code,
            content=ErrorResponse(
                error=type(exc).__name__,
                detail=mapped.message,
                status_code=mapped.status_code,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="InternalServerError",
                detail="Ocorreu um erro inesperado. Tente novamente mais tarde.",
                status_code=500,
            ).model_dump(),
        )
