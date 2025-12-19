from typing import Annotated
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.shared.infrastructure.database.session import get_db
from app.modules.auth.domain.entities.user_entity import UserEntity
from app.modules.auth.domain.repositories.user_repository import UserRepository
from app.modules.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher
from app.modules.auth.application.usecases.login_usecase import LoginUseCase
from app.modules.auth.application.usecases.register_usecase import RegisterUseCase
from app.modules.auth.application.usecases.get_current_user_usecase import GetCurrentUserUseCase
from app.modules.auth.application.usecases.logout_usecase import LogoutUseCase
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException
from app.core.constants import TOKEN_TYPE_ACCESS


# ============================================================
# Dependencies de Infraestrutura
# ============================================================

def get_password_hasher() -> PasswordHasher:
    """Dependency para obter PasswordHasher."""
    return PasswordHasher()


def get_jwt_handler() -> JWTHandler:
    """Dependency para obter JWTHandler."""
    return JWTHandler()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Dependency para obter UserRepository."""
    return UserRepositoryImpl(db)


# ============================================================
# Dependencies de UseCases
# ============================================================

def get_login_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> LoginUseCase:
    """Dependency para obter LoginUseCase."""
    return LoginUseCase(user_repository, password_hasher)


def get_register_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterUseCase:
    """Dependency para obter RegisterUseCase."""
    return RegisterUseCase(user_repository, password_hasher)


def get_current_user_usecase(
    user_repository: UserRepository = Depends(get_user_repository),
) -> GetCurrentUserUseCase:
    """Dependency para obter GetCurrentUserUseCase."""
    return GetCurrentUserUseCase(user_repository)


def get_logout_usecase() -> LogoutUseCase:
    """Dependency para obter LogoutUseCase."""
    return LogoutUseCase()


# ============================================================
# Dependencies de Autenticação
# ============================================================

async def get_token_from_header(
    authorization: Annotated[str | None, Header()] = None
) -> str:
    """
    Extrai token do header Authorization.
    
    Espera formato: "Bearer <token>"
    
    Raises:
        HTTPException: Se token não estiver presente ou formato inválido
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação não fornecido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    parts = authorization.split()
    
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de token inválido. Use: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return parts[1]


async def get_current_user(
    token: str = Depends(get_token_from_header),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    get_user_uc: GetCurrentUserUseCase = Depends(get_current_user_usecase),
) -> UserEntity:
    """
    Dependency para obter usuário autenticado atual.
    
    Valida token JWT e retorna entidade do usuário.
    
    Raises:
        HTTPException: Se token inválido ou usuário não encontrado
    """
    
    try:
        # Verifica se é token de acesso
        if not jwt_handler.verify_token_type(token, TOKEN_TYPE_ACCESS):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de acesso inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Extrai user_id do token
        user_id = jwt_handler.get_user_id_from_token(token)
        
        # Busca usuário
        user = await get_user_uc.execute(user_id)
        
        # Verifica se usuário está ativo
        if not user.can_login():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )
        
        return user
        
    except InvalidTokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Type aliases para facilitar uso
CurrentUser = Annotated[UserEntity, Depends(get_current_user)]
