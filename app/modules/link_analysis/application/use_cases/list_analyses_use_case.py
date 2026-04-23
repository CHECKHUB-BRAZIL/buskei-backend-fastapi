from typing import List

from app.modules.link_analysis.application.dtos.link_analysis_dto import AnalyzeLinkOutputDTO, ListAnalysesInputDTO
from app.modules.link_analysis.domain.repositories.link_analysis_repository import (
    LinkAnalysisRepository,
)

class ListAnalysesUseCase:
    def __init__(self, repository: LinkAnalysisRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: ListAnalysesInputDTO) -> List[AnalyzeLinkOutputDTO]:
        user_id = input_dto.user_id

        analyses = self._repository.find_all(user_id=user_id)

        return [
            AnalyzeLinkOutputDTO(
                url=str(analysis.url),
                risk=analysis.risk,
                reasons=list(analysis.reasons),
                created_at=analysis.created_at,
            )
            for analysis in analyses
        ]
