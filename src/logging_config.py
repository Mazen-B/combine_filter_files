import logging
from io import StringIO

log_buffer = StringIO()
log_handler = logging.StreamHandler(log_buffer)
log_handler.setLevel(logging.DEBUG)
log_formatter = logging.Formatter("%(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(log_handler)

def clear_log_buffer():
    log_buffer.seek(0)
    log_buffer.truncate(0)

def get_log_messages():
    log_buffer.seek(0)
    return log_buffer.read()
