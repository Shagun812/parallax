from benchmark.runner import load_prompts, run_benchmark
from benchmark.metrics import compute_metrics
from benchmark.comparator import comp_benchmarks
from utils.loader import load_config

import pytest

cfg = load_config()

# Test prompt loader
def test_load_prompts_returns():
    prompts = load_prompts()
    assert isinstance(prompts, list)
    assert len(prompts) > 0

# Test metrics

# Empty input
def test_compute_metrics_empty_results():
    with pytest.raises(ValueError):
        compute_metrics([], cfg)

# Expected keys
bench_res = [
    {
        "id": "001",
        "input_tokens": 10,
        "output_tokens": 20,
        "generation_latency_ms": 100,
        "tokens_per_sec": 50
    },
    {
        "id": "002",
        "input_tokens": 12,
        "output_tokens": 25,
        "generation_latency_ms": 200,
        "tokens_per_sec": 40
    }
]

def test_compute_metrics_returns_keys():
    metrics = compute_metrics(bench_res, cfg)

    assert "total_runs" in metrics
    assert "total_prompts" in metrics

    assert "mean_latency_ms" in metrics
    assert "p50_latency_ms" in metrics
    assert "p95_latency_ms" in metrics
    assert "p99_latency_ms" in metrics

    assert "mean_tokens_per_sec" in metrics

    assert "avg_input_tokens" in metrics
    assert "avg_output_tokens" in metrics
    assert "total_output_tokens" in metrics


def test_compute_metrics_known_values():
    metrics = compute_metrics(bench_res, cfg)

    assert metrics["total_runs"] == 2
    assert metrics["total_prompts"] == 2
    assert metrics["avg_input_tokens"] == 11
    assert metrics["avg_output_tokens"] == 22.5
    assert metrics["total_output_tokens"] == 45
    assert metrics["mean_tokens_per_sec"] == 45


# Testing Different prompt sets
def test_compare_diff_prompts():
    report_a = {
        "model": "gpt2",
        "metrics": {"total_prompts":5}
    }

    report_b = {
        "model": "gpt2-medium",
        "metrics": {"total_prompts":4}
    }

    with pytest.raises(ValueError):
        comp_benchmarks(report_a, report_b)
    
# Testing latency logic

def test_latency_comparison():

    report_a = {
        "model": "gpt2",
        "metrics": {
            "total_prompts": 5,
            "mean_latency_ms": 100
        }
    }

    report_b = {
        "model": "gpt2-medium",
        "metrics": {
            "total_prompts": 5,
            "mean_latency_ms": 50
        }
    }

    result = comp_benchmarks(report_a, report_b)

    assert (result["metrics"]["mean_latency_ms"]["better"]== "gpt2-medium")

# Testing throughput logic

def test_throughput_comparison():

    report_a = {
        "model": "gpt2",
        "metrics": {
            "total_prompts": 5,
            "mean_tokens_per_sec": 20
        }
    }

    report_b = {
        "model": "gpt2-medium",
        "metrics": {
            "total_prompts": 5,
            "mean_tokens_per_sec": 50
        }
    }

    result = comp_benchmarks(report_a,report_b)

    assert (result["metrics"]["mean_tokens_per_sec"]["better"]== "gpt2-medium")

# Testing tie
def test_comparison_tie():

    report_a = {
        "model": "gpt2",
        "metrics": {
            "total_prompts": 5,
            "mean_latency_ms": 100
        }
    }

    report_b = {
        "model": "gpt2-medium",
        "metrics": {
            "total_prompts": 5,
            "mean_latency_ms": 100
        }
    }

    result = comp_benchmarks(report_a,report_b)

    assert (result["metrics"]["mean_latency_ms"]["better"]== "tie")