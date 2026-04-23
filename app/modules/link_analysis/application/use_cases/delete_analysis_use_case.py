from dataclasses import dataclass

from app.modules.link_analysis.application.dtos.link_analysis_dto import DeleteAnalysisInputDTO
from app.modules.link_analysis.domain.exceptions.exceptions import (
    AnalysisNotFoundError,
    InvalidURLError,
)
from app.modules.link_analysis.domain.repositories.link_analysis_repository import (
    LinkAnalysisRepository,
)
from app.modules.link_analysis.domain.value_objects.url_vo import URL


class DeleteAnalysisUseCase:
    def __init__(self, repository: LinkAnalysisRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: DeleteAnalysisInputDTO) -> None:
        try:
            url = URL(value=input_dto.url)
        except ValueError:
            raise InvalidURLError(input_dto.url)

        user_id = input_dto.user_id

        # agora a verificação é por usuário também
        exists = self._repository.exists(url, user_id=user_id)

        if not exists:
            raise AnalysisNotFoundError(input_dto.url)

        self._repository.delete_by_url(url, user_id=user_id)
