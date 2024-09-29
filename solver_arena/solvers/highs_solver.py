import highspy
import psutil

from solver_arena.solvers.solver import Solver


class HiGHSSolver(Solver):
    def __init__(self):
        self.result = None

    def solve(self, mps_file):
        highs = highspy.Highs()
        highs.readModel(mps_file)
        memory_before = psutil.Process().memory_info().rss / (1024 * 1024)
        highs.run()
        memory_after = psutil.Process().memory_info().rss / (1024 * 1024)

        model_status = highs.getModelStatus()
        obj_value = highs.getObjectiveValue()
        run_time = highs.getRunTime()

        self.result = {
            "status": model_status,
            "objective_value": obj_value,
            "runtime": run_time,
            "solver": "highs",
            "memory_before_MB": memory_before,
            "memory_after_MB": memory_after,
            "memory_used_MB": memory_after - memory_before,
        }

    def get_results(self):
        return self.result
