from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.shared.infrastructure.database.session import init_db
from app.shared.presentation.middlewares.auth_middleware import AuthMiddleware
from app.infra.redis.dependencies import get_session_repository


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")
    init_db()

    # Cria SessionRepository no startup
    session_repo = get_session_repository()

    # Registra middleware
    app.add_middleware(
        AuthMiddleware,
        session_repository=session_repo,
    )

    print("Banco e Redis prontos")

    yield

    print("Encerrando aplicação...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)
