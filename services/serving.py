"""Serving service- manages active model selection and switching"""

from services.state import get_active_model, set_active_model
from utils.loader import load_config
from inference.loader import load_model


config = load_config()


def get_current_model() -> str:
    return get_active_model()


def switch_model(model_name: str) -> str: 

    if model_name not in config.models:
        available = ", ".join(config.models.keys())
        raise ValueError(
            f"{model_name} not found!\n"
            f"Available models: {available}"
            )
    # Verify the model can be loaded
    load_model(model_name, config)
    set_active_model(model_name)
        
    return model_name



def get_loaded_model() -> dict:
    model_name= get_active_model()
    return load_model(model_name, config)



