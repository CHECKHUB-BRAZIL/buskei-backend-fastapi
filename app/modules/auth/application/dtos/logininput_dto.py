from dataclasses import dataclass

from app.modules.auth.domain.value_objects.user_id_vo import UserId

@dataclass(frozen=True)
class LoginInputDTO:
    """
    DTO de entrada do caso de uso de login.

    Responsabilidades:
    ------------------
    - Transportar dados já validados da camada presentation
    - Utilizar Value Object do domínio
    - Não conter lógica de negócio
    """
    user_id: UserId
