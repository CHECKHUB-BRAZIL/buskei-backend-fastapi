from app.modules.link_analysis.domain.entities.link_entity import LinkAnalysisEntity
from app.modules.link_analysis.domain.value_objects.url_vo import URL
from app.modules.link_analysis.infrastructure.models.link_analysis_model import (
    LinkAnalysisModel,
)


class LinkAnalysisMapper:

    @staticmethod
    def to_model(entity: LinkAnalysisEntity, user_id: str) -> LinkAnalysisModel:
        return LinkAnalysisModel(
            url=str(entity.url),
            user_id=user_id,
            risk=entity.risk,
            reasons=list(entity.reasons),
            created_at=entity.created_at,
        )

    @staticmethod
    def to_entity(model: LinkAnalysisModel) -> LinkAnalysisEntity:
        return LinkAnalysisEntity(
            url=URL(value=model.url),
            risk=model.risk,
            reasons=list(model.reasons),
            created_at=model.created_at,
        )
