from datetime import datetime
import pyscipopt as scip
import logging
from solverarena.models import SolverResult
from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance
from typing import Dict, Any, Optional


class SCIPSolver(Solver):
    """
    SCIPSolver is a class that interfaces with the SCIP optimization solver using PySCIPOpt.

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

    def solve(self, mps_file, params: Optional[Dict[str, Any]] = None):
        """
        Solves the optimization problem using the SCIP solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            params (dict, optional): A dictionary of solver options to configure SCIP.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """

        try:
            model = scip.Model()
            model.readProblem(mps_file)
            # Apply solver options if any
            if params:
                for key, value in params.items():
                    model.setParam(key, value)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info(f"[{current_time}] Running the SCIP solver on {mps_file}...")

            @track_performance
            def _run_optimization(m):
                m.optimize()

            performance_data, _ = _run_optimization(model)
            native_status = model.getStatus()
            status_str = self._translate_status(native_status)

            obj_value = None
            if model.getNSols() > 0:
                try:
                    obj_value = model.getObjVal()
                except scip.Exception:
                    self.logger.warning("SCIP reported a solution but getObjVal() failed.")

            result_data = {
                "status": status_str,
                "objective_value": obj_value,
                "solver": "scip",
                **performance_data
            }
            self.result = SolverResult(**result_data)
            self.logger.info(f"Solver completed with status: {self.result.status}.")

        except FileNotFoundError:
            self.logger.error(f"File {mps_file} not found.")
            raise

    def get_results(self):
        """
        Returns the result of the last solver run.

        Returns:
            dict: A dictionary containing the results of the solver run.
        """
        if self.result is None:
            self.logger.warning("No problem has been solved yet. The result is empty.")
            return SolverResult(error="Solve method not called.", solver="scip")

        return self.result

    def _translate_status(self, native_status: str) -> str:
        """Translates SCIP's string status to a standard status."""
        status_map = {
            "optimal": "optimal",
            "infeasible": "infeasible",
            "unbounded": "unbounded",
            "timelimit": "limit_reached",
            "memlimit": "limit_reached",
            "nodelimit": "limit_reached",
            "sollimit": "limit_reached",
            "userinterrupt": "stopped",
        }
        return status_map.get(native_status, native_status)
