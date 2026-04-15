from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.link_analysis.domain.entities.link_entity import LinkAnalysisEntity
from app.modules.link_analysis.domain.exceptions.exceptions import (
    AnalysisNotFoundError,
    DuplicateAnalysisError,
)
from app.modules.link_analysis.domain.repositories.link_analysis_repository import (
    LinkAnalysisRepository,
)
from app.modules.link_analysis.domain.value_objects.url_vo import URL
from app.modules.link_analysis.infrastructure.mappers.link_analysis_mapper import (
    LinkAnalysisMapper,
)
from app.modules.link_analysis.infrastructure.models.link_analysis_model import (
    LinkAnalysisModel,
)


class SQLAlchemyLinkAnalysisRepository(LinkAnalysisRepository):
    """
    Implementação concreta do repositório usando SQLAlchemy assíncrono.

    Responsabilidades:
    - Traduzir operações de domínio em queries SQL via ORM.
    - Usar o mapper para converter modelos ↔ entidades.
    - Levantar exceções de domínio (nunca exceções de infra para cima).
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Implementações do contrato
    # ------------------------------------------------------------------

    def save(self, analysis: LinkAnalysisEntity) -> None:
        already_exists = self.exists(analysis.url)
        if already_exists:
            raise DuplicateAnalysisError(str(analysis.url))

        model = LinkAnalysisMapper.to_model(analysis)
        self._session.add(model)
        self._session.flush()  # garante o INSERT sem fechar a transação

    def find_by_url(self, url: URL) -> Optional[LinkAnalysisEntity]:
        stmt = select(LinkAnalysisModel).where(LinkAnalysisModel.url == str(url))
        result = self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return LinkAnalysisMapper.to_entity(model)

    def find_all(self) -> List[LinkAnalysisEntity]:
        stmt = select(LinkAnalysisModel).order_by(LinkAnalysisModel.created_at.desc())
        result = self._session.execute(stmt)
        models = result.scalars().all()

        return [LinkAnalysisMapper.to_entity(model) for model in models]

    def delete_by_url(self, url: URL) -> None:
        exists = self.exists(url)
        if not exists:
            raise AnalysisNotFoundError(str(url))

        stmt = delete(LinkAnalysisModel).where(LinkAnalysisModel.url == str(url))
        self._session.execute(stmt)
        self._session.flush()

    def exists(self, url: URL) -> bool:
        stmt = select(LinkAnalysisModel.url).where(LinkAnalysisModel.url == str(url))
        result = self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
