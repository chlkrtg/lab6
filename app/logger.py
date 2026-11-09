import logging

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("fastapi_lab")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        logger.addHandler(handler)
    return logger

logger = setup_logger()