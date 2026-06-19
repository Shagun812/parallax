"""Artifact writer- saves experiment data as structured JSON files"""

from utils.loader import load_config
from pathlib import Path
from datetime import datetime
import json
from utils.logger import setup_logger

import logging
logger = logging.getLogger(f"parallax.{__name__}")


def save_benchmark(report: dict)-> Path:

    cfg = load_config()

    if not report:
        logger.warning("Benchmark report is empty")
        raise ValueError("The benchmark report is empty!")
    
    artifacts_dir = Path(cfg.project.artifacts_dir)
    benchmark_dir = artifacts_dir/"benchmarks"

    if not benchmark_dir.exists():
        benchmark_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()

    #formatting

    timestamp= now.strftime("%Y-%m-%d_%H-%M-%S")

    filename= f"benchmark_{timestamp}.json"

    filepath= benchmark_dir/filename


    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)


    return filepath