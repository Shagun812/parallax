"""Benchmark runner- produce benchmark outputs"""

from utils.loader import load_config
from services.serving import get_loaded_model, get_current_model
from inference.generator import generate
from benchmark.metrics import compute_metrics
import json

cfg = load_config()


def load_prompts() -> list[dict]:


    prompt_filepath= cfg.benchmark.prompt_file


    if not prompt_filepath.exists():
        raise FileNotFoundError(f"Prompts file not found at {prompt_filepath}")

    with open(prompt_filepath,"r", encoding="utf-8") as f:
        prompts = json.load(f)
    return prompts

def run_benchmark():
    prompts= load_prompts()
    model=get_loaded_model()
    model_name= get_current_model()
    runs_per_model= cfg.benchmark.runs_per_model

    if not prompts:
        raise ValueError("Benchmark dataset is empty!")
    
    # warmup-runs(to be discarded)
    for i in range(cfg.benchmark.warmup_runs):
        generate(model, prompts[0]["prompt"],cfg)


    benchmark_res=[]


    for prompt in prompts:
        for run_num in range(runs_per_model):

            gen=generate(model,prompt["prompt"], cfg)
            run_res={}
            run_res["run"]= run_num+1
            run_res["id"]=prompt["id"]
            run_res["category"]=prompt["category"]
            run_res["prompt"]=prompt["prompt"]
            run_res["response"]= gen["response"]
            run_res["input_tokens"]= gen["input_tokens"]
            run_res["output_tokens"]= gen["output_tokens"]
            run_res["generation_latency_ms"]= gen["generation_latency_ms"]
            run_res["tokens_per_sec"]=gen["tokens_per_sec"]


            benchmark_res.append(run_res)

            
    return {
        "model": model_name,
        "results": benchmark_res,
        "metrics": compute_metrics(benchmark_res,cfg)
    }
