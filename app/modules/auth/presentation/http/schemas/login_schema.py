from pydantic import BaseModel, EmailStr, Field


class LoginRequestDTO(BaseModel):
    """
    DTO para requisição de login.
    
    Valida dados de entrada usando Pydantic.
    """
    
    email: EmailStr = Field(
        ...,
        description="Email do usuário",
        example="joao@example.com"
    )
    senha: str = Field(
        ...,
        min_length=6,
        description="Senha do usuário",
        example="senha123"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "joao@example.com",
                "senha": "senha123"
            }
        }


class LoginResponseDTO(BaseModel):
    """
    DTO para resposta de login.
    
    Retorna dados do usuário e tokens de autenticação.
    """
    
    user: 'UserResponseDTO'
    access_token: str = Field(..., description="Token de acesso JWT")
    refresh_token: str = Field(..., description="Token de refresh")
    token_type: str = Field(default="Bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    
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
                "expires_in": 1800
            }
        }


class UserResponseDTO(BaseModel):
    """
    DTO para resposta com dados do usuário.
    
    Remove informações sensíveis (senha, etc).
    """
    
    id: str = Field(..., description="ID único do usuário")
    nome: str = Field(..., description="Nome do usuário")
    email: str = Field(..., description="Email do usuário")
    is_active: bool = Field(..., description="Status do usuário")
    created_at: str = Field(..., description="Data de criação")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome": "João Silva",
                "email": "joao@example.com",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


# Forward reference para evitar import circular
LoginResponseDTO.model_rebuild()
