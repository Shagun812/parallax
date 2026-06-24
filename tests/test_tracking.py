from tracking.writer import save_benchmark
from tracking.report import load_report
from utils.loader import load_config

import pytest
import json
cfg = load_config()

# Test: Empty Report
def test_save_benchmark_empty_report():
    report = {}
    with pytest.raises(ValueError):
        save_benchmark(report)

# Test: File created
def test_save_benchmark_create_file():
    report = {
        "model": "gpt2",
        "metrics": {"total_prompts": 5,
                    "total_runs":3,
                    "mean_latency_ms": 100}
    }

    path = save_benchmark(report)
    assert path.exists()

# Data preserved
def test_save_benchmark_persist_data():

    report = {
    "model": "gpt2",
    "metrics": {"total_prompts": 5,
                "total_runs":3,
                "mean_latency_ms": 100}
    }

    path = save_benchmark(report)

    with open(path, encoding="utf-8") as f:
        saved = json.load(f)

    assert saved == report

# Test loading existing reports
def test_load_report():

    report = {
    "model": "gpt2",
    "metrics": {"total_prompts": 5,
                "total_runs":3,
                "mean_latency_ms": 100}
    }

    path = save_benchmark(report)

    loaded = load_report(path)

    assert loaded == report
