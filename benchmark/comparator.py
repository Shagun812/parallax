"""Experiment comparator- comparing two models based on benchmark runs"""


def comp_benchmarks(report_a: dict,report_b: dict)-> dict: 

    model1 = report_a["model"]
    model2 = report_b["model"]

    metrics_a= report_a["metrics"]
    metrics_b= report_b["metrics"]


    LATENCY_METRICS = [
         
        "mean_latency_ms",
        "p50_latency_ms",
        "p95_latency_ms",
        "p99_latency_ms"

    ]

    THROUGHPUT_METRICS = [
         "mean_tokens_per_sec"
    ]


    # Prompt Validation
    if not report_a["metrics"]["total_prompts"] == report_b["metrics"]["total_prompts"]:
            raise ValueError("Benchmarks were run on different prompt sets")
    

    comp={}


    for metric in LATENCY_METRICS:

        if metric not in metrics_a or metric not in metrics_b:
            continue


        value_a= metrics_a[metric]
        value_b= metrics_b[metric]

        
        if value_a < value_b:
             better = model1
        elif value_a > value_b:
             better= model2
        else:
            better = "tie"

        comp[metric] = {
            "model_a": value_a,
            "model_b": value_b,
            "difference": round(abs(value_b-value_a),2), # difference = model_b- model_a
            "better": better
        }

    for metric in THROUGHPUT_METRICS:

        if metric not in metrics_a or metric not in metrics_b:
            continue
        
        value_a= metrics_a[metric]
        value_b= metrics_b[metric]

        if value_a > value_b:
            better= model1
        elif value_a < value_b:
            better= model2
        else: 
            better = "tie"

        comp[metric] = {
            "model_a": value_a,
            "model_b": value_b,
            "difference": round(abs(value_b-value_a),2), # difference = model_b- model_a
            "better": better
        }



    return {
        "model_a": model1,
        "model_b": model2,
        "metrics": comp
    }

    

    

