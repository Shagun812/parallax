"""Inference service- coordinates model loading and text generation"""

from services.serving import get_loaded_model
from inference.generator import generate
from utils.loader import load_config

import logging
logger = logging.getLogger(f"parallax.{__name__}")

def generate_text_serving(prompt:str):

    try:

        cfg = load_config()

        if not prompt or not prompt.strip():
            logger.warning("Empty string received")
            raise ValueError("The prompt not found")
        
        loaded_model = get_loaded_model()

        logger.info("Starting text generation")

        res = generate(loaded_model, prompt, cfg)

        logger.info("Text generation completed")

        return res
    
    except Exception:
        logger.exception("Generation failed")
        raise