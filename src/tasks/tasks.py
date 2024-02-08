import smtplib

from pydantic import EmailStr

from settings import SMTPSettings, get_settings

from .celery import celery
from .email_templates import create_booking_confirmation_template

_smtp_settings = get_settings(SMTPSettings)


@celery.task  # BackgroundTasks
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    email_to = _smtp_settings.user  # отправка на свою почту
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(_smtp_settings.host, _smtp_settings.port) as server:
        server.login(_smtp_settings.user, _smtp_settings.password)
        server.send_message(msg_content)
