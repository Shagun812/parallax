"""Config- load, validate and provide typed access to settings.yaml."""

from pathlib import Path
import yaml
from pydantic import BaseModel
from functools import cache
import os
from dotenv import load_dotenv

load_dotenv()



class ProjectConfig(BaseModel):
    name: str
    artifacts_dir: str

class ModelConfig(BaseModel):
    path: str
    type: str

class InferenceConfig(BaseModel):
    default_model: str
    device: str
    max_new_tokens: int
    do_sample: bool
    temperature: float
    top_p: float
    repetition_penalty: float

class BenchmarkConfig(BaseModel):
    prompt_file: Path
    runs_per_model: int 
    warmup_runs: int
    collect_latency: bool
    collect_memory: bool
    collect_throughput: bool
    collect_tokens_per_sec: bool

class QualityConfig(BaseModel):
    enabled: bool
    method: str
    embedding_model: str
    collect_coherence_score: bool

class LoggingConfig(BaseModel):
    enabled: bool
    level: str

class HuggingFaceConfig(BaseModel):
    token: str | None = None

class AppConfig(BaseModel):
    project: ProjectConfig
    models: dict[str, ModelConfig]
    inference: InferenceConfig
    benchmark: BenchmarkConfig
    quality: QualityConfig
    logging: LoggingConfig
    huggingface: HuggingFaceConfig

def get_config(path: str="config/settings.yaml") -> AppConfig:
    # Load YAML configuration and return validated AppConfig

    config_path= Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    
    
    with open(config_path,"r",encoding='utf-8') as f:
        raw= yaml.safe_load(f)
    hf_token = os.getenv("HF_TOKEN")
    raw["huggingface"] = {"token": hf_token}
    return AppConfig(**raw)

@cache
def load_config() -> AppConfig:
    return get_config()