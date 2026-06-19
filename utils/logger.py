"""Logger- configures structured logging for the application"""

from pathlib import Path
from utils.loader import load_config

import logging


def setup_logger()-> logging.Logger:

    logger = logging.getLogger("parallax")
    cfg = load_config()

    if not cfg.logging.enabled:
        logging.disable(logging.CRITICAL)
        return logger


    #Fallback to info
    log_level = getattr(logging, cfg.logging.level.upper(), logging.INFO)
    
    logger.setLevel(log_level)


    if logger.handlers:
        return logger
    
    logs_dir = Path(cfg.project.artifacts_dir)/"logs"
    logs_dir.mkdir(parents=True, exist_ok= True)

    log_file = logs_dir/"parallax.log"

    formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s", datefmt= "%Y-%m-%d %H:%M:%S")

    #File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    #Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger()