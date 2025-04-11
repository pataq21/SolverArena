import csv
import logging
import os
from datetime import datetime
from typing import Dict, List

from solverarena.solvers.solver_factory import SolverFactory

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CSV_FIELDNAMES = [
    "execution_alias",
    "model",
    "solver",
    "status",
    "objective_value",
    "runtime",
    "memory_used_MB",
    "error",
]
def run_models(
    mps_files: List[str], solvers: Dict[str, Dict], output_dir: str = "results"
) -> List[Dict]:
    """
    Runs a set of solvers on given MPS files and records the results.

    Args:
        mps_files (list): A list of paths to MPS files representing optimization models.
        solvers: A dictionary where keys are execution aliases and values are
                 dictionaries containing at least 'solver_name' and optionally
                 other solver parameters.
        output_dir (str, optional): Directory where the result CSV will be saved. Defaults to "results".

    Returns:
        list: A list of dictionaries with results for each model-solver pair.

    Raises:
        FileNotFoundError: If any MPS file does not exist.
        ValueError: If an unsupported solver is provided.

    """
    for mps_file in mps_files:
        if not os.path.isfile(mps_file):
            logger.error(f"Input MPS file not found: {mps_file}")
            raise FileNotFoundError(f"MPS file not found: {mps_file}")
        
    for alias, params in solvers.items():
        if not isinstance(params, dict) or "solver_name" not in params:
            logger.error(f"Invalid configuration for alias '{alias}'. Must be a dict with 'solver_name'.")
            raise ValueError(f"Invalid configuration for alias '{alias}'. Missing 'solver_name'.")

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"results_{timestamp}.csv")
    logger.info(f"Results will be saved to: {output_file}")

    results = []
    try:
        with open(output_file, mode="w", newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            for execution_alias, parameters in solvers.items():
                solver_name = parameters["solver_name"]
                logger.info(f"--- Running Alias: {execution_alias} (Solver: {solver_name}) ---")
                for mps_file in mps_files:
                    model_name = os.path.basename(mps_file)
                    logger.info(f"Processing model: {model_name}")
                    result = run_solver_on_model(mps_file, execution_alias, parameters)
                    results.append(result)
                    row_to_write = {key: result.get(key) for key in CSV_FIELDNAMES}
                    writer.writerow(row_to_write)


    except IOError as e:
        logger.error(f"Error writing results to CSV file {output_file}: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during the run: {e}")
        raise

    logger.info(f"Finished processing all models. Results saved to {output_file}")
    return results

def run_solver_on_model(
    mps_file: str, execution_alias: str, parameters: Dict[str, Dict]
) -> Dict:
    """Runs a solver on a given model and handles errors."""

    solver_name = parameters["solver_name"]
    model_name = os.path.basename(mps_file)
    result_base = {
        "execution_alias": execution_alias,
        "model": model_name,
        "solver": solver_name,
        "status": "error",
        "objective_value": None,
        "runtime": None,
        "memory_used_MB": None,
        "error": "Initialization failed",
    }


    try:
        solver = SolverFactory.get_solver(solver_name)
        result_base["error"] = None

        solver_params = {k: v for k, v in parameters.items() if k != "solver_name"}
        logger.debug(f"Calling {solver_name} with params: {solver_params} for model {model_name}")

        solver.solve(mps_file, solver_params) if solver_params else solver.solve(mps_file)

        solver_results = solver.get_results()

        result = result_base.copy()
        result.update(solver_results)
        result["error"] = solver_results.get("error")

        logger.info(f"Finished {solver_name} on {model_name}. Status: {result.get('status')}, \
                    Objective: {result.get('objective_value')}")


    except Exception as e:
        error_message = f"Error running {solver_name} on {model_name}: {type(e).__name__} - {str(e)}"
        logger.error(error_message)
        result = result_base.copy()
        result["error"] = error_message

    final_result = {key: result.get(key) for key in CSV_FIELDNAMES}
    return final_result

