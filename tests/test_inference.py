
import pytest
from inference.loader import validate_model, load_model
from inference.generator import generate
from utils.loader import load_config

cfg = load_config()
TEST_MODEL = cfg.inference.default_model

@pytest.fixture(scope="session")
def loaded_model():
    return load_model(TEST_MODEL, cfg)


# Validate Valid Model
def test_validate_valid_model():
     validate_model(TEST_MODEL,cfg)

# Validate invalid model
def test_validate_invalid_model():
    with pytest.raises(ValueError):
        validate_model("fake_model", cfg)


# Test loaded model's returns
def test_load_returns_components(loaded_model):
    
    assert "name" in loaded_model
    assert "model" in loaded_model
    assert "tokenizer" in loaded_model
    assert "device" in loaded_model


# Testing caching behaviour
def test_load_model_caching():
    model1 = load_model(TEST_MODEL, cfg)
    model2 = load_model(TEST_MODEL, cfg)
    assert model1 is model2  # Same object in memory, not just equal


# Test generator's returns
def test_generate_returns(loaded_model):
    result = generate(loaded_model,"Hello world!", cfg)
    assert "response" in result
    assert "input_tokens" in result
    assert "output_tokens" in result
    assert "generation_latency_ms" in result
    assert "tokens_per_sec" in result
    assert isinstance(result["response"], str)
    assert result["input_tokens"] > 0
    assert result["output_tokens"] >= 0
    assert result["tokens_per_sec"] > 0
    assert len(result["response"]) > 0
    assert isinstance(result["generation_latency_ms"],(int, float))
    assert isinstance(result["tokens_per_sec"],(int, float))


