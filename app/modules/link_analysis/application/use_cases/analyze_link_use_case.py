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
from app.modules.link_analysis.domain.services.link_analysis_service import (
    LinkAnalysisService,
)
from app.modules.link_analysis.domain.value_objects.url_vo import URL


class AnalyzeLinkUseCase:
    """
    Caso de uso: analisar a segurança de um link.

    Fluxo:
        1. Valida e constrói o Value Object URL.
        2. Executa análise via Domain Service.
        3. Converte score → nível de risco.
        4. Cria entidade.
        5. Persiste no repositório.
        6. Retorna DTO de saída.
    """

    def __init__(
        self,
        repository: LinkAnalysisRepository,
        service: LinkAnalysisService,
    ) -> None:
        self._repository = repository
        self._service = service

    def execute(self, input_dto: AnalyzeLinkInputDTO) -> AnalyzeLinkOutputDTO:
        raw_url = input_dto.url.strip()

        # --- Validação ---
        if len(raw_url) > URLTooLongError.MAX_LENGTH:
            raise URLTooLongError(raw_url)

        try:
            url = URL(value=raw_url)
        except ValueError:
            raise InvalidURLError(raw_url)

        scheme = url.value.split("://")[0]
        if scheme not in UnsupportedSchemeError.SUPPORTED_SCHEMES:
            raise UnsupportedSchemeError(scheme)

        # --- 🔥 Análise via SERVICE ---
        score, reasons = self._service.analyze(str(url))

        # --- Classificação de risco ---
        if score >= 70:
            risk = "HIGH"
        elif score >= 40:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        # --- Criação da entidade ---
        analysis = LinkAnalysisEntity.create(
            url=url,
            risk=risk,
            reasons=reasons,
        )

        # --- Persistência ---
        self._repository.save(analysis)

        # --- Output ---
        return AnalyzeLinkOutputDTO(
            url=str(analysis.url),
            risk=analysis.risk,
            reasons=list(analysis.reasons),
            created_at=analysis.created_at,
        )
