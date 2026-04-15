from app.modules.link_analysis.application.dtos.link_analysis_dto import (
    AnalyzeLinkInputDTO,
    AnalyzeLinkOutputDTO,
)
from app.modules.link_analysis.domain.entities.link_entity import LinkAnalysisEntity
from app.modules.link_analysis.domain.exceptions.exceptions import (
    InvalidURLError,
    URLTooLongError,
    UnsupportedSchemeError,
)
from app.modules.link_analysis.domain.repositories.link_analysis_repository import (
    LinkAnalysisRepository,
)
from app.modules.link_analysis.domain.value_objects.url_vo import URL


class AnalyzeLinkUseCase:
    """
    Caso de uso: analisar a segurança de um link.

    Fluxo:
        1. Valida e constrói o Value Object URL.
        2. Delega a análise de domínio para a entidade.
        3. Persiste o resultado via repositório.
        4. Retorna DTO de saída para a apresentação.

    Não conhece detalhes de HTTP, banco de dados ou framework.
    """

    def __init__(self, repository: LinkAnalysisRepository) -> None:
        self._repository = repository

    def execute(self, input_dto: AnalyzeLinkInputDTO) -> AnalyzeLinkOutputDTO:
        raw_url = input_dto.url.strip()

        # --- Guarda de domínio: tamanho máximo ---
        if len(raw_url) > URLTooLongError.MAX_LENGTH:
            raise URLTooLongError(raw_url)

        # --- Constrói o Value Object (valida formato básico) ---
        try:
            url = URL(value=raw_url)
        except ValueError:
            raise InvalidURLError(raw_url)

        # --- Guarda de domínio: scheme suportado ---
        scheme = url.value.split("://")[0]
        if scheme not in UnsupportedSchemeError.SUPPORTED_SCHEMES:
            raise UnsupportedSchemeError(scheme)

        # --- Análise de domínio ---
        analysis: LinkAnalysisEntity = LinkAnalysisEntity.analyze(url)

        # --- Persistência ---
        self._repository.save(analysis)

        return AnalyzeLinkOutputDTO(
            url=str(analysis.url),
            risk=analysis.risk,
            reasons=list(analysis.reasons),
            created_at=analysis.created_at,
        )
