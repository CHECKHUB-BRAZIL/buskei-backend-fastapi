from app.modules.link_analysis.application.dtos.link_analysis_dto import (
    GetAnalysisInputDTO,
    GetAnalysisOutputDTO,
)
from app.modules.link_analysis.domain.exceptions.exceptions import (
    AnalysisNotFoundError,
    InvalidURLError,
)
from app.modules.link_analysis.domain.repositories.link_analysis_repository import (
    LinkAnalysisRepository,
)
from app.modules.link_analysis.domain.value_objects.url_vo import URL


class GetAnalysisUseCase:
    def __init__(self, repository: LinkAnalysisRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: GetAnalysisInputDTO) -> GetAnalysisOutputDTO:
        try:
            url = URL(value=input_dto.url)
        except ValueError:
            raise InvalidURLError(input_dto.url)

        user_id = input_dto.user_id

        # agora filtrado por usuário
        analysis = self._repository.find_by_url(url, user_id=user_id)

        if analysis is None:
            raise AnalysisNotFoundError(input_dto.url)

        return GetAnalysisOutputDTO(
            url=str(analysis.url),
            risk=analysis.risk,
            reasons=list(analysis.reasons),
            created_at=analysis.created_at,
        )
