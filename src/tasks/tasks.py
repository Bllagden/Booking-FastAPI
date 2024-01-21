import smtplib

from pydantic import EmailStr

from settings import smtp_settings

from .celery import celery
from .email_templates import create_booking_confirmation_template


@celery.task  # BackgroundTasks
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    email_to = smtp_settings.USER  # отправка на свою почту
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(smtp_settings.HOST, smtp_settings.PORT) as server:
        server.login(smtp_settings.USER, smtp_settings.PASSWORD)
        server.send_message(msg_content)
