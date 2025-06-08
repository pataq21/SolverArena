# SolverArena

SolverArena is a Python library to **run and compare optimization models** using multiple solvers in a unified and reproducible way.

---

## Features

- Run optimization models (MPS format) with different solvers using a single interface.
- Compare solver performance (status, objective value, runtime, memory, etc.).
- Easily extendable to support new solvers.
- Export results to CSV for further analysis.
- Simple API for integration in research and benchmarking workflows.

---

## Quick Example

```python
from solverarena import run_models

mps_files = ["examples/mps_files/model_dataset100.mps"]
solvers = {
    "highs_default": {"solver_name": "highs", "presolve": "on"},
    "cbc_default": {"solver_name": "cbc"}
}

results = run_models(mps_files, solvers)
print(results)
```