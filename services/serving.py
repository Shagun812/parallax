"""Serving service- manages active model selection and switching"""

from services.state import get_active_model, set_active_model
from utils.loader import load_config
from inference.loader import load_model
from utils.logger import setup_logger

import logging
logger = logging.getLogger(f"parallax.{__name__}")


config = load_config()


def get_current_model() -> str:
    return get_active_model()


def switch_model(model_name: str) -> str: 

    try:

        logger.info(f"Starting switching to {model_name}")

        if model_name not in config.models:
            available = ", ".join(config.models.keys())
            raise ValueError(
                f"{model_name} not found!\n"
                f"Available models: {available}"
                )
        set_active_model(model_name)
        logger.info(f"Model switched to {model_name}")
            
        return model_name
    except Exception:
        logger.exception("Switching failed")
        raise




def get_loaded_model() -> dict:
    model_name= get_active_model()
    return load_model(model_name, config)


def models_list()-> list[str]:

    return list(config.models.keys())
