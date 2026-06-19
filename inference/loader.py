"""Model loader- loads models from disk, resolves compute device, and caches loaded models."""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch 
from utils.loader import AppConfig 
from utils.logger import setup_logger

import logging
logger = logging.getLogger(f"parallax.{__name__}")

# Cache of already loaded models
loaded_models= {}

def on_device() -> str:
    
    if torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"
    
def validate_model(model_name: str, config: AppConfig) -> None:
    if model_name not in config.models:
        available_models= ",".join(config.models.keys())

        raise ValueError(
            f"Model {model_name} is not registered\n"
            f"Available models: {available_models}"
        )
    
def load_model(model_name: str, config: AppConfig) -> dict:

    if model_name in loaded_models:
        logger.info(f"Using cached model: {model_name}")
        return loaded_models[model_name]
    
    validate_model(model_name, config)

    model_config= config.models[model_name]

    logger.info(f"Loading model: {model_name}")

    tokenizer= AutoTokenizer.from_pretrained(model_config.path)
    tokenizer.pad_token = tokenizer.eos_token
    model= AutoModelForCausalLM.from_pretrained(model_config.path)

    device = on_device()
    model.to(device)

    loaded_model={
        "name": model_name,
        "model": model,
        "tokenizer": tokenizer,
        "device": device,
    }

    loaded_models[model_name]= loaded_model

    logger.info(f"Model loaded: {model_name} on {device}")

    return loaded_model
