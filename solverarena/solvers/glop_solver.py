from datetime import datetime
import logging

from ortools.linear_solver.python import model_builder

from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance


class GLOPSolver(Solver):
    def __init__(self):
        """
        Initializes the solver with an empty result.
        """
        self.result = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    @track_performance
    def run_glop(self, glop, model):
        """
        Runs the GLOP solver and tracks performance using the track_performance decorator.

        Args:
            glop (ModelSolver): The GLOP solver instance.
            model (ModelBuilder): The instance model

        Returns:
            dict: A dictionary containing the solver status and objective value.
        """
        model_status = glop.solve(model)

        obj_value = glop.objective_value

        return {
            "status": model_status,
            "objective_value": obj_value,
            "solver": "GLOP"
        }

    def solve(self, mps_file, options=None):
        """
        Solves the optimization problem using the GLOP solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            options (dict, optional): A dictionary of solver options to configure GLOP.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """
        model = model_builder.ModelBuilder()
        model.import_from_mps_file(mps_file)
        glop = model_builder.ModelSolver('GLOP')

        if options:
            for key, value in options.items():
                if key == 'time_limit':
                    glop.set_time_limit_in_seconds(value)
                else:
                    self.logger.info(f"Parameter {key} is not implemented or it does not exist")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"[{current_time}] Running the GLOP solver on {mps_file}...")

        self.result = self.run_glop(glop, model)

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
