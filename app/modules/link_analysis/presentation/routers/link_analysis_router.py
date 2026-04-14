from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.link_analysis.application.dtos.link_analysis_dto import (
    AnalyzeLinkInputDTO,
    DeleteAnalysisInputDTO,
    GetAnalysisInputDTO,
)
from app.modules.link_analysis.infrastructure.container import LinkAnalysisContainer
from app.modules.link_analysis.infrastructure.database.session import get_session
from app.modules.link_analysis.presentation.schemas.link_analysis_schema import (
    AnalysisListResponse,
    AnalysisResponse,
    AnalyzeLinkRequest,
    DeleteAnalysisResponse,
)

router = APIRouter(
    prefix="/links",
    tags=["Link Analysis"],
)


def get_container(session: AsyncSession = Depends(get_session)) -> LinkAnalysisContainer:
    return LinkAnalysisContainer(session)


# ---------------------------------------------------------------------------
# POST /links/analyze
# ---------------------------------------------------------------------------

@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analisar um link",
    description=(
        "Recebe uma URL, executa a analise de seguranca baseada nas regras de dominio "
        "e persiste o resultado. Retorna o nivel de risco e os motivos identificados."
    ),
)
async def analyze_link(
    body: AnalyzeLinkRequest,
    container: LinkAnalysisContainer = Depends(get_container),
) -> AnalysisResponse:
    output = await container.analyze_link().execute(
        AnalyzeLinkInputDTO(url=body.url)
    )
    return AnalysisResponse(
        url=output.url,
        risk=output.risk,
        reasons=output.reasons,
        created_at=output.created_at,
    )


# ---------------------------------------------------------------------------
# GET /links
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=AnalysisListResponse,
    status_code=status.HTTP_200_OK,
    summary="Listar todas as analises",
    description="Retorna todas as analises de links ja realizadas, ordenadas da mais recente.",
)
async def list_analyses(
    container: LinkAnalysisContainer = Depends(get_container),
) -> AnalysisListResponse:
    outputs = await container.list_analyses().execute()
    items = [
        AnalysisResponse(
            url=o.url,
            risk=o.risk,
            reasons=o.reasons,
            created_at=o.created_at,
        )
        for o in outputs
    ]
    return AnalysisListResponse(total=len(items), items=items)


# ---------------------------------------------------------------------------
# GET /links/analysis
# ---------------------------------------------------------------------------

@router.get(
    "/analysis",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar analise por URL",
    description="Recupera a analise de seguranca previamente realizada para uma URL especifica.",
)
async def get_analysis(
    url: str = Query(..., min_length=1, max_length=2083, description="URL a ser consultada."),
    container: LinkAnalysisContainer = Depends(get_container),
) -> AnalysisResponse:
    output = await container.get_analysis().execute(
        GetAnalysisInputDTO(url=url)
    )
    return AnalysisResponse(
        url=output.url,
        risk=output.risk,
        reasons=output.reasons,
        created_at=output.created_at,
    )


# ---------------------------------------------------------------------------
# DELETE /links/analysis
# ---------------------------------------------------------------------------

@router.delete(
    "/analysis",
    response_model=DeleteAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Remover analise por URL",
    description="Remove permanentemente a analise associada a uma URL.",
)
async def delete_analysis(
    url: str = Query(..., min_length=1, max_length=2083, description="URL a ser removida."),
    container: LinkAnalysisContainer = Depends(get_container),
) -> DeleteAnalysisResponse:
    await container.delete_analysis().execute(
        DeleteAnalysisInputDTO(url=url)
    )
    return DeleteAnalysisResponse(
        message="Analise removida com sucesso.",
        url=url,
    )
