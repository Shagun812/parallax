"""Report generator - report access layer"""

from pathlib import Path
from utils.loader import load_config
import json


def get_reports_dir() -> Path:

    cfg = load_config()
    return Path(cfg.project.artifacts_dir)/"benchmarks"



def list_reports() -> list[Path]:

    reports_dir = get_reports_dir()

    if not reports_dir.exists():
        return []
    
    reports = list(reports_dir.glob("*.json"))
    return sorted(reports, reverse=True)
    


def load_report(path: Path) -> dict:

    if not path.exists():
        raise FileNotFoundError(f"Report not found: {path}")

    try:    
        with open(path, "r",encoding="utf-8") as f:
            report = json.load(f)

    except json.JSONDecodeError:
        raise ValueError(f"Json {path} not found ")
    
    return report


