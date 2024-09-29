from solvers.highs_solver import HiGHSSolver


class SolverFactory:
    @staticmethod
    def get_solver(solver_name: str):
        if solver_name.lower() == "highs":
            return HiGHSSolver()
        else:
            raise ValueError(f"Solver {solver_name} no reconocido")
