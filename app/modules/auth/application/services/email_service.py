from abc import ABC, abstractmethod


class EmailService(ABC):
    """
    Contrato para serviços de envio de emails.
    
    As implementações concretas ficam na infraestrutura,
    utilizando provedores como SMTP, Resend, SendGrid, etc.
    """

    @abstractmethod
    async def send_password_reset(
        self,
        email: str,
        reset_url: str,
    ) -> None:
        """
        Envia email contendo link para redefinição de senha.
        """
        raise NotImplementedError
