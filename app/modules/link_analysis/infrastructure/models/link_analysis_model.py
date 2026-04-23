from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import ARRAY

from app.shared.infrastructure.database.base import Base


class LinkAnalysisModel(Base):
    """
    Modelo ORM (SQLAlchemy) para persistência da análise de links.

    Responsabilidades:
    - Mapear a entidade de domínio para uma tabela relacional.
    - Não carregar nenhuma lógica de negócio.
    - Ser convertido de/para entidade de domínio pelo repositório.
    """

    __tablename__ = "link_analyses"

    url = Column(String(2083), primary_key=True, nullable=False, index=True)
    user_id = Column(String(36), primary_key=True, nullable=False, index=True)

    risk = Column(String(10), nullable=False)
    reasons = Column(ARRAY(Text), nullable=False, default=list)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return f"<LinkAnalysisModel url={self.url!r} risk={self.risk!r}>"
