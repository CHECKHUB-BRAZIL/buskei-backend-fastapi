# 🚀 Busquei API

API RESTful construída com **FastAPI**, seguindo princípios de **Clean Architecture** e **Domain-Driven Design (DDD)**.

## 📋 Índice

- [Características](#características)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Migrações](#migrações)
- [Testes](#testes)

## ✨ Características

- ✅ Clean Architecture
- ✅ Domain-Driven Design (DDD)
- ✅ Modular e escalável
- ✅ Autenticação JWT
- ✅ Validação com Pydantic
- ✅ Documentação automática (Swagger/ReDoc)
- ✅ Migrações com Alembic
- ✅ Type hints completos
- ✅ CORS configurável

## 🏗️ Arquitetura
```
Domain Layer (Entidades, Value Objects, Repositórios)
    ↓
Application Layer (Use Cases, DTOs)
    ↓
Infrastructure Layer (Models, Implementações)
    ↓
Presentation Layer (Routes, Dependencies)
```

## 🛠️ Tecnologias

- **Framework**: FastAPI 0.104+
- **Database**: PostgreSQL + SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **Migrations**: Alembic
- **Validation**: Pydantic V2

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <repo-url>
cd busquei-api
```

### 2. Crie ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale dependências
```bash
pip install -r requirements.txt
```

### 4. Configure variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas configurações
```

### 5. Configure o banco de dados
```bash
# Crie o banco PostgreSQL
createdb busquei_db

# Execute migrações
alembic upgrade head
```

## 🚀 Uso

### Desenvolvimento
```bash
uvicorn main:app --reload
```

### Produção
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API**: http://localhost:8000/api/v1

## 📁 Estrutura do Projeto
```
app/
├── modules/              # Módulos de negócio
│   └── auth/
│       ├── domain/       # Entidades, Value Objects, Interfaces
│       ├── application/  # Use Cases, DTOs
│       ├── infrastructure/  # Models, Implementações
│       └── presentation/    # Routes, Dependencies
│
├── shared/              # Código compartilhado
│   ├── domain/
│   ├── infrastructure/
│   └── presentation/
│
├── core/                # Configurações globais
│   ├── config.py
│   └── constants.py
│
└── main.py             # Entry point
```

## 🔌 API Endpoints

### Auth

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/v1/auth/register` | Registrar usuário | ❌ |
| POST | `/api/v1/auth/login` | Login | ❌ |
| POST | `/api/v1/auth/logout` | Logout | ✅ |
| GET | `/api/v1/auth/me` | Usuário atual | ✅ |
| POST | `/api/v1/auth/refresh` | Renovar token | ❌ |

### Exemplo de Request
```bash
# Registro
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "senha": "senha123"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@example.com",
    "senha": "senha123"
  }'

# Acessar rota protegida
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <seu_token>"
```

## 🗄️ Migrações
```bash
# Criar nova migração
alembic revision --autogenerate -m "Descrição da migração"

# Aplicar migrações
alembic upgrade head

# Reverter última migração
alembic downgrade -1

# Ver histórico
alembic history
```

## 🧪 Testes
```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar testes
pytest

# Com cobertura
pytest --cov=app tests/
```

## 📝 Licença

MIT

## 👨‍💻 Autor

Seu Nome
