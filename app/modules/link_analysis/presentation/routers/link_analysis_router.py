from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.modules.link_analysis.application.dtos.link_analysis_dto import AnalyzeLinkInputDTO, GetAnalysisInputDTO
from app.shared.infrastructure.database.session import get_db

from app.modules.link_analysis.infrastructure.repositories.link_analysis_repository_impl import (
    SQLAlchemyLinkAnalysisRepository,
)

from app.modules.link_analysis.application.use_cases.analyze_link_use_case import (
    AnalyzeLinkUseCase,
)
from app.modules.link_analysis.application.use_cases.list_analyses_use_case import (
    ListAnalysesUseCase,
)
from app.modules.link_analysis.application.use_cases.get_analysis_use_case import (
    GetAnalysisUseCase,
)
from app.modules.link_analysis.application.use_cases.delete_analysis_use_case import (
    DeleteAnalysisInputDTO,
    DeleteAnalysisUseCase,
)


from app.modules.link_analysis.presentation.schemas.link_analysis_schema import (
    AnalysisListResponse,
    AnalysisResponse,
    AnalyzeLinkRequest,
    DeleteAnalysisResponse,
)

router = APIRouter(prefix="/links", tags=["Link Analysis"])


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_link(body: AnalyzeLinkRequest, db: Session = Depends(get_db)):
    repo = SQLAlchemyLinkAnalysisRepository(db)
    use_case = AnalyzeLinkUseCase(repo)

    output = use_case.execute(
        AnalyzeLinkInputDTO(url=body.url)
    )

    return AnalysisResponse(**output.__dict__)


@router.get("", response_model=AnalysisListResponse)
def list_analyses(db: Session = Depends(get_db)):
    repo = SQLAlchemyLinkAnalysisRepository(db)
    use_case = ListAnalysesUseCase(repo)

    outputs = use_case.execute()

    return AnalysisListResponse(
        total=len(outputs),
        items=[AnalysisResponse(**o.__dict__) for o in outputs],
    )


@router.get("/analysis", response_model=AnalysisResponse)
def get_analysis(url: str = Query(...), db: Session = Depends(get_db)):
    repo = SQLAlchemyLinkAnalysisRepository(db)
    use_case = GetAnalysisUseCase(repo)

    output = use_case.execute(
        GetAnalysisInputDTO(url=url)
    )

    return AnalysisResponse(**output.__dict__)


@router.delete("/analysis", response_model=DeleteAnalysisResponse)
def delete_analysis(url: str = Query(...), db: Session = Depends(get_db)):
    repo = SQLAlchemyLinkAnalysisRepository(db)
    use_case = DeleteAnalysisUseCase(repo)

    use_case.execute(
        DeleteAnalysisInputDTO(url=url)
    )

    return DeleteAnalysisResponse(
        message="Analysis removed successfully.",
        url=url,
    )
