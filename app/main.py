from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings

from app.infra.redis.redis_client import RedisClient
from app.infra.redis.session_repository import RedisSessionRepository

from app.modules.auth.presentation.http.routes.auth_routes import (
    router as auth_router,
)

from app.modules.link_analysis.presentation.routers.link_analysis_router import (
    router as link_analysis_router,
)

from app.modules.boleto_analysis.presentation.routers.boleto_validation_router import (
    router as boleto_validation_router,
)

from app.modules.boleto_analysis.presentation.exception_handlers import (
    register_boleto_exception_handlers,
)

from app.modules.auth.domain.exceptions.auth_exceptions import (
    AuthException,
)

from app.shared.presentation.exceptions.exception_handlers import (
    auth_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    generic_exception_handler,
)

from app.shared.presentation.middlewares.cors_middleware import (
    setup_cors,
)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Iniciando aplicação...")

    redis = RedisClient.get_client()

    app.state.session_repository = RedisSessionRepository(redis)

    print("Banco e Redis prontos")

    yield

    print("Encerrando aplicação...")


# ---------------------------------------------------------------------------
# FastAPI App
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Middlewares
# ---------------------------------------------------------------------------

setup_cors(app)


# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "service": "buskei-backend",
    }


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    link_analysis_router,
    prefix="/api/v1",
)

app.include_router(
    boleto_validation_router,
    prefix="/api/v1",
)


# ---------------------------------------------------------------------------
# Exception Handlers
# ---------------------------------------------------------------------------

# auth
app.add_exception_handler(
    AuthException,
    auth_exception_handler,
)

# boleto module (antifraude + validation errors)
register_boleto_exception_handlers(app)

# pydantic validation
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

# database
app.add_exception_handler(
    SQLAlchemyError,
    database_exception_handler,
)

# fallback geral
app.add_exception_handler(
    Exception,
    generic_exception_handler,
)
