from datetime import datetime
import highspy
import logging

from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance


class HiGHSSolver(Solver):
    """
    HiGHSSolver is a class that interfaces with the HiGHS optimization solver.

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
    def run_highs(self, highs):
        """
        Runs the HiGHS solver and tracks performance using the track_performance decorator.

        Args:
            highs (highspy.Highs): The HiGHS solver instance.

        Returns:
            dict: A dictionary containing the solver status and objective value.
        """
        highs.run()  # Execute the solver
        model_status = highs.getModelStatus()
        obj_value = highs.getObjectiveValue()

        return {
            "status": model_status,
            "objective_value": obj_value,
            "solver": "highs"
        }

    def solve(self, mps_file, options=None):
        """
        Solves the optimization problem using the HiGHS solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            options (dict, optional): A dictionary of solver options to configure HiGHS.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """
        highs = highspy.Highs()
        highs.readModel(mps_file)

        highs.setOptionValue('log_to_console', False)

        if options:
            for key, value in options.items():
                highs.setOptionValue(key, value)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"[{current_time}] Running the HiGHS solver on {mps_file}...")

        self.result = self.run_highs(highs)
        del highs
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
