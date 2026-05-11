from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.modules.boleto_analysis.application.exceptions.application_exceptions import (
    BoletoApplicationError,
    BoletoInternalError,
    BoletoUnsupportedTypeError,
    BoletoValidationError,
    map_domain_exception,
)

from app.modules.boleto_analysis.domain.exceptions.exceptions import (
    BoletoDomainError,
)

from app.modules.boleto_analysis.presentation.schemas.boleto_validation_schema import (
    ErrorResponse,
)


def register_boleto_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Handlers globais do módulo boleto_analysis.

    Fluxo simplificado:
    - 400 → erros estruturais/validação
    - 422 → tipo não suportado
    - 500 → erros internos
    """

    # ==========================================================
    # 400 - Validation
    # ==========================================================

    @app.exception_handler(BoletoValidationError)
    def boleto_validation_error_handler(
        request: Request,
        exc: BoletoValidationError,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="BoletoValidationError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    # ==========================================================
    # 422 - Unsupported Type
    # ==========================================================

    @app.exception_handler(BoletoUnsupportedTypeError)
    def boleto_unsupported_type_handler(
        request: Request,
        exc: BoletoUnsupportedTypeError,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error="BoletoUnsupportedTypeError",
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    # ==========================================================
    # Base Application Error
    # ==========================================================

    @app.exception_handler(BoletoApplicationError)
    def boleto_application_error_handler(
        request: Request,
        exc: BoletoApplicationError,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=type(exc).__name__,
                detail=exc.message,
                status_code=exc.status_code,
            ).model_dump(),
        )

    # ==========================================================
    # Domain -> Application Mapping
    # ==========================================================

    @app.exception_handler(BoletoDomainError)
    def boleto_domain_error_handler(
        request: Request,
        exc: BoletoDomainError,
    ):
        mapped = map_domain_exception(exc)

        return JSONResponse(
            status_code=mapped.status_code,
            content=ErrorResponse(
                error=type(exc).__name__,
                detail=mapped.message,
                status_code=mapped.status_code,
            ).model_dump(),
        )

    # ==========================================================
    # Fallback
    # ==========================================================

    @app.exception_handler(Exception)
    def unhandled_error_handler(
        request: Request,
        exc: Exception,
    ):
        internal = BoletoInternalError()

        return JSONResponse(
            status_code=internal.status_code,
            content=ErrorResponse(
                error="InternalServerError",
                detail=internal.message,
                status_code=internal.status_code,
            ).model_dump(),
        )
