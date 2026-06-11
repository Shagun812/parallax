"""Text generator- runs inference and returns generated responses"""


import time
import torch

def generate(loaded_model: dict, prompt: str, config) -> dict:

    model= loaded_model["model"]
    tokenizer= loaded_model["tokenizer"]
    device= loaded_model["device"]
    cfg=config.inference

    inputs= tokenizer(prompt, return_tensors="pt", padding=True)

    inputs={ 
        key: value.to(device)
        for key, value in inputs.items()
    }

    if device == "cuda":
        torch.cuda.synchronize()
        
    start_time= time.perf_counter()

    with torch.no_grad():
        output= model.generate(
            **inputs, 
            max_new_tokens= cfg.max_new_tokens,
            do_sample=cfg.do_sample,
            temperature=cfg.temperature,
            top_p=cfg.top_p,
            repetition_penalty=cfg.repetition_penalty,
            pad_token_id= tokenizer.eos_token_id
            )

    end_time = time.perf_counter()
    input_length= inputs["input_ids"].shape[1]

    generated_ids= output[0,input_length:]

    response= tokenizer.decode(generated_ids, skip_special_tokens=True)

    time_taken_ms =(end_time-start_time)*1000
    tokens_per_sec = generated_ids.shape[0] /(time_taken_ms / 1000)

    return {
        "response": response,
        "input_tokens": input_length,
        "output_tokens": generated_ids.shape[0],
        "generation_latency_ms": round(time_taken_ms,2),
        "tokens_per_sec": round(tokens_per_sec, 2),
    }





