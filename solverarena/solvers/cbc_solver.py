import logging
import os

from datetime import datetime

import pulp
from typing import Dict, Any, Optional

from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance

CSV_FIELDNAMES = ["execution_alias", "model", "solver", "status",
                  "objective_value", "runtime", "memory_used_MB", "error"]


class CBCSolver(Solver):
    """
    CBCSolver executes CBC directly via subprocess on an MPS file.
    """

    def __init__(self):
        self.result = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    @track_performance
    def run_cbc(self, cbc, model: pulp.LpProblem) -> dict[str, any]:
        """
        Solves a given MPS file using the CBC solver via subprocess and parses stdout.

        Args:
            cbc: cbc solver.
            model: loaded model.

        Returns:
            Dict[str, Any]: A dictionary containing:
                - "status": Solver status ('optimal', 'infeasible', 'unbounded',
                                        'error', 'unknown').
                - "objective_value": The final objective function value (float) if found,
                                    otherwise None.
        """
        solve_status_code = model.solve(cbc)

        pulp_status = pulp.LpStatus[solve_status_code]
        obj_value = pulp.value(model.objective) if pulp_status in ["Optimal", "Undefined"] else None
        status_map = {
            "Optimal": "optimal",
            "Not Solved": "error",
            "Infeasible": "infeasible",
            "Unbounded": "unbounded",
            "Undefined": "stopped",
        }
        solver_status = status_map.get(pulp_status, "unknown")

        return {
            "status": solver_status,
            "objective_value": obj_value,
            "solver": "CBC"
        }

    def solve(self, mps_file, params: Optional[Dict[str, Any]] = None):
        if not os.path.isfile(mps_file):
            self.logger.error(f"MPS file not found: {mps_file}")
            self.result = {
                "status": "error",
                "objective_value": None,
                "runtime": 0,
                "memory_used_MB": 0,
                "error": f"File not found: {mps_file}"
            }
            for key in CSV_FIELDNAMES:
                if key not in self.result:
                    self.result[key] = None
            return

        try:
            _, loaded_model = pulp.LpProblem.fromMPS(mps_file)
            self.logger.info(f"Successfully loaded {mps_file} into PuLP.")

            cbc_params = params or {}
            solver_options = []
            time_limit_sec = None
            if 'timeLimit' in cbc_params:
                time_limit_sec = float(cbc_params['timeLimit'])
                solver_options.append(f"seconds {time_limit_sec}")
            if 'gap' in cbc_params:
                solver_options.append(f"allowableGap {cbc_params['gap']}")

            solver = pulp.PULP_CBC_CMD(msg=1, options=solver_options,
                                       timeLimit=time_limit_sec)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info(f"[{current_time}] Running CBC on {mps_file}...")

            self.result = self.run_cbc(solver, loaded_model)

        except pulp.PulpError as e:
            self.logger.error(f"PuLP error solving {mps_file}: {e}")
            self.result = {key: None for key in CSV_FIELDNAMES}
            self.result["status"] = "error"
            self.result["error"] = f"PuLP Error: {str(e)}"
            self.result["solver"] = "cbc"
            self.result["model"] = os.path.basename(mps_file)
        except Exception as e:
            self.logger.error(f"Unexpected error solving {mps_file} with PuLP/CBC: {e}")
            self.result = {key: None for key in CSV_FIELDNAMES}
            self.result["status"] = "error"
            self.result["error"] = f"Unexpected Error: {type(e).__name__} - {str(e)}"
            self.result["solver"] = "cbc"
            self.result["model"] = os.path.basename(mps_file)

    def get_results(self):
        if self.result is None:
            self.logger.warning("get_results called before solve completed or after early failure.")
            return {key: None for key in CSV_FIELDNAMES}
        final_result = {key: self.result.get(key) for key in CSV_FIELDNAMES}
        return final_result
