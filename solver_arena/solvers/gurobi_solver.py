import time
import gurobipy as gp
import psutil

from solver_arena.solvers.solver import Solver


class GurobiSolver(Solver):
    def __init__(self):
        self.result = None

    def solve(self, mps_file, time_limit=1500):
        model = gp.read(mps_file)
        model.Params.TimeLimit = time_limit
        model.Params.OutputFlag = 0

        start_time = time.time()
        memory_before = psutil.Process().memory_info().rss / (1024 * 1024)
        model.optimize()
        end_time = time.time()
        memory_after = psutil.Process().memory_info().rss / (1024 * 1024)

        if model.status == gp.GRB.OPTIMAL:
            model_status = "OPTIMAL"
            obj_value = model.objVal
        else:
            model_status = model.status
            obj_value = None

        run_time = end_time - start_time

        self.result = {
            "status": model_status,
            "objective_value": obj_value,
            "runtime": run_time,
            "solver": "gurobi",
            "memory_before_MB": memory_before,
            "memory_after_MB": memory_after,
            "memory_used_MB": memory_after - memory_before,
        }

    def get_results(self):
        return self.result
