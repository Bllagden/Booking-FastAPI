import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from settings import LogSettings, get_settings

logger = logging.getLogger()
_log_handler = logging.StreamHandler()
_log_settings = get_settings(LogSettings)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict) -> None:
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname


formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s",
)

_log_handler.setFormatter(formatter)
logger.addHandler(_log_handler)
logger.setLevel(_log_settings.level)
