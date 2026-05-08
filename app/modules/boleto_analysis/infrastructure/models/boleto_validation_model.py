from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
)

from sqlalchemy.dialects.postgresql import ARRAY

from app.shared.infrastructure.database.base import BaseModel


class BoletoValidationModel(BaseModel):
    """
    Modelo ORM (SQLAlchemy) para persistência da validação de boletos.
    """

    __tablename__ = "boleto_validations"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id = Column(
        String,
        nullable=False,
        index=True,
    )

    code = Column(
        String(44),
        nullable=False,
        index=True,
    )

    original_code = Column(
        String(48),
        nullable=False,
    )

    boleto_type = Column(
        String(10),
        nullable=False,
    )

    amount = Column(
        Numeric(precision=12, scale=2),
        nullable=False,
    )

    due_date_factor = Column(
        String(4),
        nullable=True,
    )

    is_expired = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    days_overdue = Column(
        Integer,
        nullable=False,
        default=0,
    )

    status = Column(
        String(15),
        nullable=False,
        index=True,
    )

    reasons = Column(
        ARRAY(Text),
        nullable=False,
        default=list,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return (
            f"<BoletoValidationModel "
            f"id={self.id!r} "
            f"user_id={self.user_id!r} "
            f"code={self.code!r} "
            f"status={self.status!r} "
            f"amount={self.amount}>"
        )
