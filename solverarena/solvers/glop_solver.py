from datetime import datetime
import logging

from ortools.linear_solver.python import model_builder

from solverarena.models import SolverResult
from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance
from typing import Dict, Any, Optional
from ortools.linear_solver.python.model_builder import SolveStatus


class GLOPSolver(Solver):
    def __init__(self):
        """
        Initializes the solver with an empty result.
        """
        self.result = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def solve(self, mps_file, params: Optional[Dict[str, Any]] = None):
        """
        Solves the optimization problem using the GLOP solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            params (dict, optional): A dictionary of solver options to configure GLOP.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """
        model = model_builder.ModelBuilder()
        model.import_from_mps_file(mps_file)
        glop = model_builder.ModelSolver('GLOP')

        if params:
            for key, value in params.items():
                if key == 'time_limit':
                    glop.set_time_limit_in_seconds(value)
                else:
                    self.logger.info(f"Parameter {key} is not implemented or it does not exist")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"[{current_time}] Running the GLOP solver on {mps_file}...")

        @track_performance
        def _run_optimization(solver, model_instance):
            return solver.solve(model_instance)

        performance_data, status_code = _run_optimization(glop, model)
        status_str = self._translate_status(status_code)
        obj_value = None
        if status_str == "optimal":
            obj_value = glop.objective_value

        result_data = {
            "status": status_str,
            "objective_value": obj_value,
            "solver": "GLOP",
            **performance_data
        }
        self.result = SolverResult(**result_data)
        self.logger.info(f"Solver completed with status: {status_str}.")

    def get_results(self):
        """
        Returns the result of the last solver run.

        Returns:
            dict: A dictionary containing the results of the solver run.
        """
        if self.result is None:
            self.logger.warning("No problem has been solved yet. The result is empty.")
            return SolverResult(error="Solve method not called.", solver="GLOP")
        return self.result

    def _translate_status(self, native_status: SolveStatus) -> str:
        """Translates OR-Tools native status to a standard status string."""
        status_map = {
            SolveStatus.OPTIMAL: "optimal",
            SolveStatus.FEASIBLE: "feasible",
            SolveStatus.INFEASIBLE: "infeasible",
            SolveStatus.UNBOUNDED: "unbounded",
            SolveStatus.ABNORMAL: "error",
            SolveStatus.NOT_SOLVED: "not_solved",
        }

        status = status_map.get(native_status, "unknown")

        if status == "not_solved":
            return "limit_reached"

        return status
