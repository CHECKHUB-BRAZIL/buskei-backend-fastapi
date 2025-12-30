from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequestDTO(BaseModel):
    """
    DTO para requisição de registro.
    
    Valida dados de entrada para criação de novo usuário.
    """
    
    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome completo do usuário",
        example="João Silva"
    )
    email: EmailStr = Field(
        ...,
        description="Email do usuário",
        example="joao@example.com"
    )
    senha: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Senha do usuário",
        example="senha123"
    )
    
    @field_validator('nome')
    @classmethod
    def validate_nome(cls, v: str) -> str:
        """Valida e normaliza o nome."""
        v = v.strip()
        if len(v) < 2:
            raise ValueError("Nome deve ter no mínimo 2 caracteres")
        return v
    
    @field_validator('senha')
    @classmethod
    def validate_senha(cls, v: str) -> str:
        """Valida força da senha."""
        if not any(c.isalpha() for c in v):
            raise ValueError("Senha deve conter pelo menos uma letra")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João Silva",
                "email": "joao@example.com",
                "senha": "senha123"
            }
        }


class RegisterResponseDTO(BaseModel):
    """
    DTO para resposta de registro.
    
    Retorna dados do usuário criado e tokens de autenticação.
    """
    
    user: 'UserResponseDTO'
    access_token: str = Field(..., description="Token de acesso JWT")
    refresh_token: str = Field(..., description="Token de refresh")
    token_type: str = Field(default="Bearer", description="Tipo do token")
    message: str = Field(default="Usuário criado com sucesso", description="Mensagem de sucesso")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "nome": "João Silva",
                    "email": "joao@example.com",
                    "is_active": True,
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "Bearer",
                "message": "Usuário criado com sucesso"
            }
        }


# Import necessário para resolver forward reference
from app.modules.auth.application.dtos.login_dto import UserResponseDTO

RegisterResponseDTO.model_rebuild()
