"""Export service- coordinates artifact writing and manifest updates"""

from tracking.report import get_reports_dir, list_reports, load_report
from benchmark.comparator import comp_benchmarks

def list_experiments_serving():

    list_exp = list_reports()

    return list_exp


def load_report_serving(report_name):


    rep_dir = get_reports_dir()
    report_dir = rep_dir/report_name

    if not report_dir.exists():
        raise FileNotFoundError(f"Report {report_dir} not exists")

    loaded_report = load_report(report_dir)

    
    return loaded_report


def comp_benchmarks_serving(report1:str, report2:str):

    dir = get_reports_dir()


    report1_path = dir/report1
    report2_path = dir/report2

    report_a = load_report(report1_path)

    report_b = load_report(report2_path)

    if report_a is None:
        raise FileNotFoundError(f"Report not found: {report1}")
    
    if report_b is None:
        raise FileNotFoundError(f"Report not found: {report2}")

    comp = comp_benchmarks(report_a, report_b)

    return comp
