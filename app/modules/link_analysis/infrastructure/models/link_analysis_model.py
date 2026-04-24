from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY

from app.shared.infrastructure.database.base import BaseModel


class LinkAnalysisModel(BaseModel):
    __tablename__ = "link_analyses"

    url = Column(String(2083), nullable=False)
    user_id = Column(String(36), nullable=False, index=True)

    risk = Column(String(10), nullable=False)
    reasons = Column(ARRAY(Text), nullable=False, default=list)

    __table_args__ = (
        UniqueConstraint("url", "user_id", name="uq_user_url"),
    )
