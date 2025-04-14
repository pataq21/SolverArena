from typing import List
from solverarena.solvers.cbc_solver import CBCSolver
from solverarena.solvers.glop_solver import GLOPSolver
from solverarena.solvers.gurobi_solver import GurobiSolver
from solverarena.solvers.highs_solver import HiGHSSolver
from solverarena.solvers.pdlp_solver import PDLPSolver
from solverarena.solvers.scip_solver import SCIPSolver


class SolverFactory:
    _solver_map = {
        "highs": HiGHSSolver,
        "gurobi": GurobiSolver,
        "glop": GLOPSolver,
        "scip": SCIPSolver,
        "pdlp": PDLPSolver,
        "cbc": CBCSolver,
    }

    @staticmethod
    def get_solver(solver_name: str):
        solver_class = SolverFactory._solver_map.get(solver_name.lower())
        if solver_class:
            return solver_class()
        else:
            raise ValueError(
                f"Solver {solver_name} not recognized. Available: {list(SolverFactory._solver_map.keys())}")

    @staticmethod
    def is_solver_supported(solver_name: str) -> bool:
        """
        Checks if a solver name is recognized by the factory without instantiating it.

        Args:
            solver_name: The name of the solver to check.

        Returns:
            True if the solver name is supported, False otherwise.
        """
        return solver_name.lower() in SolverFactory._solver_map

    @staticmethod
    def get_available_solvers() -> List[str]:
        """
        Returns a list of names of all available/supported solvers.

        Returns:
            A list of strings, where each string is a supported solver name.
        """
        return list(SolverFactory._solver_map.keys())
