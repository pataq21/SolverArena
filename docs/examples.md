# Examples

Here are some practical examples to help you get started with SolverArena.

---

## 1. Run Multiple Solvers on a Single Model

```python
from solverarena import run_models

mps_files = ["examples/mps_files/model_dataset100.mps"]
solvers = {
    "highs_default": {"solver_name": "highs"},
    "cbc_default": {"solver_name": "cbc"}
}

results = run_models(mps_files, solvers)
print(results)
```

---

## 2. Run a Solver with Custom Parameters

```python
from solverarena import run_models

mps_files = ["examples/mps_files/model.mps"]
solvers = {
    "highs_ipm": {"solver_name": "highs", "solver": "ipm", "time_limit": 600},
    "highs_simplex": {"solver_name": "highs", "solver": "simplex", "presolve": "off"}
}

results = run_models(mps_files, solvers)
for res in results:
    print(f"{res['execution_alias']}: status={res['status']}, obj={res['objective_value']}")
```

---

## 3. List Available Solvers

```python
from solverarena import get_available_solvers

print("Available solvers:", get_available_solvers())
```

---

## 4. Export Results to CSV

By default, `run_models` will export results to a timestamped CSV file in the `results/` directory. You can specify a custom output directory:

```python
from solverarena import run_models

mps_files = ["examples/mps_files/model_dataset100.mps"]
solvers = {"highs_default": {"solver_name": "highs"}}

results = run_models(mps_files, solvers, output_dir="my_results")
```

---

For more advanced usage, see the [API Reference](api.md) or check the [Getting Started](getting_started.md) guide.
