from app.modules.link_analysis.domain.entities.link_entity import LinkAnalysisEntity
from app.modules.link_analysis.domain.value_objects.url_vo import URL
from app.modules.link_analysis.infrastructure.models.link_analysis_model import (
    LinkAnalysisModel,
)


class LinkAnalysisMapper:
    """
    Converte entre a entidade de domínio (LinkAnalysisEntity)
    e o modelo ORM (LinkAnalysisModel).

    Mantém domínio e infraestrutura completamente desacoplados:
    - O domínio nunca importa o modelo ORM.
    - O ORM nunca conhece as regras de negócio.
    """

    @staticmethod
    def to_model(entity: LinkAnalysisEntity) -> LinkAnalysisModel:
        """Entidade de domínio → modelo ORM."""
        return LinkAnalysisModel(
            url=str(entity.url),
            risk=entity.risk,
            reasons=list(entity.reasons),
            created_at=entity.created_at,
        )

    @staticmethod
    def to_entity(model: LinkAnalysisModel) -> LinkAnalysisEntity:
        """Modelo ORM → entidade de domínio."""
        return LinkAnalysisEntity(
            url=URL(value=model.url),
            risk=model.risk,
            reasons=list(model.reasons),
            created_at=model.created_at,
        )
