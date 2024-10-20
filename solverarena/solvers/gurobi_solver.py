from datetime import datetime
import gurobipy as gp
import logging

from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance


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

    @track_performance
    def run_gurobi(self, model):
        """
        Runs the Gurobi solver and tracks performance using the track_performance decorator.

        Args:
            model (gurobipy.Model): The Gurobi model instance.

        Returns:
            dict: A dictionary containing the solver status and objective value.
        """
        model.optimize()  # Execute the solver
        if model.status == gp.GRB.OPTIMAL:
            model_status = "OPTIMAL"
        obj_value = model.objVal

        return {
            "status": model_status,
            "objective_value": obj_value,
            "solver": "gurobi"
        }

    def solve(self, mps_file, options=None):
        """
        Solves the optimization problem using the Gurobi solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            options (dict, optional): A dictionary of solver options to configure Gurobi.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """
        with gp.Env(empty=True) as env:
            env.setParam('OutputFlag', 0)  # Suppress output
            env.start()  # Start the Gurobi environment

            # Read the model into the environment
            with gp.read(mps_file, env) as model:
                if options:
                    for key, value in options.items():
                        model.setParam(key, value)
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.logger.info(f"[{current_time}] Running the Gurobi solver on {mps_file}...")

                self.result = self.run_gurobi(model)

                self.logger.info(f"Solver completed with status: {self.result['status']}.")

    def get_results(self):
        """
        Returns the result of the last solver run.

        Returns:
            dict: A dictionary containing the results of the solver run.
        """
        if self.result is None:
            self.logger.warning("No problem has been solved yet. The result is empty.")
        return self.result
