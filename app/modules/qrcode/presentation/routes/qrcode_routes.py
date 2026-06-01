from fastapi import APIRouter
from fastapi import Depends

from app.modules.auth.domain.entities.user_entity import (
    UserEntity,
)

from app.modules.auth.presentation.http.dependencies.auth_deps import (
    get_current_user,
)

from app.modules.qrcode.application.usecases.analyze_qrcode_usecase import (
    AnalyzeQRCodeUseCase,
)


from app.modules.qrcode.infrastructure.services.antifraud_qrcode_service import (
    AntiFraudQRCodeService,
)
from app.modules.qrcode.presentation.schemas.qrcode_request_schema import (
    QRCodeAnalyzeRequest,
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

qrcode_service = AntiFraudQRCodeService()

analyze_qrcode_usecase = AnalyzeQRCodeUseCase(
    analyzer_service=qrcode_service,
)

# ==========================================================
# ROUTES
# ==========================================================


@router.post(
    "/analyze",
    response_model=QRCodeResponseSchema,
)
async def analyze_qrcode(
    payload: QRCodeAnalyzeRequest,

    current_user: UserEntity = Depends(
        get_current_user,
    ),
):
    """
    Analisa QRCode com validação antifraude.
    """

    result = analyze_qrcode_usecase.execute(
        content=payload.content,
    )

    return QRCodeResponseSchema(
        raw_value=result.raw_value,
        qrcode_type=result.qrcode_type,
        is_valid=result.is_valid,
        risk_score=result.risk_score,
        status=result.status,
        reasons=result.reasons,
        positives=result.positives,
        pix_key=result.pix_key,
        merchant_name=result.merchant_name,
        amount=result.amount,
        detected_url=result.detected_url,
        is_suspicious_url=result.is_suspicious_url,
        has_unknown_domain=result.has_unknown_domain,
    )
