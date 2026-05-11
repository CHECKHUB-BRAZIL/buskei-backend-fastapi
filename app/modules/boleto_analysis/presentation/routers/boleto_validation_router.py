from fastapi import APIRouter, Depends, status

from app.modules.auth.domain.entities.user_entity import UserEntity

from app.modules.auth.presentation.http.dependencies.auth_deps import (
    get_current_user,
)

from app.modules.boleto_analysis.application.dtos.boleto_validation_dto import (
    ValidateBoletoInputDTO,
)

from app.modules.boleto_analysis.application.use_cases.validate_boleto_use_case import (
    ValidateBoletoUseCase,
)

from app.modules.boleto_analysis.domain.services.boleto_analysis_service import (
    BoletoAnalysisService,
)

from app.modules.boleto_analysis.presentation.schemas.boleto_validation_schema import (
    BoletoValidationResponse,
    ValidateBoletoRequest,
)

router = APIRouter(
    prefix="/boletos",
    tags=["Boleto Analysis"],
)


@router.post(
    "/validate",
    response_model=BoletoValidationResponse,
    status_code=status.HTTP_200_OK,
)
def validate_boleto(
    body: ValidateBoletoRequest,
    current_user: UserEntity = Depends(get_current_user),
):
    """
    Executa análise antifraude do boleto.
    Requer autenticação.
    """

    analysis_service = BoletoAnalysisService()

    use_case = ValidateBoletoUseCase(
        analysis_service=analysis_service,
    )

    output = use_case.execute(
        ValidateBoletoInputDTO(
            code=body.code,
        )
    )

    return BoletoValidationResponse(
        **output.__dict__
    )
