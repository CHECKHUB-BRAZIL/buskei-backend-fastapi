from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from app.modules.qrcode.application.exceptions.qrcode_application_exceptions import (
    QRCodeApplicationException,
)

from app.modules.qrcode.domain.exceptions.qrcode_exceptions import (
    InvalidQRCodeException,
    QRCodeDomainException,
)


# ==========================================================
# DOMAIN EXCEPTIONS
# ==========================================================

async def invalid_qrcode_exception_handler(
    request: Request,
    exc: InvalidQRCodeException,
):
    return JSONResponse(
        status_code=400,
        content={
            "error": "invalid_qrcode",
            "detail": str(exc),
        },
    )


async def qrcode_domain_exception_handler(
    request: Request,
    exc: QRCodeDomainException,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": "qrcode_domain_error",
            "detail": str(exc),
        },
    )


# ==========================================================
# APPLICATION EXCEPTIONS
# ==========================================================

async def qrcode_application_exception_handler(
    request: Request,
    exc: QRCodeApplicationException,
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "qrcode_application_error",
            "detail": str(exc),
        },
    )


# ==========================================================
# REGISTER
# ==========================================================

def register_qrcode_exception_handlers(
    app: FastAPI,
):
    app.add_exception_handler(
        InvalidQRCodeException,
        invalid_qrcode_exception_handler,
    )

    app.add_exception_handler(
        QRCodeDomainException,
        qrcode_domain_exception_handler,
    )

    app.add_exception_handler(
        QRCodeApplicationException,
        qrcode_application_exception_handler,
    )
