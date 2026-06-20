from services.export import comp_benchmarks_serving
from services.serving import switch_model
from services.inference import generate_text_serving

import pytest


def test_generate_text_serving():
    with pytest.raises(ValueError):
        generate_text_serving("")

def test_switch_model():
    with pytest.raises(ValueError):
        switch_model("Fake model")

def test_comp_benchmark_serving():

    with pytest.raises(FileNotFoundError):
        comp_benchmarks_serving("benchmark_2026-06-11_20-03-16.json", "does_not_exist.json")