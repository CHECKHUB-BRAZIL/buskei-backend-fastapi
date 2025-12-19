from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.shared.infrastructure.database.session import init_db
from app.shared.presentation.middlewares.cors_middleware import setup_cors
from app.shared.presentation.middlewares.error_handler import (
    auth_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    generic_exception_handler,
)
from app.modules.auth.domain.exceptions.auth_exceptions import AuthException
from app.modules.auth.presentation.routes import auth_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    
    Startup:
    - Inicializa banco de dados
    - Configura conexões
    
    Shutdown:
    - Fecha conexões
    - Cleanup de recursos
    """
    # Startup
    print("🚀 Iniciando aplicação...")
    init_db()
    print("✅ Banco de dados inicializado")
    
    yield
    
    # Shutdown
    print("👋 Encerrando aplicação...")


# Cria aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    ## Busquei API
    
    API RESTful construída com Clean Architecture e Domain-Driven Design.
    
    ### Módulos
    - **Auth**: Autenticação e autorização de usuários
    - **Products**: Gerenciamento de produtos (em breve)
    - **Orders**: Gerenciamento de pedidos (em breve)
    
    ### Autenticação
    Utilize JWT tokens obtidos através do endpoint `/auth/login`.
    
    Inclua o token no header: `Authorization: Bearer <token>`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ============================================================
# Configuração de Middlewares
# ============================================================

# CORS
setup_cors(app)


# ============================================================
# Configuração de Exception Handlers
# ============================================================

app.add_exception_handler(AuthException, auth_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# ============================================================
# Rotas
# ============================================================

# Health Check
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Verifica se a API está funcionando.
    
    Útil para:
    - Monitoramento
    - Load balancers
    - CI/CD
    """
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "project": settings.PROJECT_NAME,
    }


# Rotas de módulos
app.include_router(auth_routes.router, prefix="/api/v1")


# ============================================================
# Rota raiz
# ============================================================

@app.get("/", tags=["Root"])
async def root():
    """Rota raiz da API."""
    return {
        "message": f"Bem-vindo ao {settings.PROJECT_NAME}!",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": "/health",
    }


# ============================================================
# Execução (para desenvolvimento)
# ============================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
