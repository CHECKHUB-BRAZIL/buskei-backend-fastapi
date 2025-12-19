from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidTokenException


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware de autenticação global.
    
    Pode ser usado para:
    - Validar tokens em rotas protegidas
    - Adicionar informações do usuário ao request
    - Logging de acessos
    
    Nota: Este middleware é opcional. Preferimos usar
    dependencies do FastAPI (get_current_user) que são
    mais flexíveis e testáveis.
    """
    
    def __init__(self, app, exclude_paths: list[str] = None):
        super().__init__(app)
        self.jwt_handler = JWTHandler()
        self.exclude_paths = exclude_paths or [
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
        ]
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Processa cada requisição.
        """
        
        # Ignora rotas excluídas
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        # Extrai token do header
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token de autenticação não fornecido"},
            )
        
        token = auth_header.split()[1]
        
        try:
            # Valida token
            payload = self.jwt_handler.decode_token(token)
            
            # Adiciona user_id ao state do request
            request.state.user_id = payload.get("sub")
            
        except InvalidTokenException:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token inválido ou expirado"},
            )
        
        return await call_next(request)
