"""
CLI entrypoint for all user facing commands
"""
import typer
from services.serving import get_current_model, switch_model, models_list
from services.benchmark import run_benchmark_service
from services.export import load_report_serving, comp_benchmarks_serving, list_experiments_serving
from services.inference import generate_text_serving

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()


# Main app
app = typer.Typer(help="Local LLM benchmarking and serving platform")

# Sub-apps
models_app = typer.Typer(help="Manage available models")
benchmark_app = typer.Typer(help="Run benchmarks and measure performance")
experiments_app = typer.Typer(help="View and compare experiment results")

app.add_typer(models_app, name="models")

app.add_typer(benchmark_app,name="benchmark")
app.add_typer(benchmark_app, name="bench")

app.add_typer(experiments_app,name="experiments")
app.add_typer(experiments_app, name="exp")


@models_app.command("list")
def list_model():
    """List all available models."""

    table = Table(title="Available Models")
    table.add_column("Model")
    
    models = models_list()

    for model in models:
        table.add_row(model)
    console.print(table)
        

@models_app.command("current")
def current_model():
    """Show the currently active model."""

    model_name= get_current_model()

    console.print(Panel(model_name, title="Current Model"))


@models_app.command("switch")
def switch_cmd(model_name:str = typer.Option(...,"-m", "--model", help="Model to switch to")):
    """Switch the active model."""

    current= get_current_model()

    if current== model_name:
        typer.echo(f"{model_name} already active")
        return
    
    switch_model(model_name)
    console.print(Panel(f"{model_name} switched!"))


@app.command("generate")
def generate_cmd(prompt:str= typer.Option(...,"-p","--prompt", help="Prompt to generate from"))-> None:
    """Run inference with the active model."""

    if not prompt.strip():
        raise typer.BadParameter("Prompt cannot be empty!")
    
    result= generate_text_serving(prompt)


    console.print(Panel(result["response"],title="Response"))

    metrics_table = Table(title="Generation Metrics")

    metrics_table.add_column("Metric")
    metrics_table.add_column("Value")

    metrics_table.add_row("Input Tokens",str(result["input_tokens"]))
    metrics_table.add_row("Output Tokens",str(result["output_tokens"]))

    metrics_table.add_row("Generation Time (ms)", str(result["generation_latency_ms"]))
    metrics_table.add_row("Tokens per sec", str(result["tokens_per_sec"]),)
    console.print(metrics_table)



@benchmark_app.command("run")
def benchmark_run():
    """Run benchmark for the active model."""

    console.print("[bold green] Running benchmark....[/bold green]")
    with console.status("Running benchmark..."):
        service_res = run_benchmark_service()

    artifact_path = service_res["artifact_path"]

    report = service_res["report"]

    metrics = report["metrics"]
    model_name= report["model"]


    console.print(Panel(model_name, title="Benchmark Model"))

    metrics_table= Table(title="Benchmark Results")
    metrics_table.add_column("Metric")
    metrics_table.add_column("Value")

    rows={
        "mean_latency_ms": "Mean Latency (ms)",
        "p50_latency_ms": "P50 Latency (ms)",
        "p95_latency_ms": "P95 Latency (ms)",
        "p99_latency_ms": "P99 Latency (ms)",
        "max_latency_ms": "Max Latency (ms)",
        "min_latency_ms": "Min Latency (ms)",
        "mean_tokens_per_sec": "Mean Throughput",
        "avg_input_tokens": "Avg Input Tokens",
        "avg_output_tokens": "Avg Output Tokens",
        "total_output_tokens": "Total Output Tokens"
    }

    for metric, display_name in rows.items():
        if metric in metrics:
            metrics_table.add_row(display_name, str(metrics[metric]))
    console.print(metrics_table)

    console.print(f"Benchmark saved: {artifact_path}")


@experiments_app.command("list")
def experiment_list():
    """List all saved benchmark reports."""

    exp_list = list_experiments_serving()

    metrics_table = Table(title="Benchmarks List")
    metrics_table.add_column("Report")
    metrics_table.add_column("Model")
    metrics_table.add_column("Prompts")
    metrics_table.add_column("Runs")

    if not exp_list:
        console.print("No benchmark reports found")
        return

    for path in exp_list:
        report = load_report_serving(path.name)
        metrics = report["metrics"]
        metrics_table.add_row(
            path.name, 
            report["model"],
            str(metrics["total_prompts"]),
            str(metrics["total_runs"])
            )

    console.print(metrics_table)


@experiments_app.command("show")
def exp_show(report_name:str = typer.Option(...,"-f", "--file", help="Report filename")):
    """Show details of a specific benchmark report."""

    report_data = load_report_serving(report_name)
    

    metrics = report_data["metrics"]

    table = Table(title="Benchmarks Report")

    console.print(Panel(report_data['model'], title= "Benchmark Model"))
    table.add_column("Metric")
    table.add_column("Value")


    rows={
        "mean_latency_ms": "Mean Latency (ms)",
        "p50_latency_ms": "P50 Latency (ms)",
        "p95_latency_ms": "P95 Latency (ms)",
        "p99_latency_ms": "P99 Latency (ms)",
        "max_latency_ms": "Max Latency (ms)",
        "min_latency_ms": "Min Latency (ms)",
        "mean_tokens_per_sec": "Mean Throughput",
        "avg_input_tokens": "Avg Input Tokens",
        "avg_output_tokens": "Avg Output Tokens",
        "total_output_tokens": "Total Output Tokens"
    }

    for metric, display_name in rows.items():
        if metric in metrics:
            table.add_row(display_name, str(metrics[metric]))
    console.print(table)


@experiments_app.command("compare")
def compare_benchmarks(
    report1:str = typer.Option(...,"-a", "--file-a", help="First benchmark report" ),
    report2: str= typer.Option(...,"-b","--file-b", help="Second benchmark report")): 
    """Compare two benchmark reports side by side."""
    
    comp = comp_benchmarks_serving(report1, report2)

    model1 = comp["model_a"]
    model2 = comp["model_b"]

    met = comp["metrics"]


    DISPLAY_NAMES = {
    "mean_latency_ms": "Mean Latency (ms)",
    "p50_latency_ms": "P50 Latency (ms)",
    "p95_latency_ms": "P95 Latency (ms)",
    "p99_latency_ms": "P99 Latency (ms)",
    "mean_tokens_per_sec": "Mean Throughput"

}

    table = Table(title="Comparison Report")
    table.add_column("Metric")
    table.add_column(model1)
    table.add_column(model2)
    table.add_column("Difference")
    table.add_column("Better")

    for metric_name, metric_data in met.items():
        display_name = DISPLAY_NAMES.get(metric_name, metric_name)
        table.add_row(
            display_name,
            str(metric_data["model_a"]),
            str(metric_data["model_b"]),
            str(metric_data["difference"]),
            str(metric_data["better"])
        )

    console.print(table)

    
 