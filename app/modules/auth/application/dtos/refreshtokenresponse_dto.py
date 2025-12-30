from app.shared.infrastructure.database.base import BaseModel

class RefreshTokenResponseDTO(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
