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
from arenasolver.run import run_models

# Define the list of MPS files and solvers
mps_files = ['path/to/model1.mps', 'path/to/model2.mps']
solvers = ['solver1', 'solver2']
parameters = {
    "solver1": {
        "presolve": "on",
        "pdlp_native_termination": True,
        "solver": "pdlp",
    },
}

# Run the models
results = run_models(mps_files, solvers, parameters)
print(results)
```