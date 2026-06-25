# Architecture

##  Overview

Parallax is a local AI experimentation platform focused on model serving, benchmarking, and experiment management.

The system is designed around a small set of architectural goals:

* Separate business workflows from user interfaces
* Keep system behavior configuration-driven
* Support both CLI and API access through shared workflows
* Treat benchmarking as a first-class capability
* Maintain a local-first, dependency-light architecture

---
## Architectural Style

Parallax follows a layered architecture in which interfaces, workflow coordination, execution, and persistence are separated into distinct concerns. Dependencies flow inward toward application services, allowing multiple interfaces to share the same workflows while keeping core system behavior independent of how the platform is accessed.

---

##  Architectural Principles

### Centralized Workflow Coordination

Services act as the central coordination layer for all application workflows.

Interfaces invoke services, while engines perform execution. This keeps business logic isolated from user-facing entrypoints.

### Configuration Over Code

Operational behavior should be controlled through configuration rather than source code modifications.

Models, inference settings, benchmark parameters, logging behavior, and storage locations are defined externally.

### Local-First Execution

Models execute on local hardware and artifacts remain locally accessible.

This removes external dependencies and ensures benchmark reproducibility.

### Explicit Resource Management

Large language models are expensive runtime resources.

Model lifecycle, memory consumption, and device allocation are managed explicitly rather than implicitly.


---

##  Architecture Diagram

![Architecture](architecture.png)


---

## Architectural Boundaries

Parallax separates user interaction, workflow orchestration, execution, and persistence into distinct architectural boundaries.

The following dependency rules apply:

- Interfaces may only communicate with services.
- Services coordinate workflows and own application behavior.
- Execution systems perform computation but do not handle user interaction.
- Persistence manages artifacts, logs, and configuration without knowledge of application workflows.

---

##  Request Flows

### Text Generation

```text
 CLI / API
      ↓
Generation Service
      ↓
Model Resolution
      ↓
Inference Execution
      ↓
Response + Runtime Metrics
```

A generation request is validated by the interface layer, coordinated by the service layer, executed by the inference engine, and returned together with runtime metrics.

### Benchmark Execution

```text
     CLI
      ↓
Benchmark Service
      ↓
Benchmark Workload
      ↓
Inference Execution
      ↓
Metrics Aggregation
      ↓
Artifact Persistence
      ↓
Benchmark Report
```

Benchmark execution repeatedly invokes the inference engine, aggregates performance measurements, and persists the resulting report as a structured artifact.

---

##  State Management

Parallax maintains a single active model at any given time.

```text
Model Requested
        ↓
Already Active?
    ↙       ↘
 Yes        No
  ↓          ↓
Reuse     Load Model
  ↓          ↓
Generate  Set Active Model
        ↓
     Generate
```

This approach keeps memory usage predictable and avoids repeated model initialization costs.

Model state is managed centrally and shared across application workflows.

---
## Device Resolution

Parallax abstracts the underlying compute device through automatic device selection.
```
device: "auto"
    ↓
CUDA available? → load on GPU
    ↓
No CUDA → fall back to CPU
```
This allows workflows to remain independent of the underlying compute environment while supporting heterogeneous hardware.

---

##  Configuration-Driven Design

All operational behavior is controlled through:

```text
config/settings.yaml
```

Configuration governs:

* Available models
* Active model selection
* Device preferences
* Generation parameters
* Benchmark settings
* Logging behavior
* Artifact locations

Configuration serves as the operational contract of the platform, allowing system behavior to evolve without architectural changes. It also governs operational observability, including structured logging behavior across application workflows.

---

##  Architectural Tradeoffs

### Service Layer vs Direct Execution

Introducing a service layer adds indirection but prevents workflow duplication across interfaces.

The architecture favors maintainability and extensibility over minimal code paths.

### Local Artifacts vs Database Storage

Benchmark reports are stored as structured files rather than database records.

This simplifies deployment and keeps artifacts directly inspectable, at the cost of advanced querying capabilities.

### Single Active Model vs Multi-Model Loading

Maintaining a single active model reduces memory pressure and simplifies lifecycle management.

The tradeoff is that switching models incurs reload latency.

### Configuration-Driven Behavior vs Hardcoded Defaults

External configuration increases flexibility and adaptability.

The tradeoff is additional configuration management complexity.

---

##  Architectural Constraints

The following constraints are intentional design decisions:

* Application workflows must remain independent of interfaces
* CLI and API must share the same application workflows
* Only one model may be active at a time
* System behavior must be configurable without code changes
* Benchmark artifacts must be reproducible and inspectable
* Models execute locally rather than through remote inference providers
* Artifact persistence remains filesystem-based in v1
* All application workflows must emit structured logs through a centralized logging system.

These constraints guide implementation decisions throughout the system.

---

## Benchmarking as a First-Class Workflow

Parallax treats benchmarking as an independent workflow rather than an external utility.

Benchmark execution, metric aggregation, artifact persistence, and experiment comparison are modeled as dedicated system capabilities with their own services and execution paths. Benchmarking depends on inference execution but is not implemented within the inference subsystem. The two workflows remain architecturally independent and evolve separately.

---

##  Future Evolution

The architecture intentionally leaves room for future capabilities without requiring structural redesign.

Potential extensions include:

* Asynchronous inference execution
* Multi-model serving
* Evaluation pipelines
* Quality evaluation pipelines
* Advanced observability

These features can be introduced by extending existing components while preserving the current architectural boundaries.

---