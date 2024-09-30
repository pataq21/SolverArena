import psutil
from ortools.linear_solver import pywraplp
from ortools.linear_solver.python import model_builder

from solver_arena.solvers.solver import Solver


class SCIPSolver(Solver):
    def __init__(self):
        self.result = None

    def solve(self, mps_file, time_limit=1500):
        model = model_builder.ModelBuilder()
        model.import_from_mps_file(mps_file)
        solver = model_builder.ModelSolver('SCIP')
        solver.set_time_limit_in_seconds(time_limit)

        memory_before = psutil.Process().memory_info().rss / (1024 * 1024)
        status = solver.solve(model)
        memory_after = psutil.Process().memory_info().rss / (1024 * 1024)

        # Obtener resultados
        if status == pywraplp.Solver.OPTIMAL:
            obj_value = solver.objective_value
        else:
            obj_value = None

        run_time = solver.wall_time / 1000.0  # Convertir de milisegundos a segundos

        self.result = {
            "status": status,
            "objective_value": obj_value,
            "runtime": run_time,
            "solver": "glop",
            "memory_before_MB": memory_before,
            "memory_after_MB": memory_after,
            "memory_used_MB": memory_after - memory_before,
        }

    def get_results(self):
        return self.result
