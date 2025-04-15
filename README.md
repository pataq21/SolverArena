# Solver Arena

**Solver Arena** is an open-source library designed to facilitate the performance comparison of different solvers in optimization problems. The library abstracts the implementation of solvers, allowing users to input a list of MPS files and choose the desired solvers with their respective parameters.

## Installation

To install the library from PyPI, you can use `pipenv` with one of the following commands:

1. **Basic Installation** (only the main library):

    ```bash
    pipenv install solverarena
    ```

2. **Installation with a Specific Solver**:

    If you want to install the library along with a specific solver, you can use:

    ```bash
    pipenv install solverarena[highs]      # To install with Highs
    pipenv install solverarena[gurobi]     # To install with Gurobi
    pipenv install solverarena[scip]       # To install with SCIP
    pipenv install solverarena[ortools]    # To install with OR-Tools
    ```

3. **Installation with All Solvers**:

    If you want to install the library along with all available solvers, use:

    ```bash
    pipenv install solverarena[all_solvers]
    ```

## Usage

To use the library, you can refer to the example folder, which contains a basic implementation. Here is an example of how to use `arena_solver`:

```python
from solverarena import run_models

if __name__ == "__main__":
    mps_files = [
        "examples/mps_files/model_dataset100.mps",
    ]

    solvers = {
        "highs_default": {
            "solver_name": "highs",
            "presolve": "on",
            "time_limit": 3600,
            "solver": "ipm"
        },
        "highs_no_presolve": {
            "solver_name": "highs",
            "presolve": "off",
            "time_limit": 1800,
            "solver": "simplex"
        }
    }

    results = run_models(mps_files, solvers)
```