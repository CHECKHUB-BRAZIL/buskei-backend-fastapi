from app.modules.auth.application.services.email_service import (
    EmailService,
)


class ConsoleEmailService(EmailService):
    async def send_password_reset(
        self,
        email: str,
        reset_url: str,
    ) -> None:
        print(
            f"\n[EMAIL PASSWORD RESET]\n"
            f"To: {email}\n"
            f"Link: {reset_url}\n"
        )
