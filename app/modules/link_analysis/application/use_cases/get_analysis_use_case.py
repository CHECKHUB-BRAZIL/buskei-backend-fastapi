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
    """
    Caso de uso: recuperar a análise mais recente de um link já analisado.

    Fluxo:
        1. Constrói o Value Object URL a partir da string recebida.
        2. Consulta o repositório.
        3. Levanta AnalysisNotFoundError se não houver resultado.
        4. Retorna DTO de saída.
    """

    def __init__(self, repository: LinkAnalysisRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: GetAnalysisInputDTO) -> GetAnalysisOutputDTO:
        try:
            url = URL(value=input_dto.url)
        except ValueError:
            raise InvalidURLError(input_dto.url)

        analysis = self._repository.find_by_url(url)

        if analysis is None:
            raise AnalysisNotFoundError(input_dto.url)

        return GetAnalysisOutputDTO(
            url=str(analysis.url),
            risk=analysis.risk,
            reasons=list(analysis.reasons),
            created_at=analysis.created_at,
        )
