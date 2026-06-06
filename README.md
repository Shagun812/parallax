# Parallax
*Parallax is a local LLM experimentation and serving platform designed for model comparison, benchmarking, evaluation, and lightweight inference workflows.*
*The project aims to provide a consistent interface for running multiple language models locally while collecting performance metrics and maintaining reproducible experiment configurations.*

# Installation

**Clone the repository:**

```bash 
git clone https://github.com/Shagun812/parallax
cd parallax
```

**Create a virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Install the dependancies:**
```bash
python -m pip install -e .
```
**CLI Commands**

List available models:
```bash
parallax models list
```
Show current model:
```bash
parallax models current
```
Switch model:
```bash
parallax models switch <model-name>
```
Generate text:
```bash
parallax generate --prompt "What is artificial intelligence?"
```

# Project Goals

Parallax is intended to evolve into a platform for:

Local LLM experimentation  
Model benchmarking  
Evaluation workflows  
Reproducible inference  
Lightweight serving  

  The architecture emphasizes clear separation between configuration, inference, serving, and experiment management.
