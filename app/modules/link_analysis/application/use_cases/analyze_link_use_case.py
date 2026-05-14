from app.modules.link_analysis.application.dtos.link_analysis_dto import (
    AnalyzeLinkInputDTO,
    AnalyzeLinkOutputDTO,
)

from app.modules.link_analysis.domain.exceptions.exceptions import (
    InvalidURLError,
    URLTooLongError,
    UnsupportedSchemeError,
)

from app.modules.link_analysis.domain.services.link_analysis_service import (
    LinkAnalysisService,
)

from app.modules.link_analysis.domain.value_objects.url_vo import (
    URLVO,
)


class AnalyzeLinkUseCase:
    """
    Caso de uso responsável por:
    - validar URL
    - executar análise heurística antifraude
    - retornar DTO para apresentação
    """

    def __init__(
        self,
        service: LinkAnalysisService,
    ) -> None:
        self._service = service

    def execute(
        self,
        input_dto: AnalyzeLinkInputDTO,
    ) -> AnalyzeLinkOutputDTO:

        raw_url = input_dto.url.strip()

        # ======================================================
        # TAMANHO
        # ======================================================

        if len(raw_url) > URLTooLongError.MAX_LENGTH:
            raise URLTooLongError(raw_url)

        # ======================================================
        # URL VO
        # ======================================================

        try:
            url = URLVO(value=raw_url)

        except ValueError:
            raise InvalidURLError(raw_url)

        # ======================================================
        # SCHEME
        # ======================================================

        scheme = url.value.split("://")[0]

        if scheme not in UnsupportedSchemeError.SUPPORTED_SCHEMES:
            raise UnsupportedSchemeError(scheme)

        # ======================================================
        # ANÁLISE
        # ======================================================

        risk_score, reasons, positives = self._service.analyze(url)

        # ======================================================
        # CLASSIFICAÇÃO
        # ======================================================

        if risk_score >= 70:
            risk = "HIGH"

        elif risk_score >= 40:
            risk = "MEDIUM"

        else:
            risk = "LOW"

        # ======================================================
        # OUTPUT
        # ======================================================

        return AnalyzeLinkOutputDTO(
            url=str(url),
            risk=risk,
            risk_score=risk_score,
            reasons=reasons,
            positives=positives,
        )
