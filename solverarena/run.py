from datetime import datetime
import gc
import os
import csv
import logging
from typing import List, Dict, Optional
from solverarena.solvers.solver_factory import SolverFactory

# Set up basic logging
logging.basicConfig(level=logging.INFO)


def run_models(mps_files: List[str],
               solvers: List[str],
               parameters: Optional[Dict[str, Dict]] = None,
               output_dir: str = "results") -> List[Dict]:
    """
    Runs a set of solvers on given MPS files and records the results.

    Args:
        mps_files (list): A list of paths to MPS files representing optimization models.
        solvers (list): A list of solver names (as strings) that will be used to solve the models.
        parameters (dict, optional): A dictionary where keys are solver names and values are dictionaries 
                                     of solver-specific options. If None, solvers are run with default settings.
        output_dir (str, optional): Directory where the result CSV will be saved. Defaults to "results".

    Returns:
        list: A list of dictionaries with results for each model-solver pair.

    Raises:
        FileNotFoundError: If any MPS file does not exist.
        ValueError: If an unsupported solver is provided.

    This function also saves the results to a CSV file in the `output_dir` directory.
    """
    # Check if MPS files exist
    for mps_file in mps_files:
        if not os.path.isfile(mps_file):
            raise FileNotFoundError(f"MPS file not found: {mps_file}")

    # Create timestamp and output file path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = initialize_csv(timestamp, output_dir)

    results = []
    for solver_name in solvers:
        for mps_file in mps_files:
            result = run_solver_on_model(mps_file, solver_name, parameters)
            results.append(result)
            append_to_csv(output_file, result)
            gc.collect()
    return results


def initialize_csv(timestamp: str, output_dir: str) -> str:
    """Initializes the CSV file and writes the header."""
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"results_{timestamp}.csv")

    fieldnames = [
        "model", "solver", "status", "objective_value", "runtime", "memory_used_MB", "error"
    ]

    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    return output_file


def run_solver_on_model(mps_file: str, solver_name: str, parameters: Optional[Dict[str, Dict]]) -> Dict:
    """Runs a solver on a given model and handles errors."""

    solver = SolverFactory.get_solver(solver_name)

    try:
        solver_params = parameters.get(solver_name) if parameters and solver_name in parameters else None
        solver.solve(mps_file, solver_params) if solver_params else solver.solve(mps_file)

        result = solver.get_results()
        result.update({
            "model": os.path.basename(mps_file),
            "solver": solver_name
        })

    except Exception as e:
        logging.error(f"Error when running {solver_name} on {mps_file}: {str(e)}")
        result = {
            "model": os.path.basename(mps_file),
            "solver": solver_name,
            "status": "error",
            "objective_value": None,
            "runtime": None,
            "memory_used_MB": None,
            "error": str(e),
        }

    return result


def append_to_csv(output_file: str, result: Dict) -> None:
    """Appends a result dictionary to the CSV file."""
    fieldnames = [
        "model", "solver", "status", "objective_value", "runtime", "memory_used_MB", "error"
    ]

    with open(output_file, mode="a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(result)
