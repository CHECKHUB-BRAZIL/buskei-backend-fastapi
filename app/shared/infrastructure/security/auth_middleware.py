from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared.domain.repositories.session_repository import SessionRepository


class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, session_repository: SessionRepository):
        super().__init__(app)
        self._session_repo = session_repository

    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)

        token = auth_header.split(" ")[1]

        # Verifica se access token está revogado
        if self._session_repo.is_access_token_blacklisted(token):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token revogado"},
            )

        return await call_next(request)
