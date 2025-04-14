from datetime import datetime
import highspy
import logging

from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance
from typing import Dict, Any, Optional


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
        highs.run()
        model_status = highs.getModelStatus()
        obj_value = highs.getObjectiveValue()

        return {
            "status": self._translate_status(model_status),
            "objective_value": obj_value,
            "solver": "highs"
        }

    def solve(self, mps_file, params: Optional[Dict[str, Any]] = None):
        """
        Solves the optimization problem using the HiGHS solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            params (dict, optional): A dictionary of solver options to configure HiGHS.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """
        highs = highspy.Highs()
        highs.readModel(mps_file)

        if params:
            for key, value in params.items():
                highs.setOptionValue(key, value)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"[{current_time}] Running the HiGHS solver on {mps_file}...")

        self.result = self.run_highs(highs)
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

    def _translate_status(self, native_status: Optional[highspy.HighsModelStatus]) -> str:
        """Translates HiGHS native status to standard status."""
        if native_status is None:
            return "error"

        if native_status == highspy.HighsModelStatus.kOptimal:
            return "optimal"
        elif native_status == highspy.HighsModelStatus.kInfeasible:
            return "infeasible"
        elif native_status == highspy.HighsModelStatus.kUnbounded:
            return "unbounded"
        elif native_status in [
            highspy.HighsModelStatus.kTimeLimit,
            highspy.HighsModelStatus.kIterationLimit,
            highspy.HighsModelStatus.kObjectiveBound,
            highspy.HighsModelStatus.kObjectiveTarget
        ]:
            return "limit_reached"
        elif native_status in [
            highspy.HighsModelStatus.kNotset,
            highspy.HighsModelStatus.kLoadError,
            highspy.HighsModelStatus.kModelError,
            highspy.HighsModelStatus.kPresolveError,
            highspy.HighsModelStatus.kSolveError,
            highspy.HighsModelStatus.kPostsolveError,
            highspy.HighsModelStatus.kUnknown,
        ]:
            return "error"
        else:
            self.logger.warning(f"Unhandled HiGHS native status: {native_status}. Reporting as error.")
            return "error"
