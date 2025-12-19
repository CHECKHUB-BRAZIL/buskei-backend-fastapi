from fastapi import APIRouter, Depends, status, Response
from typing import Annotated

from app.modules.auth.application.dtos import (
    LoginRequestDTO,
    LoginResponseDTO,
    RegisterRequestDTO,
    RegisterResponseDTO,
    UserResponseDTO,
)
from app.modules.auth.application.usecases import (
    LoginUseCase,
    RegisterUseCase,
    LogoutUseCase,
)
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler
from app.modules.auth.domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    UserAlreadyExistsException,
    UserNotFoundException,
    InactiveUserException,
)
from app.modules.auth.presentation.dependencies.auth_deps import (
    get_login_usecase,
    get_register_usecase,
    get_logout_usecase,
    get_jwt_handler,
    CurrentUser,
)
from app.shared.presentation.exceptions.http_exceptions import (
    UnauthorizedException,
    ConflictException,
    BadRequestException,
)
from app.core.config import settings


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login",
    response_model=LoginResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Login de usuário",
    description="Autentica usuário e retorna tokens de acesso",
)
async def login(
    credentials: LoginRequestDTO,
    login_uc: Annotated[LoginUseCase, Depends(get_login_usecase)],
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
):
    """
    ## Login
    
    Autentica usuário com email e senha.
    
    **Retorna:**
    - Dados do usuário
    - Access token (JWT)
    - Refresh token (JWT)
    - Tempo de expiração
    
    **Erros:**
    - 401: Credenciais inválidas
    - 403: Usuário inativo
    """
    
    try:
        # Executa caso de uso
        user = await login_uc.execute(
            email=credentials.email,
            senha=credentials.senha,
        )
        
        # Gera tokens
        access_token = jwt_handler.create_access_token(user.id)
        refresh_token = jwt_handler.create_refresh_token(user.id)
        
        # Monta response
        return LoginResponseDTO(
            user=UserResponseDTO(
                id=user.id,
                nome=user.nome,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at.isoformat() if user.created_at else None,
            ),
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        
    except (InvalidCredentialsException, UserNotFoundException) as e:
        raise UnauthorizedException(str(e))
    except InactiveUserException as e:
        raise UnauthorizedException("Usuário inativo")
    except ValueError as e:
        raise BadRequestException(str(e))


@router.post(
    "/register",
    response_model=RegisterResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Registro de novo usuário",
    description="Cria uma nova conta de usuário",
)
async def register(
    data: RegisterRequestDTO,
    register_uc: Annotated[RegisterUseCase, Depends(get_register_usecase)],
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
):
    """
    ## Registro
    
    Cria uma nova conta de usuário.
    
    **Retorna:**
    - Dados do usuário criado
    - Access token (JWT)
    - Refresh token (JWT)
    - Mensagem de sucesso
    
    **Erros:**
    - 400: Dados inválidos
    - 409: Email já cadastrado
    """
    
    try:
        # Executa caso de uso
        user = await register_uc.execute(
            nome=data.nome,
            email=data.email,
            senha=data.senha,
        )
        
        # Gera tokens
        access_token = jwt_handler.create_access_token(user.id)
        refresh_token = jwt_handler.create_refresh_token(user.id)
        
        # Monta response
        return RegisterResponseDTO(
            user=UserResponseDTO(
                id=user.id,
                nome=user.nome,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at.isoformat() if user.created_at else None,
            ),
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer",
            message="Usuário criado com sucesso",
        )
        
    except UserAlreadyExistsException as e:
        raise ConflictException(str(e))
    except ValueError as e:
        raise BadRequestException(str(e))


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout de usuário",
    description="Encerra sessão do usuário",
)
async def logout(
    current_user: CurrentUser,
    logout_uc: Annotated[LogoutUseCase, Depends(get_logout_usecase)],
):
    """
    ## Logout
    
    Encerra a sessão do usuário autenticado.
    
    **Requer:** Token de autenticação válido
    
    **Nota:** Como usamos JWT stateless, o logout é tratado
    principalmente no cliente (removendo o token).
    
    **Retorna:** Status 204 (No Content)
    """
    
    await logout_uc.execute(current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/me",
    response_model=UserResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="Obter usuário atual",
    description="Retorna dados do usuário autenticado",
)
async def get_me(current_user: CurrentUser):
    """
    ## Usuário Atual
    
    Retorna os dados do usuário autenticado.
    
    **Requer:** Token de autenticação válido
    
    **Retorna:** Dados do usuário
    
    **Erros:**
    - 401: Token inválido ou expirado
    """
    
    return UserResponseDTO(
        id=current_user.id,
        nome=current_user.nome,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat() if current_user.created_at else None,
    )


@router.post(
    "/refresh",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Renovar token de acesso",
    description="Gera novo access token usando refresh token",
)
async def refresh_token(
    refresh_token: str,
    jwt_handler: Annotated[JWTHandler, Depends(get_jwt_handler)],
):
    """
    ## Refresh Token
    
    Gera um novo access token usando o refresh token.
    
    **Body:**
```json
    {
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
```
    
    **Retorna:**
    - Novo access token
    - Tempo de expiração
    
    **Erros:**
    - 401: Refresh token inválido ou expirado
    """
    
    try:
        # Valida refresh token
        from app.core.constants import TOKEN_TYPE_REFRESH
        
        if not jwt_handler.verify_token_type(refresh_token, TOKEN_TYPE_REFRESH):
            raise UnauthorizedException("Refresh token inválido")
        
        # Extrai user_id
        user_id = jwt_handler.get_user_id_from_token(refresh_token)
        
        # Gera novo access token
        new_access_token = jwt_handler.create_access_token(user_id)
        
        return {
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        }
        
    except Exception as e:
        raise UnauthorizedException("Não foi possível renovar o token")
