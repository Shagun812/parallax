"""Benchmark service- orchestrates benchmark runs and metric collection"""

from benchmark.runner import run_benchmark
from tracking.writer import save_benchmark
from utils.logger import setup_logger

import logging
logger = logging.getLogger(f"parallax.{__name__}")

def run_benchmark_service():

    try:
        logger.info("Starting benchmark run")

        report = run_benchmark()

        logger.info(f"Benchmark completed for model={report['model']}")

        artifact_path = save_benchmark(report)

        logger.info(f"Benchmark saved to {artifact_path}")

        return {
            "artifact_path": artifact_path,
            "report": report
        }
    except Exception:
        logger.exception("Benchmark failed")
        raise