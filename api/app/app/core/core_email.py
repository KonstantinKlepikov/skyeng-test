import asyncio
from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
    MessageType,
        )
from pydantic import EmailStr
from app.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD.get_secret_value(),
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
        )


async def send_email(
    message: str,
    recipient: EmailStr,
    subject: str
        ) -> None:
    """Send email
    """
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=message,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)


if __name__ == "__main__":

    asyncio.run(send_email(
        message="This",
        recipient=settings.MAIL_FROM,
        subject="Me")
                )
