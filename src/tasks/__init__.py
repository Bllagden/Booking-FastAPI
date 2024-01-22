import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "src"))

from .tasks import send_booking_confirmation_email  # noqa: F401, E402
