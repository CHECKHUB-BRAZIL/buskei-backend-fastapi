from pydantic import BaseModel, Field


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
