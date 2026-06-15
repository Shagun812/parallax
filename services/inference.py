"""Inference service- coordinates model loading and text generation"""

from services.serving import get_loaded_model
from inference.generator import generate
from utils.loader import load_config


def generate_text_serving(prompt:str):

    cfg = load_config()

    if not prompt:
        raise ValueError("The prompt not found")
    
    loaded_model = get_loaded_model()
    res = generate(loaded_model, prompt, cfg)

    return res
    