import dotenv

dotenv.load_dotenv(".env.dev")

from .tasks import send_booking_confirmation_email  # noqa: E402

__all__ = [
    "send_booking_confirmation_email",
]
