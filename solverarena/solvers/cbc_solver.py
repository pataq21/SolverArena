import logging
import os
import re
import subprocess
from datetime import datetime

from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance


class CBCSolver(Solver):
    """
    CBCSolver executes CBC directly via subprocess on an MPS file.
    """

    def __init__(self):
        self.result = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    @track_performance
    def run_cbc(self, mps_file_path: str) -> dict[str, any]:
        """
        Solves a given MPS file using the CBC solver via subprocess and parses stdout.

        Args:
            mps_file_path (str): The path to the MPS model file.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - "status": Solver status ('optimal', 'infeasible', 'unbounded',
                                        'error', 'unknown').
                - "objective_value": The final objective function value (float) if found,
                                    otherwise None.
                - "error_message": A description of the error if status is 'error',
                                otherwise None.
                - "raw_output": The full stdout from the solver for debugging.
        """
        # 1. Check if the MPS file exists
        if not os.path.isfile(mps_file_path):
            logging.error(f"Error: MPS file not found at '{mps_file_path}'")
            return {
                "status": "error",
                "objective_value": None,
                "error_message": f"MPS file not found: {mps_file_path}",
                "raw_output": None,
            }

        # 2. Construct the command

        command = ["cbc", mps_file_path, "solve"]

        # 3. Run the solver using subprocess
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            stdout = result.stdout

        except FileNotFoundError:
            logging.error("Error: CBC executable 'cbc' not found.")
            logging.error("Please ensure CBC is installed and in your system PATH")
            return {
                "status": "error",
                "objective_value": None,
                "error_message": "CBC executable not found: cbc",
                "raw_output": None,
            }

        except Exception as e:
            logging.error(f"An unexpected error occurred running subprocess: {e}")
            return {
                "status": "error",
                "objective_value": None,
                "error_message": f"Subprocess execution failed: {e}",
                "raw_output": None,
            }

        # 4. Parse the stdout to find status and objective value
        solver_status = "unknown"
        objective_value = None
        error_msg_from_output = None

        # Common patterns in CBC output:
        status_patterns = {
            "optimal": r"Result - Optimal solution found",
            "infeasible": r"Result - Problem proven infeasible",
            "unbounded": r"Result - Problem proven unbounded",
        }
        # Objective value pattern (handles integer and floating point)
        objective_pattern = r"Objective value:\s+(-?\d+(\.\d+)?)"

        for line in stdout.splitlines():
            # Check for status
            for status_key, pattern in status_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    solver_status = status_key
                    break

            # Check for objective value (only if status is potentially optimal/feasible)
            match = re.search(objective_pattern, line, re.IGNORECASE)
            if match:
                try:
                    objective_value = float(match.group(1))
                    # Keep searching in case CBC prints it multiple times (e.g., during search)
                    # The last one found is usually the final one.
                except (ValueError, IndexError):
                    logging.warning(
                        f"Could not parse objective value from line: {line}"
                    )

        # Handle cases where CBC exited non-zero but we parsed a status
        if result.returncode != 0 and solver_status not in ["infeasible", "unbounded"]:
            if solver_status == "unknown":
                solver_status = "error"
                error_msg_from_output = f"CBC process exited with code {result.returncode}. Output may be incomplete."
                logging.error(error_msg_from_output)

        return {
            "status": solver_status,
            "objective_value": objective_value,
        }

    def solve(self, mps_file, options=None):
        if not os.path.exists(mps_file):
            raise FileNotFoundError(f"File {mps_file} not found.")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"[{current_time}] Running CBC on {mps_file}...")

        self.result = self.run_cbc(mps_file)

    def get_results(self):
        if self.result is None:
            self.logger.warning("No problem has been solved yet.")
        return self.result
