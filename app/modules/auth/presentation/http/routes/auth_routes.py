from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
import traceback

# ===== Presentation (HTTP Schemas) =====
from app.modules.auth.presentation.http.schemas.current_user_response_schema import CurrentUserResponse
from app.modules.auth.presentation.http.schemas.login_request import LoginRequest
from app.modules.auth.presentation.http.schemas.login_response import LoginResponse
from app.modules.auth.presentation.http.schemas.refresh_token_request import RefreshTokenRequest
from app.modules.auth.presentation.http.schemas.refresh_token_response import RefreshTokenResponse
from app.modules.auth.presentation.http.schemas.register_request import RegisterRequest
from app.modules.auth.presentation.http.schemas.register_response import RegisterResponse

# ===== Application =====
from app.modules.auth.application.usecases import (
    LoginUseCase,
    RegisterUseCase,
)
from app.modules.auth.application.dtos import (
    LoginInputDTO,
    RegisterInputDTO,
)

# ===== Domain =====
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.modules.auth.domain.value_objects.plain_password_vo import PlainPassword

from app.modules.auth.domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
    InactiveUserException,
)

# ===== Infrastructure =====
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler

# ===== Dependencies & Exceptions =====
from app.modules.auth.presentation.http.dependencies.auth_deps import (
    CurrentUser,
    get_jwt_handler,
    get_login_usecase,
    get_register_usecase,
)

from app.shared.presentation.exceptions.http_exceptions import (
    UnauthorizedException,
    ConflictException,
    BadRequestException,
)
from app.core.config import settings
from app.core.constants import TOKEN_TYPE_REFRESH


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginRequest,
    login_uc: Annotated[LoginUseCase, Depends(get_login_usecase)],
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
):
    try:
        input_dto = LoginInputDTO(
            email=Email(data.email),
            password=PlainPassword(data.senha),
        )

        result = await login_uc.execute(input_dto)

        return LoginResponse(
            user_id=str(result.user_id.value),
            access_token=jwt_handler.create_access_token(str(result.user_id.value)),
            refresh_token=jwt_handler.create_refresh_token(str(result.user_id.value)),
            token_type="Bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    except (InvalidCredentialsException, UserNotFoundException):
        raise UnauthorizedException("Credenciais inválidas")
    except InactiveUserException:
        raise UnauthorizedException("Usuário inativo")
    except ValueError as e:
        raise BadRequestException(str(e))

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterRequest,
    register_uc: Annotated[RegisterUseCase, Depends(get_register_usecase)],
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
):
    try:
        input_dto = RegisterInputDTO(
            nome=Name(data.nome),
            email=Email(data.email),
            password=PlainPassword(data.senha),
        )

        user = await register_uc.execute(input_dto)

        return RegisterResponse(
            user=CurrentUserResponse.from_domain(user),
            access_token=jwt_handler.create_access_token(str(user.id.value)),
            refresh_token=jwt_handler.create_refresh_token(str(user.id.value)),
        )

    except UserAlreadyExistsException as e:
        raise ConflictException(str(e))
    except ValueError as e:
        raise BadRequestException(str(e))
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Erro interno")

@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
async def get_me(current_user: CurrentUser):
    return CurrentUserResponse.from_domain(current_user)


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
async def refresh_token(
    data: RefreshTokenRequest,
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
):
    if not jwt_handler.verify_token_type(data.refresh_token, TOKEN_TYPE_REFRESH):
        raise UnauthorizedException("Refresh token inválido")

    user_id = jwt_handler.get_user_id_from_token(data.refresh_token)

    return RefreshTokenResponse(
        access_token=jwt_handler.create_access_token(user_id),
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
