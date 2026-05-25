from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from app.modules.auth.domain.entities.user_entity import (
    UserEntity,
)

from app.modules.auth.presentation.http.dependencies.auth_deps import (
    get_current_user,
)

from app.modules.qrcode.application.usecases.analyze_qrcode_usecase import (
    AnalyzeQRCodeUseCase,
)

from app.modules.qrcode.domain.exceptions.qrcode_exceptions import (
    InvalidQRCodeException,
    QRCodeDomainException,
)

from app.modules.qrcode.infrastructure.services.pyzbar_qrcode_service import (
    PyzbarQRCodeService,
)

from app.modules.qrcode.presentation.schemas.qrcode_response_schema import (
    QRCodeResponseSchema,
)

router = APIRouter(
    prefix="/qrcode",
    tags=["QRCode"],
)

# ==========================================================
# DEPENDENCIES
# ==========================================================

qrcode_service = PyzbarQRCodeService()

analyze_qrcode_usecase = AnalyzeQRCodeUseCase(
    analyzer_service=qrcode_service,
)

# ==========================================================
# ROUTES
# ==========================================================


@router.post(
    "/analyze",
    response_model=QRCodeResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def analyze_qrcode(
    file: UploadFile = File(...),

    current_user: UserEntity = Depends(
        get_current_user,
    ),
):
    """
    Analisa QRCode com validação antifraude.
    Requer autenticação.
    """

    if not file.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "O arquivo enviado "
                "deve ser uma imagem."
            ),
        )

    try:
        image_bytes = await file.read()

        result = analyze_qrcode_usecase.execute(
            image_bytes=image_bytes,
        )

        return QRCodeResponseSchema(
            raw_value=result.raw_value,
            qr_type=result.qr_type,
            is_safe=result.is_safe,
            risk_score=result.risk_score,
            status=result.status,
            reasons=result.reasons,
        )

    except InvalidQRCodeException as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except QRCodeDomainException as e:
        raise HTTPException(
            status_code=422,
            detail=str(e),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "Erro interno ao analisar "
                "QRCode."
            ),
        )
