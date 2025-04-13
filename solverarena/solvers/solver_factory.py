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
