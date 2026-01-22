from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        session_repo = getattr(
            request.app.state,
            "session_repository",
            None,
        )

        # se ainda não estiver pronto (ex: startup)
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
