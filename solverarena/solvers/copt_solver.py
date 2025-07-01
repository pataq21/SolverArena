from datetime import datetime
import coptpy
import logging

from solverarena.models import SolverResult
from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance
from typing import Dict, Any, Optional


class CoptSolver(Solver):
    """
    CoptSolver is a class that interfaces with the Cardinal Optimizer (COPT) solver.

    Attributes:
        result (dict): Stores the results of the optimization run.
    """

    def __init__(self):
        """
        Initializes the solver with an empty result.
        """
        self.result = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def solve(self, mps_file: str, params: Optional[Dict[str, Any]] = None):
        """
        Solves the optimization problem using the COPT solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            params (dict, optional): A dictionary of solver options to configure COPT.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """
        env = coptpy.Envr()

        model = env.createModel('')
        model.read(mps_file)
        if params:
            for key, value in params.items():
                try:
                    model.setParam(key, value)
                except Exception as e:
                    raise ValueError(f"Invalid parameter {key}: {e}")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"[{current_time}] Running the COPT solver on {mps_file}...")

        @track_performance
        def _run_optimization(m):
            m.solve()

        performance_data, solver_outcome = _run_optimization(model)
        status_map = {
            coptpy.COPT.OPTIMAL: "optimal",
            coptpy.COPT.INFEASIBLE: "infeasible",
            coptpy.COPT.UNBOUNDED: "unbounded",
            coptpy.COPT.TIMEOUT: "timeout",
            coptpy.COPT.INTERRUPTED: "stopped",
        }
        status_code = model.status
        status_str = status_map.get(status_code, f"UNKNOWN_STATUS_{status_code}")
        obj_value = None
        if model.hasmipsol:
            obj_value = model.objval
        result_data = {
            "status": status_str,
            "objective_value": obj_value,
            "solver": "copt",
            **performance_data
        }
        self.result = SolverResult(**result_data)

        self.logger.info(f"Solver completed with status: {self.result.status}.")

    def get_results(self):
        """
        Returns the result of the last solver run.

        Returns:
            dict: A dictionary containing the results of the solver run.
        """
        if self.result is None:
            self.logger.warning("No problem has been solved yet. The result is empty.")
            return SolverResult(error="Solve method not called.", solver="copt")
        return self.result
