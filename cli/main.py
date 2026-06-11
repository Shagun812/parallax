"""
CLI entrypoint for all user facing commands
"""
import typer
from utils.loader import load_config
from inference.generator import generate
from services.serving import get_loaded_model, get_current_model, switch_model

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


console = Console()
metrics_table= Table()



# Main app
app = typer.Typer()

# Sub-apps
models_app = typer.Typer()
benchmark_app = typer.Typer()
experiments_app = typer.Typer()

app.add_typer(models_app, name="models")
app.add_typer(benchmark_app,name="benchmark")
app.add_typer(experiments_app,name="experiments")

config = load_config()
default_model= config.inference.default_model



@models_app.command("list")
def models_list():
    
    text=" "
    
    for model_name in config.models:
        if model_name== default_model:
            text+= (f"-{model_name}(default)\n")
        else:
            text+= (f" -{model_name}")
    console.print(Panel(text, title="Available Models"))


@models_app.command("current")
def current_model():

    model_name= get_current_model()

    console.print(Panel(model_name, title="Current Model"))


@models_app.command("switch")
def switch_cmd(model_name:str):

    current= get_current_model()

    if current== model_name:
        typer.echo(f"{model_name} already active")
        return
    
    switch_model(model_name)
    console.print(Panel(f"{model_name} switched!"))


@app.command("generate")
def generate_cmd(prompt:str= typer.Option(..., "--prompt", help="Prompt to generate from"))-> None:

    if not prompt.strip():
        raise typer.BadParameter("Prompt cannot be empty!")
    

    model= get_loaded_model()
    result= generate(model, prompt, config)


    console.print(Panel(result["response"],title="Response"))

    metrics_table = Table(title="Generation Metrics")

    metrics_table.add_column("Metric")
    metrics_table.add_column("Value")

    metrics_table.add_row("Input Tokens",str(result["input_tokens"]))
    metrics_table.add_row("Output Tokens",str(result["output_tokens"]))

    metrics_table.add_row("Generation Time (ms)", str(result["generation_latency_ms"]))
    metrics_table.add_row("Tokens per sec", str(result["tokens_per_sec"]),)
    console.print(metrics_table)

