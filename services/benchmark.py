"""Benchmark service- orchestrates benchmark runs and metric collection"""
from benchmark.runner import run_benchmark
from tracking.writer import save_benchmark

def run_benchmark_service():
    report = run_benchmark()
    artifact_path = save_benchmark(report)

    return {
        "artifact_path": artifact_path,
        "report": report
    }
