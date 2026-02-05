from uuid import uuid4
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import traceback

from app.modules.auth.application.usecases.google_login_usecase import GoogleLoginUseCase
from app.modules.auth.application.usecases.reset_password_usecase import ResetPasswordUseCase
from app.modules.auth.presentation.http.schemas.google_login_request import GoogleLoginRequest
from app.modules.auth.presentation.http.schemas.reset_password_request import ResetPasswordRequest
from redis import Redis

# ===== Presentation (HTTP Schemas) =====
from app.modules.auth.presentation.http.schemas.current_user_response_schema import CurrentUserResponse
from app.modules.auth.presentation.http.schemas.forgot_password_request import ForgotPasswordRequest
from app.modules.auth.presentation.http.schemas.login_request import LoginRequest
from app.modules.auth.presentation.http.schemas.login_response import LoginResponse
from app.modules.auth.presentation.http.schemas.logout_request import LogoutRequest
from app.modules.auth.presentation.http.schemas.refresh_token_request import RefreshTokenRequest
from app.modules.auth.presentation.http.schemas.refresh_token_response import RefreshTokenResponse
from app.modules.auth.presentation.http.schemas.register_request import RegisterRequest
from app.modules.auth.presentation.http.schemas.register_response import RegisterResponse

# ===== Application =====
from app.modules.auth.application.usecases import (
    LoginUseCase,
    RegisterUseCase,
)

from app.modules.auth.application.usecases.forgot_password_usecase import (
    ForgotPasswordUseCase,
)

from app.modules.auth.application.dtos import (
    LoginInputDTO,
    RegisterInputDTO,
)

# ===== Domain =====
from app.modules.auth.domain.value_objects.email_vo import Email
from app.modules.auth.domain.value_objects.name_vo import Name
from app.modules.auth.domain.value_objects.plain_password_vo import PlainPassword

from app.modules.auth.domain.exceptions.auth_exceptions import UserAlreadyExistsException

# ===== Infrastructure =====
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler

# ===== Dependencies & Exceptions =====
from app.modules.auth.presentation.http.dependencies.auth_deps import (
    CurrentUser,
    get_forgot_password_usecase,
    get_google_login_usecase,
    get_jwt_handler,
    get_login_usecase,
    get_register_usecase,
    get_reset_password_usecase,
)

from app.shared.presentation.exceptions.http_exceptions import (
    UnauthorizedException,
    ConflictException,
    BadRequestException,
)
from app.core.config import settings
from app.core.constants import TOKEN_TYPE_ACCESS, TOKEN_TYPE_REFRESH

from app.infra.redis.dependencies import get_redis


router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer()

