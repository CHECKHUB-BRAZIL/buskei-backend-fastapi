from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import ARRAY

from app.shared.infrastructure.database.base import BaseModel


class BoletoValidationModel(BaseModel):
    """
    Modelo ORM (SQLAlchemy) para persistência da validação de boletos.

    Responsabilidades:
    - Mapear a entidade de domínio para uma tabela relacional.
    - Não carregar nenhuma lógica de negócio.
    - Ser convertido de/para entidade de domínio pelo mapper.

    Colunas:
    - code (PK): código de barras normalizado (44 dígitos)
    - original_code: entrada original do usuário (linha digitável ou código de barras)
    - boleto_type: 'cobranca' | 'convenio'
    - amount: valor em Decimal(12, 2)
    - due_date_factor: fator de vencimento bruto do código (4 dígitos)
    - is_expired: cache calculado na entidade
    - days_overdue: cache calculado na entidade
    - status: 'valid' | 'expired' | 'suspicious'
    - reasons: lista de motivos textuais
    - created_at: timestamp UTC da validação
    """

    __tablename__ = "boleto_validations"

    code = Column(String(44), primary_key=True, nullable=False, index=True)
    original_code = Column(String(48), nullable=False)
    boleto_type = Column(String(10), nullable=False)
    amount = Column(Numeric(precision=12, scale=2), nullable=False)
    due_date_factor = Column(String(4), nullable=True)   # None para convênio
    is_expired = Column(Boolean, nullable=False, default=False)
    days_overdue = Column(Integer, nullable=False, default=0)
    status = Column(String(15), nullable=False, index=True)
    reasons = Column(ARRAY(Text), nullable=False, default=list)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    def __repr__(self) -> str:
        return (
            f"<BoletoValidationModel code={self.code!r} "
            f"status={self.status!r} amount={self.amount}>"
        )
