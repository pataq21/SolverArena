# Getting Started

Welcome to **SolverArena**! This guide will help you install the library, set up your environment, and run your first optimization benchmark.

---

## Installation

SolverArena requires Python 3.12 or higher.

Install the core package with pip:

```bash
pip install solverarena
```

To use specific solvers, install the corresponding extras. For example, to use HiGHS and Gurobi:

```bash
pip install solverarena[highs]
pip install solverarena[gurobi]
```

Or install all supported solvers and development tools:

```bash
pip install solverarena[all_solvers,dev]
```

> **Note:** Some solvers (like Gurobi or COPT) may require a license and additional setup. Please refer to their documentation.

---

## Preparing Your Models

SolverArena works with models in **MPS format**. Place your `.mps` files in a directory, for example: `examples/mps_files/model1.mps`.

---

## Running Your First Benchmark

Here's a minimal example to run two solvers on a model:

```python
from solverarena import run_models

mps_files = ["examples/mps_files/model1.mps"]
solvers = {
    "highs_default": {"solver_name": "highs"},
    "cbc_default": {"solver_name": "cbc"}
}

results = run_models(mps_files, solvers)
print(results)
```

This will run both solvers on the model and print the results.

---

## Checking Available Solvers

You can list all solvers supported by SolverArena:

```python
from solverarena import get_available_solvers

print(get_available_solvers())
```

---

## Next Steps

- Check the [Examples](examples.md) for more advanced usage.
- Visit the [Repository](https://github.com/pataq21/SolverArena) for source code and issue tracking.

---
