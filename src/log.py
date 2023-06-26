"""Logging configuration."""
import logging

from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter("%(levelname)%%(message)%", timestamp=True)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
