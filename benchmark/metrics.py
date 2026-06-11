"""Metrics collector- measures execution performance"""

import numpy as np


def compute_metrics(bench_res, cfg):


    if not bench_res:
        raise ValueError("No benchmark results provided")
    
 
    input_tokens = np.array( [r["input_tokens"] for r in bench_res])
    output_tokens = np.array([r["output_tokens"] for r in bench_res])

    avg_input_tokens = round(float(np.mean(input_tokens)),2)
    avg_output_tokens = round(float(np.mean(output_tokens)),2)

    total_runs = len(bench_res)
    total_prompts = len(set(r["id"] for r in bench_res))

    total_output_tokens= int(np.sum(output_tokens))


    metrics={
        "total_runs": total_runs,
        "total_prompts": total_prompts
    }


    if cfg.benchmark.collect_latency:

        latencies = np.array([r["generation_latency_ms"] for r in bench_res])

        mean_latency = round(float(np.mean(latencies)),2)
        P99_latency = round(float(np.percentile(latencies, 99)),2)
        P95_latency = round(float(np.percentile(latencies, 95)),2)
        P50_latency = round(float(np.percentile(latencies, 50)),2)
        min_latency = round(float(np.min(latencies)),2)
        max_latency = round(float(np.max(latencies)),2)

        metrics.update({

            "mean_latency_ms": mean_latency,
            "p50_latency_ms": P50_latency,
            "p95_latency_ms": P95_latency,
            "p99_latency_ms": P99_latency,
            "min_latency_ms": min_latency,
            "max_latency_ms": max_latency,
        })


    if cfg.benchmark.collect_throughput:

        tokens_per_sec = np.array([r["tokens_per_sec"] for r in bench_res])

        mean_tokens_per_sec = round(float(np.mean(tokens_per_sec)),2)
        p99_tokens_per_sec = round(float(np.percentile(tokens_per_sec, 99)),2)
        p95_tokens_per_sec = round(float(np.percentile(tokens_per_sec,95)),2)
        p50_tokens_per_sec = round(float(np.percentile(tokens_per_sec,50)),2)

        metrics.update({
            "mean_tokens_per_sec": mean_tokens_per_sec,
            "p50_tokens_per_sec": p50_tokens_per_sec,
            "p95_tokens_per_sec": p95_tokens_per_sec,
            "p99_tokens_per_sec": p99_tokens_per_sec,
        })


    metrics.update({
        "avg_input_tokens": avg_input_tokens,
        "avg_output_tokens": avg_output_tokens,
        "total_output_tokens": total_output_tokens
    })
    

    return metrics
    


