from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.shared.presentation.exempt_paths import EXEMPT_PATHS


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # ignora rotas específicas
        if request.url.path in EXEMPT_PATHS:
            return await call_next(request)

        session_repo = getattr(request.app.state, "session_repository", None)
        if session_repo is None:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(request)

        token = auth_header.split(" ")[1]

        if session_repo.is_access_token_blacklisted(token):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token revogado"},
            )

        return await call_next(request)
