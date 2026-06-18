"""FASTAPI application - HTTPS interface for parallax"""

from fastapi import FastAPI
from api.schemas import HealthResponse, CurrentModelResponse,ModelsListResponse, SwitchModelResponse, GenerateRequest, GenerateResponse, SwitchModelRequest
from services.serving import get_current_model, models_list, switch_model
from services.inference import generate_text_serving

app = FastAPI(title="Parallax", version="0.1.0")


@app.get("/")
async def root():

    return {"service": "Parallax",
            "version": "0.1.0",
            "status": "running"
        }



@app.get("/health/", response_model=HealthResponse)
async def check_health():

    return HealthResponse(status="Healthy")



@app.get("/models/current", response_model= CurrentModelResponse)
async def current_model():

    model = get_current_model()

    return CurrentModelResponse(current_model=model)



@app.get("/models", response_model=ModelsListResponse)
async def list_models():

    model_l = models_list()

    return ModelsListResponse(models= model_l)



@app.post("/models/switch", response_model=SwitchModelResponse)
async def switching_model(request: SwitchModelRequest):

    model = switch_model(request.model_name)

    return SwitchModelResponse(current_model=model, message=f"Switched to {model} successfully")



@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):

    response = generate_text_serving(request.prompt)
    
    return GenerateResponse(**response)