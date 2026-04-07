from dataclasses import dataclass

from app.modules.link_analysis.domain.exceptions.exceptions import (
    AnalysisNotFoundError,
    InvalidURLError,
)
from app.modules.link_analysis.domain.repositories.link_analysis_repository import (
    LinkAnalysisRepository,
)
from app.modules.link_analysis.domain.value_objects.url_vo import URL


@dataclass(frozen=True)
class DeleteAnalysisInputDTO:
    url: str


class DeleteAnalysisUseCase:
    """
    Caso de uso: remover a análise de um link pelo seu endereço.

    Fluxo:
        1. Constrói o Value Object URL.
        2. Verifica existência antes de tentar deletar.
        3. Delega a exclusão ao repositório.
    """

    def __init__(self, repository: LinkAnalysisRepository) -> None:
        self._repository = repository

    async def execute(self, input_dto: DeleteAnalysisInputDTO) -> None:
        try:
            url = URL(value=input_dto.url)
        except ValueError:
            raise InvalidURLError(input_dto.url)

        exists = await self._repository.exists(url)
        if not exists:
            raise AnalysisNotFoundError(input_dto.url)

        await self._repository.delete_by_url(url)
