from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserNotFoundException,
)
from app.modules.auth.domain.read_models.user_credentials import (
    UserCredentials,
)
from app.modules.auth.domain.repositories.user_repository import (
    UserRepository,
)
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.password_vo import Password
from app.shared.domain.value_objects.id_vo import Id
from app.modules.auth.infrastructure.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self._db = db

    async def create(self, user: UserEntity) -> UserEntity:
        model = UserModel.from_entity(user)

        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)

        return model.to_entity()

    async def get_by_id(
        self,
        user_id: Id,
    ) -> Optional[UserEntity]:
        model = self._get_model_by_id(user_id)

        return model.to_entity() if model else None

    async def get_by_email(
        self,
        email: Email,
    ) -> Optional[UserEntity]:
        stmt = select(UserModel).where(
            UserModel.email == email.value
        )

        model = self._db.execute(
            stmt
        ).scalar_one_or_none()

        return model.to_entity() if model else None

    async def exists_by_email(
        self,
        email: Email,
    ) -> bool:
        stmt = select(UserModel.id).where(
            UserModel.email == email.value
        )

        return (
            self._db.execute(stmt).scalar_one_or_none()
            is not None
        )

    async def get_credentials_by_email(
        self,
        email: Email,
    ) -> Optional[UserCredentials]:
        stmt = select(
            UserModel.id,
            UserModel.password,
            UserModel.is_active,
        ).where(
            UserModel.email == email.value
        )

        row = self._db.execute(stmt).first()

        if row is None:
            return None

        return UserCredentials(
            user_id=Id(row.id),
            password_hash=row.password,
            is_active=row.is_active,
        )

    async def update(
        self,
        user: UserEntity,
    ) -> UserEntity:
        user_model = self._get_model_by_id(user.id)

        if user_model is None:
            raise UserNotFoundException(
                str(user.id.value)
            )

        user_model.nome = user.nome.value
        user_model.email = user.email.value
        user_model.is_active = user.is_active

        self._db.commit()
        self._db.refresh(user_model)

        return user_model.to_entity()

    async def delete(
        self,
        user_id: Id,
    ) -> bool:
        user_model = self._get_model_by_id(user_id)

        if user_model is None:
            return False

        self._db.delete(user_model)
        self._db.commit()

        return True

    async def update_password(
        self,
        user_id: Id,
        password: Password,
    ) -> None:
        user_model = self._get_model_by_id(user_id)

        if user_model is None:
            raise UserNotFoundException(
                str(user_id.value)
            )

        user_model.password = password.value

        self._db.commit()

    def _get_model_by_id(
        self,
        user_id: Id,
    ) -> Optional[UserModel]:
        stmt = select(UserModel).where(
            UserModel.id == user_id.value
        )

        return self._db.execute(
            stmt
        ).scalar_one_or_none()
