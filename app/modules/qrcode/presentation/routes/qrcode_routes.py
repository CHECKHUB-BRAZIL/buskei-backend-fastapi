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
        "image/",
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "O arquivo enviado "
                "deve ser uma imagem."
            ),
        )

    image_bytes = await file.read()

    result = analyze_qrcode_usecase.execute(
        image_bytes=image_bytes,
    )

    return QRCodeResponseSchema(
        raw_value=result.raw_value,
        qrcode_type=result.qrcode_type,
        is_valid=result.is_valid,
        risk_score=result.risk_score,
        status=result.status,
        reason=result.reason,
        pix_key=result.pix_key,
        merchant_name=result.merchant_name,
        amount=result.amount,
        detected_url=result.detected_url,
        is_suspicious_url=result.is_suspicious_url,
        has_unknown_domain=result.has_unknown_domain,
    )