@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    credentials: LoginRequest,
    login_uc: Annotated[LoginUseCase, Depends(get_login_usecase)],
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    input_dto = LoginInputDTO(
        email=Email(credentials.email),
        password=PlainPassword(credentials.senha),
    )

    result = await login_uc.execute(input_dto)

    user_id = str(result.user_id.value)

    access_token = jwt_handler.create_access_token(user_id)
    refresh_token = jwt_handler.create_refresh_token(user_id)

    # decodifica refresh para pegar o jti
    refresh_payload = jwt_handler.decode_token(
        refresh_token,
        expected_type=TOKEN_TYPE_REFRESH,
    )

    jti = refresh_payload["jti"]

    # salva refresh
    redis.setex(
        name=f"refresh:{jti}",
        time=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        value=user_id,
    )

    # registra sessão do usuário
    redis.sadd(f"user_sessions:{user_id}", refresh_payload["jti"])

    user_response = CurrentUserResponse(
        id=user_id,
        nome=result.nome.value,
        email=result.email.value,
        is_active=result.is_active,
        created_at=None,
    )

    return LoginResponse(
        user=user_response,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    data: RegisterRequest,
    register_uc: Annotated[RegisterUseCase, Depends(get_register_usecase)],
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    try:
        input_dto = RegisterInputDTO(
            nome=Name(data.nome),
            email=Email(data.email),
            password=PlainPassword(data.senha),
        )

        user = await register_uc.execute(input_dto)
        user_id = str(user.id.value)

        access_token = jwt_handler.create_access_token(user_id)
        refresh_token = jwt_handler.create_refresh_token(user_id)

        refresh_payload = jwt_handler.decode_token(
            refresh_token,
            expected_type=TOKEN_TYPE_REFRESH,
        )

        jti = refresh_payload["jti"]

        # 1 salva refresh token
        redis.setex(
            name=f"refresh:{jti}",
            time=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
            value=user_id,
        )

        # 2 registra sessão
        redis.sadd(f"user_sessions:{user_id}", jti)

        return RegisterResponse(
            user=CurrentUserResponse.from_domain(user),
            access_token=access_token,
            refresh_token=refresh_token,
        )

    except UserAlreadyExistsException as e:
        raise ConflictException(str(e))
    except ValueError as e:
        raise BadRequestException(str(e))
    except Exception:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Erro interno")



@router.get(
    "/me",
    response_model=CurrentUserResponse,
    dependencies=[Depends(bearer_scheme)],
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
    redis: Annotated[Redis, Depends(get_redis)],
):
    payload = jwt_handler.decode_token(
        data.refresh_token,
        expected_type=TOKEN_TYPE_REFRESH,
    )

    jti = payload["jti"]
    user_id = payload["sub"]

    redis_key = f"refresh:{jti}"

    # 1. Verifica se refresh ainda é válido
    if not redis.exists(redis_key):
        raise UnauthorizedException("Refresh token revogado ou inválido")

    # 2. Revoga refresh antigo
    redis.delete(redis_key)
    redis.srem(f"user_sessions:{user_id}", jti)

    # 3. Gera novos tokens
    new_access_token = jwt_handler.create_access_token(user_id)
    new_refresh_token = jwt_handler.create_refresh_token(user_id)

    new_payload = jwt_handler.decode_token(
        new_refresh_token,
        expected_type=TOKEN_TYPE_REFRESH,
    )

    new_jti = new_payload["jti"]

    # 4. Salva novo refresh
    redis.setex(
        name=f"refresh:{new_jti}",
        time=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        value=user_id,
    )

    redis.sadd(f"user_sessions:{user_id}", new_jti)

    return RefreshTokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="Bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    data: LogoutRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    redis: Redis = Depends(get_redis),
):
    access_token = credentials.credentials

    # 1 Decodifica access token
    access_payload = jwt_handler.decode_token(
        access_token,
        expected_type=TOKEN_TYPE_ACCESS,
    )

    user_id = access_payload["sub"]

    # 2 Blacklist do access token
    expires_at = jwt_handler.get_token_expiration(access_token)
    ttl = int((expires_at - jwt_handler._now()).total_seconds())

    if ttl > 0:
        redis.setex(
            name=f"blacklist:{access_token}",
            time=ttl,
            value="true",
        )

    # 3 Decodifica refresh token
    refresh_payload = jwt_handler.decode_token(
        data.refresh_token,
        expected_type=TOKEN_TYPE_REFRESH,
    )

    # 4 Garante que ambos pertencem ao mesmo usuário
    if refresh_payload["sub"] != user_id:
        raise UnauthorizedException("Refresh token não pertence ao usuário")

    # 5 Revoga refresh token
    redis.delete(f"refresh:{refresh_payload['jti']}")
    redis.srem(f"user_sessions:{user_id}", refresh_payload["jti"])

    return


@router.post(
    "/logout-all",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_all(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    jwt_handler: JWTHandler = Depends(get_jwt_handler),
    redis: Redis = Depends(get_redis),
):
    # Ainda implementar token_version no User e checar aqui para invalidar tokens antigos
    access_token = credentials.credentials

    payload = jwt_handler.decode_token(
        access_token,
        expected_type=TOKEN_TYPE_ACCESS,
    )

    user_id = payload["sub"]

    # Busca todos os refresh tokens do usuário
    jtis = redis.smembers(f"user_sessions:{user_id}")

    for jti in jtis:
        redis.delete(f"refresh:{jti}")

    redis.delete(f"user_sessions:{user_id}")

    # blacklist do access token atual
    expires_at = jwt_handler.get_token_expiration(access_token)
    ttl = int((expires_at - jwt_handler._now()).total_seconds())

    if ttl > 0:
        redis.setex(f"blacklist:{access_token}", ttl, "true")

    return


@router.post("/forgot-password")
async def forgot_password(
    data: ForgotPasswordRequest,
    forgot_password_uc: ForgotPasswordUseCase = Depends(get_forgot_password_usecase),
):
    email = Email(data.email)
    await forgot_password_uc.execute(email)
    return {"message": "Se o email existir, enviaremos instruções."}


@router.post("/reset-password")
async def reset_password(
    data: ResetPasswordRequest,
    reset_password_uc: ResetPasswordUseCase = Depends(get_reset_password_usecase),
):
    
    plain_password = PlainPassword(data.new_password)
    await reset_password_uc.execute(
        token=data.token,
        new_password=plain_password,
    )
    return {"message": "Senha alterada com sucesso"}

@router.post(
    "/google-login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def google_login(
    body: GoogleLoginRequest,
    usecase: GoogleLoginUseCase = Depends(get_google_login_usecase),
):
    """
    Realiza login ou cadastro usando conta Google.
    """
    return await usecase.execute(body.id_token)
