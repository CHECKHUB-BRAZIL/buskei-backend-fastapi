from fastapi import APIRouter, Depends, status

from app.modules.auth.domain.entities.user_entity import (
    UserEntity,
)

from app.modules.auth.presentation.http.dependencies.auth_deps import (
    get_current_user,
)

from app.modules.link_analysis.application.dtos.link_analysis_dto import (
    AnalyzeLinkInputDTO,
)

from app.modules.link_analysis.application.use_cases.analyze_link_use_case import (
    AnalyzeLinkUseCase,
)

from app.modules.link_analysis.domain.services.link_analysis_service import (
    LinkAnalysisService,
)

from app.modules.link_analysis.presentation.schemas.link_analysis_schema import (
    AnalyzeLinkRequest,
    AnalyzeLinkResponse,
)

router = APIRouter(
    prefix="/links",
    tags=["Link Analysis"],
)


# ==========================================================
# POST /links/analyze
# ==========================================================

@router.post(
    "/analyze",
    response_model=AnalyzeLinkResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_link(
    body: AnalyzeLinkRequest,
    current_user: UserEntity = Depends(get_current_user),
):
    """
    Executa análise antifraude de URL.
    Requer autenticação.
    """

    service = LinkAnalysisService()

    use_case = AnalyzeLinkUseCase(
        service=service,
    )

    output = use_case.execute(
        AnalyzeLinkInputDTO(
            url=body.url,
        )
    )

    return AnalyzeLinkResponse(
        **output.__dict__
    )
