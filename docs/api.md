# API Reference

This page documents the main public API of SolverArena.

---

## run_models

```python
def run_models(mps_files: List[str], solvers: Dict[str, Dict], output_dir: str = "results") -> List[Dict]:
```

Runs a set of solvers on given MPS files and records the results.

**Parameters:**
- `mps_files` (`List[str]`): List of paths to MPS files representing optimization models.
- `solvers` (`Dict[str, Dict]`): Dictionary where keys are execution aliases and values are dictionaries containing at least `'solver_name'` and optionally other solver parameters.
- `output_dir` (`str`, optional): Directory where the result CSV will be saved. Defaults to `"results"`.

**Returns:**
- `List[Dict]`: List of dictionaries with results for each model-solver pair.

**Raises:**
- `InputValidationError`: If the input parameters fail validation.
- `IOError`: If there's an error writing the results file.
- `Exception`: For other unexpected errors during execution.

**Example:**
```python
results = run_models(["model.mps"], {"cbc": {"solver_name": "cbc"}})
```

---

## get_available_solvers

```python
def get_available_solvers() -> List[str]:
```

Returns a list of names of all available/supported solvers based on configuration.

**Returns:**
- `List[str]`: List of solver names (e.g., `["highs", "cbc", "gurobi", ...]`).

**Example:**
```python
from solverarena import get_available_solvers
print(get_available_solvers())
```

---

## Error Handling

### InputValidationError
Raised when input parameters to `run_models` are invalid.

---

## See Also
- [Getting Started](getting_started.md)
- [Examples](examples.md)
- [Changelog](changelog.md)
