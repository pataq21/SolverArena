from datetime import datetime
import gurobipy as gp
import logging

from solverarena.models import SolverResult
from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance
from typing import Dict, Any, Optional


class GurobiSolver(Solver):
    """
    GurobiSolver is a class that interfaces with the Gurobi optimization solver.

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
        Solves the optimization problem using the Gurobi solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            params (dict, optional): A dictionary of solver options to configure Gurobi.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """
        with gp.Env(empty=True) as env:
            env.start()  # Start the Gurobi environment

            # Read the model into the environment
            with gp.read(mps_file, env) as model:
                if params:
                    for key, value in params.items():
                        model.setParam(key, value)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.logger.info(f"[{current_time}] Running the Gurobi solver on {mps_file}...")

                @track_performance
                def _run_optimization(m):
                    m.optimize()
                performance_data, solver_outcome = _run_optimization(model)
                status_map = {
                    gp.GRB.OPTIMAL: "OPTIMAL",
                    gp.GRB.INFEASIBLE: "INFEASIBLE",
                    gp.GRB.UNBOUNDED: "UNBOUNDED",
                    gp.GRB.TIME_LIMIT: "TIME_LIMIT_REACHED",
                }
                status = status_map.get(model.status, f"UNKNOWN_STATUS_{model.status}")
                obj_val = None
                if model.solCount > 0:
                    try:
                        obj_val = model.objVal
                    except gp.GurobiError:
                        self.logger.warning("Could not retrieve objective value.")

                result_data = {
                    "status": status,
                    "objective_value": obj_val,
                    "solver": "gurobi",
                    **performance_data
                }
                self.result = SolverResult(**result_data)
                self.logger.info(f"Solver completed with status: {self.result.status}.")

    def get_results(self) -> Optional[SolverResult]:
        if self.result is None:
            self.logger.warning("No result available. Call the solve() method first.")
            return SolverResult(error="Solve method not called.", solver="gurobi")
        return self.result
