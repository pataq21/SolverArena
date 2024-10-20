from datetime import datetime
import pyscipopt as scip
import logging
from solverarena.solvers.solver import Solver
from solverarena.solvers.utils import track_performance


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

    @track_performance
    def run_scip(self, model):
        """
        Runs the SCIP solver and tracks performance using the track_performance decorator.

        Args:
            model (pyscipopt.Model): The SCIP model instance.

        Returns:
            dict: A dictionary containing the solver status and objective value.
        """
        model.optimize()  # Execute the solver
        status = model.getStatus()
        obj_value = model.getObjVal() if status == "optimal" else None

        return {
            "status": status.upper(),
            "objective_value": obj_value,
            "solver": "scip"
        }

    def solve(self, mps_file, options=None):
        """
        Solves the optimization problem using the SCIP solver.

        Args:
            mps_file (str): The path to the MPS file containing the model.
            options (dict, optional): A dictionary of solver options to configure SCIP.

        Raises:
            FileNotFoundError: If the provided MPS file does not exist.
            ValueError: If an invalid option is passed in the options dictionary.
        """
        model = scip.Model()  # Create a new SCIP model

        try:
            # Load the MPS file
            model.readProblem(mps_file)
            model.setParam('display/verblevel', 0)
            # Apply solver options if any
            if options:
                for key, value in options.items():
                    model.setParam(key, value)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info(f"[{current_time}] Running the SCIP solver on {mps_file}...")

            # Run the SCIP solver and store the result
            self.result = self.run_scip(model)

            self.logger.info(f"Solver completed with status: {self.result['status']}.")

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
        return self.result
