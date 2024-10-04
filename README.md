# Arena Solver

**Arena Solver** is an open-source library designed to facilitate the performance comparison of different solvers in optimization problems. The library abstracts the implementation of solvers, allowing users to input a list of MPS files and choose the desired solvers with their respective parameters.

## Installation

For now, the library is available on GitHub. To install it, clone the repository and use Pipenv:

```bash
git clone https://github.com/your_username/arene_solver.git
cd arena_solver
pipenv install
```
## Usage
To use the library, you can refer to the example folder, which contains a basic implementation. Here is an example of how to use arena_solver:
```python
from arena_solver import run_models

# Define the list of MPS files and solvers
mps_files = ['path/to/model1.mps', 'path/to/model2.mps']
solvers = ['solver1', 'solver2']

# Run the models
results = run_models(mps_files, solvers)
print(results)
```

## Main Functions
run_models: Executes multiple solvers on MPS files and logs performance results.

## Dependencies
The library depends on the following libraries:

memory_profiler
HiGHS
You can install these dependencies using Pipenv.

## Contributions
Contributions are welcome. If you would like to contribute, please open an issue or a pull request on the GitHub repository.

## License
This library is licensed under the MIT License.