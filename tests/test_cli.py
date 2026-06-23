from typer.testing import CliRunner
from unittest.mock import patch
from pathlib import Path

from cli.main import app

runner = CliRunner()

@patch("cli.main.models_list")
def test_models_list_cmd(mock_models):
    mock_models.return_value = ["gpt2", "gpt2-medium"]
    result = runner.invoke(app, ["models","list"])

    assert result.exit_code == 0
    assert "gpt2" in result.stdout
    assert "gpt2-medium" in result.stdout


@patch("cli.main.generate_text_serving")
def test_generate_cmd(mock_generate):

    mock_generate.return_value = {
        "response": "python is a high-level language",
        "input_tokens": 4,
        "output_tokens": 7,
        "generation_latency_ms": 10.5,
        "tokens_per_sec": 50.0,
    }

    result = runner.invoke(app,["generate", "--prompt", "python"])
    assert result.exit_code == 0
    assert "python" in result.stdout

@patch("cli.main.load_report_serving")
@patch("cli.main.list_experiments_serving")
def test_exp_list_cmd(mock_list, mock_load):


    mock_load.side_effect = [
    {
        "model": "gpt2",
        "metrics": {"total_prompts": 16,"total_runs": 48}
    },
    {
        "model": "gpt2-medium",
        "metrics": {"total_prompts": 16,"total_runs": 48}
    }
    ]    

    mock_list.return_value = [
        Path("benchmark_1.json"),
        Path("benchmark_2.json")
    ]

    result = runner.invoke(app, ["exp","list"])

    assert result.exit_code == 0

    assert "gpt2" in result.stdout
    assert "gpt2-medium" in result.stdout
    assert "benchmark_1.json" in result.stdout
    assert "benchmark_2.json" in result.stdout
