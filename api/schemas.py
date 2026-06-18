"""Pydantic schemas- request and response for API"""

from pydantic import BaseModel



# Health Endpoint

class HealthResponse(BaseModel):
    status: str


# Models List Endpoint

class ModelsListResponse(BaseModel):
    models: list[str]


# Current Model Endpoint

class CurrentModelResponse(BaseModel):
    current_model: str | None


# Model switch endpoint

class SwitchModelRequest(BaseModel):
    model_name: str


class SwitchModelResponse(BaseModel):
    current_model: str
    message: str

# Generate Endpoint

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    response: str
    input_tokens: int
    output_tokens: int
    generation_latency_ms: float 
    tokens_per_sec: float


