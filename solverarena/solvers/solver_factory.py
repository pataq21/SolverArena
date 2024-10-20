

from solverarena.solvers.glop_solver import GLOPSolver
from solverarena.solvers.gurobi_solver import GurobiSolver
from solverarena.solvers.highs_solver import HiGHSSolver
from solverarena.solvers.pdlp_solver import PDLPSolver
from solverarena.solvers.scip_solver import SCIPSolver


class SolverFactory:
    @staticmethod
    def get_solver(solver_name: str):
        if solver_name.lower() == "highs":
            return HiGHSSolver()
        elif solver_name.lower() == "gurobi":
            return GurobiSolver()
        elif solver_name.lower() == "glop":
            return GLOPSolver()
        elif solver_name.lower() == "scip":
            return SCIPSolver()
        elif solver_name.lower() == "pdlp":
            return PDLPSolver()
        else:
            raise ValueError(f"Solver {solver_name} not recognized")
