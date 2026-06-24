# Parallax

### A Local LLM Benchmarking, Experimentation, and Serving Platform

---

## Table of Contents

- [Why Parallax](#why-parallax)
- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [CLI](#cli)
  - [REST API](#rest-api)
- [Runtime Artifacts](#runtime-artifacts)
- [Project Structure](#project-structure)
- [Benchmarks & Experiment Tracking](#benchmarks--experiment-tracking)
- [Testing](#testing)
- [Supported Models](#supported-models)
- [V1 Scope & Limitations](#v1-scope--limitations)
- [V2 Roadmap](#v2-roadmap)
- [License](#license)

---

## Why Parallax

Most LLM projects are notebooks. A notebook runs a model, it doesn't tell you much about how a real system is structured, how services talk to each other, how dependencies flow, how you separate transport from business logic from infrastructure, or how you make results reproducible across runs.

Parallax was built to answer those questions concretely, by implementing them rather than reading about them. The goal was to understand how production AI systems are actually organized — what a service layer does, why CLI and HTTP endpoints shouldn't duplicate logic, how benchmarking infrastructure differs from just timing a cell, and what experiment tracking looks like when results need to be reproducible.

The result is a platform that is deliberately over-engineered for local use — not because local use requires it, but because the engineering is the point.

---

## Screenshots

### CLI

![CLI](docs/CLI.png.png)
---

## Overview

Parallax is a modular local LLM platform built around a production-inspired service architecture.

It exposes two interfaces over a shared service layer. The CLI provides full platform access — model management, text generation, benchmark execution, and experiment tracking. 

The FastAPI layer exposes a focused subset: model management and inference through a typed HTTP interface with Swagger documentation.

Benchmarking and experiment tracking are CLI-driven workflows. Results are persisted as structured JSON artifacts and can be loaded, inspected, and compared across runs.

---

## Key Features

**Model Management**
- List available models from configuration
- View and switch the active model at runtime
- Persistent model state across commands

**Text Generation**
- Run inference via CLI or HTTP
- Per-request metrics: generation latency, tokens per second (throughput) , input/output token counts

**Benchmarking**
- Execute structured benchmark runs against any configured model
- Collect generation latency (decode loop), throughput, and token-level statistics
- Percentile breakdown: mean, p50, p95, p99, min, max

**Experiment Tracking**
- Auto-save benchmark runs as timestamped JSON artifacts
- Load and inspect historical reports
- Side-by-side comparison across runs or models

**REST API**
- FastAPI serving layer with typed request/response schemas
- Model management and inference endpoints
- Swagger UI at `/docs`

**Observability**
- Structured logging to `artifacts/logs/`
- Reproducible benchmark artifacts with full run metadata
- Configuration-driven — all behavior controlled from a single YAML file

---

## Architecture

Parallax follows a layered architecture that separates interfaces, business logic, model execution, and artifact persistence.

Key design principles:

- Shared service layer across CLI and FastAPI — business logic is implemented once
- Separated concerns — inference, benchmarking, and tracking are independent modules
- Configuration-driven model management — models and behavior defined in `config/settings.yaml`
- Structured logging and artifact persistence — all runs are traceable and reproducible

![Architecture](docs/images/architecture.png)

For a detailed breakdown of each layer and component, see [`docs/architecture.md`](docs/architecture.md).

---

## Installation

**Requirements:** Python 3.9+

```bash
git clone https://github.com/Shagun812/parallax.git
cd parallax

python -m venv .venv
source .venv/bin/activate       # Linux / macOS / WSL
# .venv\Scripts\activate        # Windows

# For runtime dependencies
pip install -e .

# For runtime dependencies + testing tools
pip install -e ".[dev]"
```

---

## Configuration

Parallax is configuration-driven. All models, inference parameters, benchmark settings, and logging behavior are controlled from a single file:

```
config/settings.yaml
```

**Example configuration:**

```yaml
project:
  name: parallax
  artifacts_dir: "./artifacts"

models:
  qwen-small:
    path: "Qwen/Qwen2.5-0.5B-Instruct"
    type: "causal_lm"
  smollm2:
    path: "HuggingFaceTB/SmolLM2-360M-Instruct"
    type: "causal_lm"

inference:
  default_model: "qwen-small"
  device: "auto"
  max_new_tokens: 126
  do_sample: true
  temperature: 0.4
  top_p: 0.9
  repetition_penalty: 1.15

benchmark:
  prompt_file: data/prompts.json
  runs_per_model: 3
  warmup_runs: 1
  collect_latency: true
  collect_memory: true
  collect_throughput: true

quality:
  enabled: false
  method: "semantic_similarity"
  embedding_model: "all-MiniLM-L6-v2"
  collect_coherence_score: true

logging:
  enabled: true
  level: "INFO"
```

**Configuration reference:**

| Section | Key | Description |
|---|---|---|
| `project` | `artifacts_dir` | Root directory for all runtime artifacts |
| `models` | `path` | HuggingFace model identifier |
| `models` | `type` | Model class — currently `causal_lm` |
| `inference` | `default_model` | Model loaded on startup |
| `inference` | `device` | `auto`, `cuda`, or `cpu` |
| `inference` | `max_new_tokens` | Maximum decode tokens per request |
| `inference` | `temperature` | Sampling temperature |
| `inference` | `top_p` | Nucleus sampling threshold |
| `inference` | `repetition_penalty` | Penalizes token repetition |
| `benchmark` | `prompt_file` | Path to benchmark prompt dataset |
| `benchmark` | `runs_per_model` | Benchmark iterations per run |
| `benchmark` | `warmup_runs` | Warmup iterations excluded from metrics |
| `quality` | `enabled` | Enable semantic quality scoring (v2) |
| `logging` | `level` | Log verbosity — `INFO`, `DEBUG`, `WARNING` |

---

## Usage

### CLI

**Model management**

```bash
# List all configured models
parallax models list

# Show the currently active model
parallax models current

# Switch active model
parallax models switch --model smollm2
```

**Text generation**

```bash
parallax generate --prompt "Explain attention mechanisms"
```

Output includes: generated text, input tokens, output tokens, generation latency (ms), tokens/sec.

**Benchmarking**

```bash
parallax benchmark run
```

Runs a structured benchmark workload against the active model using prompts from `data/prompts.json`. Results are automatically saved to `artifacts/benchmarks/`.

**Experiment tracking**

```bash
# List all saved benchmark reports
parallax experiments list

# Inspect a specific report
parallax experiments show --file <filename>

# Compare two runs side by side
parallax experiments compare --file-a <file1> --file-b <file2>
```

---

### REST API

Start the server:

```bash
uvicorn api.app:app --reload
```

Swagger UI: `http://127.0.0.1:8000/docs`

**Endpoints**

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/models` | List available models |
| `GET` | `/models/current` | Show active model |
| `POST` | `/models/switch` | Switch active model |
| `POST` | `/generate` | Run inference |

**Example requests**

```bash
# Generate text
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain attention mechanisms"}'

# Switch model
curl -X POST http://127.0.0.1:8000/models/switch \
  -H "Content-Type: application/json" \
  -d '{"model_name": "smollm2"}'
```

---

## Runtime Artifacts

Parallax generates artifacts at runtime. These are excluded from version control via `.gitignore` and created automatically on first use.

```
artifacts/
├── benchmarks/
│   ├── benchmark_2026-06-23_18-20-01.json
│   └── benchmark_2026-06-23_18-45-17.json
└── logs/
    └── parallax.log
```

Benchmark artifacts contain full run metadata: model name, timestamp, latency distributions, throughput metrics, and token statistics. Logs are written in structured format for traceability.

---

## Project Structure

```
parallax/
├── api/
│   ├── app.py
│   └── schemas.py
├── benchmark/
│   ├── comparator.py
│   ├── metrics.py
│   └── runner.py
├── cli/
│   └── main.py
├── config/
│   └── settings.yaml
├── inference/
│   ├── generator.py
│   └── loader.py
├── services/
│   ├── benchmark.py
│   ├── export.py
│   ├── inference.py
│   └── serving.py
├── tracking/
│   ├── report.py
│   └── writer.py
├── utils/
│   ├── loader.py
│   └── logger.py
├── tests/
├── data/
│   └── prompts.json
├── artifacts/          # Generated at runtime — gitignored
└── docs/
    ├── architecture.md
    └── images/
        └── architecture.png
```

---

## Benchmarks & Experiment Tracking

Benchmark runs are executed via the CLI and persisted as structured JSON artifacts. Each report captures:

- Model name and configuration
- Prompt count and runs per prompt
- Generation latency — mean, p50, p95, p99, min, max
- Mean tokens per second
- Average input and output token counts

**What is measured:** Generation latency covers the full `model.generate()` decode loop — all forward passes, KV cache operations, and sampling. A CUDA synchronization point is placed after generation and before the timer stop to ensure GPU execution is fully complete before measurement is taken.

**What is not measured:** Time to first token (TTFT), tokenization time, and end-to-end request latency are not currently captured. These are planned for v2.

For full benchmark results across models, methodology, and reproduction steps, see [`docs/benchmarks.md`](docs/benchmarks.md).

---

## Testing

Run the complete test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

Test coverage includes the inference layer, benchmark engine, service layer, CLI commands, and experiment tracking.

---

## Supported Models

Parallax currently ships with:

- Qwen2.5-0.5B-Instruct
- SmolLM2-360M-Instruct

Additional Hugging Face causal language models can be added through configuration.

---

## V1 Scope & Limitations

Parallax v1 is intentionally scoped to local single-user experimentation.

- Single active model at a time
- No async inference or request queuing
- No distributed or multi-GPU execution
- No dashboard or UI — CLI and HTTP only
- Benchmarking and experiment tracking available via CLI only
- Artifact storage is local filesystem only
- Quality scoring is implemented in configuration but disabled pending v2 evaluation pipeline

---

## V2 Roadmap

| Area | Planned Work |
|---|---|
| Inference | Async serving, request queues |
| Evaluation | Quality scoring pipeline, semantic similarity, coherence metrics |
| Observability | Advanced monitoring, metrics dashboard |
| Deployment | Docker containerization, simplified environment setup |

---

## License

MIT — see [`LICENSE`](LICENSE) for details.