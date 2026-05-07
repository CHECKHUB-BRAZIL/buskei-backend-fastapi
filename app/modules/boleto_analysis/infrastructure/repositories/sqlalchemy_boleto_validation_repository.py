from typing import List, Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.modules.boleto_analysis.domain.entities.boleto_validation_entity import (
    BoletoValidationEntity,
)
from app.modules.boleto_analysis.domain.exceptions.exceptions import (
    BoletoValidationNotFoundError,
    DuplicateBoletoValidationError,
)
from app.modules.boleto_analysis.domain.repositories.boleto_validation_repository import (
    BoletoValidationRepository,
)
from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import BoletoCode
from app.modules.boleto_analysis.infrastructure.mappers.boleto_validation_mapper import (
    BoletoValidationMapper,
)
from app.modules.boleto_analysis.infrastructure.models.boleto_validation_model import (
    BoletoValidationModel,
)


class SQLAlchemyBoletoValidationRepository(BoletoValidationRepository):
    """
    Implementação concreta do repositório usando SQLAlchemy assíncrono.

    Responsabilidades:
    - Traduzir operações de domínio em queries SQL via ORM.
    - Usar o mapper para converter modelos ↔ entidades.
    - Levantar exceções de domínio (nunca vazar exceções de infra).
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Implementações do contrato
    # ------------------------------------------------------------------

    def save(self, validation: BoletoValidationEntity) -> None:
        already_exists = self.exists(validation.code)
        if already_exists:
            raise DuplicateBoletoValidationError(str(validation.code))

        model = BoletoValidationMapper.to_model(validation)
        self._session.add(model)
        self._session.flush()
        self._session.commit()

    def find_by_code(self, code: BoletoCode) -> Optional[BoletoValidationEntity]:
        stmt = (
            select(BoletoValidationModel)
            .where(BoletoValidationModel.code == str(code))
        )
        result = self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return BoletoValidationMapper.to_entity(model)

    def find_all(self) -> List[BoletoValidationEntity]:
        stmt = (
            select(BoletoValidationModel)
            .order_by(BoletoValidationModel.created_at.desc())
        )
        result = self._session.execute(stmt)
        models = result.scalars().all()

        return [BoletoValidationMapper.to_entity(model) for model in models]

    def find_by_status(self, status: str) -> List[BoletoValidationEntity]:
        """
        Busca validações por status específico.
        Operação extra — útil para dashboards e relatórios.
        """
        stmt = (
            select(BoletoValidationModel)
            .where(BoletoValidationModel.status == status)
            .order_by(BoletoValidationModel.created_at.desc())
        )
        result = self._session.execute(stmt)
        models = result.scalars().all()

        return [BoletoValidationMapper.to_entity(model) for model in models]

    def delete_by_code(self, code: BoletoCode) -> None:
        exists = self.exists(code)
        if not exists:
            raise BoletoValidationNotFoundError(str(code))

        stmt = delete(BoletoValidationModel).where(
            BoletoValidationModel.code == str(code)
        )
        self._session.execute(stmt)
        self._session.flush()
        self._session.commit()

    def exists(self, code: BoletoCode) -> bool:
        stmt = select(BoletoValidationModel.code).where(
            BoletoValidationModel.code == str(code)
        )
        result = self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
