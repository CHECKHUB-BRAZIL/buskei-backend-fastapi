from typing import List

from app.modules.link_analysis.application.dtos.link_analysis_dto import AnalyzeLinkOutputDTO
from app.modules.link_analysis.domain.repositories.link_analysis_repository import (
    LinkAnalysisRepository,
)


class ListAnalysesUseCase:
    """
    Caso de uso: listar todas as análises já realizadas.

    Fluxo:
        1. Busca todas as entidades no repositório.
        2. Converte para DTOs de saída.
        3. Retorna lista (pode ser vazia).
    """

    def __init__(self, repository: LinkAnalysisRepository) -> None:
        self._repository = repository

    async def execute(self) -> List[AnalyzeLinkOutputDTO]:
        analyses = await self._repository.find_all()

        return [
            AnalyzeLinkOutputDTO(
                url=str(analysis.url),
                risk=analysis.risk,
                reasons=list(analysis.reasons),
                created_at=analysis.created_at,
            )
            for analysis in analyses
        ]
