from __future__ import annotations

import logging

logger = logging.getLogger("qb_widget")
logger.setLevel(logging.INFO)

logger.handlers = [logging.FileHandler("console.log", "w")]

class Console:

    @staticmethod
    def log(message):
        logger.info(message)
