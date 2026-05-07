from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modules.boleto_analysis.application.exceptions.application_exceptions import (
    BoletoApplicationError,
    BoletoConflictError,
    BoletoNotFoundError,
    BoletoUnsupportedTypeError,
    BoletoValidationError,
    map_domain_exception,
)
from app.modules.boleto_analysis.domain.exceptions.exceptions import BoletoDomainError
from app.modules.boleto_analysis.presentation.schemas.boleto_validation_schema import (
    ErrorResponse,
)


def register_boleto_exception_handlers(app: FastAPI) -> None:
    """
    Registra os handlers globais de exceção do módulo boleto_validation.

    Ordem de captura (do mais específico ao mais genérico):
        1. BoletoValidationError     → 400 (código malformado, valor inválido)
        2. BoletoNotFoundError       → 404 (validação não encontrada)
        3. BoletoConflictError       → 409 (código já validado)
        4. BoletoUnsupportedTypeError → 422 (tipo de boleto não suportado)
        5. BoletoApplicationError    → status do erro (fallback de aplicação)
        6. BoletoDomainError         → mapeado dinamicamente (domínio escapou)
        7. Exception                 → 500 (erro inesperado)

    Usage (em main.py ou app factory):
        from presentation.exception_handlers import register_boleto_exception_handlers
        register_boleto_exception_handlers(app)
    """

    @app.exception_handler(BoletoValidationError)
    def boleto_validation_error_handler(
        request: Request, exc: BoletoValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="BoletoValidationError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(BoletoNotFoundError)
    def boleto_not_found_handler(
        request: Request, exc: BoletoNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="BoletoNotFoundError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(BoletoConflictError)
    def boleto_conflict_handler(
        request: Request, exc: BoletoConflictError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="BoletoConflictError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(BoletoUnsupportedTypeError)
    def boleto_unsupported_type_handler(
        request: Request, exc: BoletoUnsupportedTypeError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="BoletoUnsupportedTypeError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(BoletoApplicationError)
    def boleto_application_error_handler(
        request: Request, exc: BoletoApplicationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="BoletoApplicationError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    @app.exception_handler(BoletoDomainError)
    def boleto_domain_error_handler(
        request: Request, exc: BoletoDomainError
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

    @app.exception_handler(Exception)
    def unhandled_error_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="InternalServerError",
                detail="Ocorreu um erro inesperado. Tente novamente mais tarde.",
                status_code=500,
            ).model_dump(),
        )
