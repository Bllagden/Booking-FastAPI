import dotenv

dotenv.load_dotenv(".dev.env")

from .tasks import send_booking_confirmation_email  # noqa: F401, E402
