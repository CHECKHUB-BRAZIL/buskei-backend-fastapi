import resend

from app.core.config import settings
from app.modules.auth.application.services.email_service import (
    EmailService,
)


class ResendEmailService(EmailService):
    def __init__(self):
        resend.api_key = settings.RESEND_API_KEY

    async def send_password_reset(
        self,
        email: str,
        reset_url: str,
    ) -> None:

        resend.Emails.send(
            {
                "from": (
                    f"{settings.EMAIL_FROM_NAME} "
                    f"<{settings.EMAIL_FROM}>"
                ),
                "to": [email],
                "subject": "Recuperação de senha",
                "html": f"""
                    <h2>Recuperação de senha</h2>

                    <p>
                        Recebemos uma solicitação para redefinir
                        sua senha.
                    </p>

                    <p>
                        Clique no link abaixo:
                    </p>

                    <p>
                        <a href="{reset_url}">
                            Redefinir senha
                        </a>
                    </p>

                    <p>
                        Se você não solicitou esta alteração,
                        ignore este email.
                    </p>
                """,
            }
        )
