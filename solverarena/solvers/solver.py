from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from solverarena.models import SolverResult


class Solver(ABC):

    @abstractmethod
    def solve(self, mps_file, params: Optional[Dict[str, Any]] = None):
        """
        Solves the optimization problem defined in the MPS file.

        Args:
            mps_file (str): Path to the MPS model file.
            params (Optional[Dict[str, Any]]): A dictionary of solver-specific
                                               parameters (e.g., time limit, tolerances).
        """
        pass

    @abstractmethod
    def get_results(self) -> SolverResult:
        """
        Returns the results of the last solve run.

        Should return a dictionary containing at least the keys defined
        in run.py's CSV_FIELDNAMES (status, objective_value, runtime,
        memory_used_MB, error), potentially adding solver-specific info.
        Values can be None if not applicable or if an error occurred.
        """
        pass
