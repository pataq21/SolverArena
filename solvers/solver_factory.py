from solvers.gurobi_solver import GurobiSolver
from solvers.highs_solver import HiGHSSolver


class SolverFactory:
    @staticmethod
    def get_solver(solver_name: str):
        if solver_name.lower() == "highs":
            return HiGHSSolver()
        elif solver_name.lower() == "gurobi":
            return GurobiSolver()
        else:
            raise ValueError(f"Solver {solver_name} not recognized")
