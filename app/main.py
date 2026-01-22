from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.shared.infrastructure.database.session import init_db
from app.shared.presentation.middlewares.auth_middleware import AuthMiddleware
from app.infra.redis.redis_client import RedisClient
from app.infra.redis.session_repository import RedisSessionRepository
from app.modules.auth.presentation.http.routes.auth_routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")

    init_db()
    redis = RedisClient.get_client()
    app.state.session_repository = RedisSessionRepository(redis)

    print("Banco e Redis prontos")
    yield
    print("Encerrando aplicação...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

# middleware
app.add_middleware(AuthMiddleware)

# REGISTRA AS ROTAS
app.include_router(auth_router, prefix="/api/v1")
