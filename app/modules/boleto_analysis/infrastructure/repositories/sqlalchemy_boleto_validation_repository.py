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

from app.modules.boleto_analysis.domain.value_objects.boleto_code_vo import (
    BoletoCode,
)

from app.modules.boleto_analysis.infrastructure.mappers.boleto_validation_mapper import (
    BoletoValidationMapper,
)

from app.modules.boleto_analysis.infrastructure.models.boleto_validation_model import (
    BoletoValidationModel,
)


class SQLAlchemyBoletoValidationRepository(
    BoletoValidationRepository
):
    """
    Implementação concreta do repositório usando SQLAlchemy.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(
        self,
        validation: BoletoValidationEntity,
    ) -> None:

        already_exists = self.exists(
            validation.code,
            validation.user_id,
        )

        if already_exists:
            raise DuplicateBoletoValidationError(
                str(validation.code)
            )

        model = BoletoValidationMapper.to_model(validation)

        self._session.add(model)
        self._session.flush()
        self._session.commit()

    # ------------------------------------------------------------------
    # Find by code
    # ------------------------------------------------------------------

    def find_by_code(
        self,
        code: BoletoCode,
        user_id: str,
    ) -> Optional[BoletoValidationEntity]:

        stmt = (
            select(BoletoValidationModel)
            .where(BoletoValidationModel.code == str(code))
            .where(BoletoValidationModel.user_id == user_id)
        )

        result = self._session.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return BoletoValidationMapper.to_entity(model)

    # ------------------------------------------------------------------
    # Find all
    # ------------------------------------------------------------------

    def find_all(
        self,
        user_id: str,
    ) -> List[BoletoValidationEntity]:

        stmt = (
            select(BoletoValidationModel)
            .where(BoletoValidationModel.user_id == user_id)
            .order_by(BoletoValidationModel.created_at.desc())
        )

        result = self._session.execute(stmt)

        models = result.scalars().all()

        return [
            BoletoValidationMapper.to_entity(model)
            for model in models
        ]

    # ------------------------------------------------------------------
    # Find by status
    # ------------------------------------------------------------------

    def find_by_status(
        self,
        status: str,
        user_id: str,
    ) -> List[BoletoValidationEntity]:

        stmt = (
            select(BoletoValidationModel)
            .where(BoletoValidationModel.status == status)
            .where(BoletoValidationModel.user_id == user_id)
            .order_by(BoletoValidationModel.created_at.desc())
        )

        result = self._session.execute(stmt)

        models = result.scalars().all()

        return [
            BoletoValidationMapper.to_entity(model)
            for model in models
        ]

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    def delete_by_code(
        self,
        code: BoletoCode,
        user_id: str,
    ) -> None:

        exists = self.exists(code, user_id)

        if not exists:
            raise BoletoValidationNotFoundError(str(code))

        stmt = (
            delete(BoletoValidationModel)
            .where(BoletoValidationModel.code == str(code))
            .where(BoletoValidationModel.user_id == user_id)
        )

        self._session.execute(stmt)

        self._session.flush()
        self._session.commit()

    # ------------------------------------------------------------------
    # Exists
    # ------------------------------------------------------------------

    def exists(
        self,
        code: BoletoCode,
        user_id: str,
    ) -> bool:

        stmt = (
            select(BoletoValidationModel.code)
            .where(BoletoValidationModel.code == str(code))
            .where(BoletoValidationModel.user_id == user_id)
        )

        result = self._session.execute(stmt)

        return result.scalar_one_or_none() is not None
