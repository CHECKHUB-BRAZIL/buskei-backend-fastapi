from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    async def send_password_reset(
        self,
        email: str,
        reset_url: str,
    ) -> None:
        pass
