import highspy

from solvers.solver import Solver


class HiGHSSolver(Solver):
    def __init__(self):
        self.result = None

    def solve(self, mps_file):
        # Cargamos y resolvemos el modelo usando HiGHS
        highs = highspy.Highs()
        highs.readModel(mps_file)
        highs.run()

        # Extraemos la información relevante
        model_status = highs.getModelStatus()
        obj_value = highs.getObjectiveValue()
        run_time = highs.getRunTime()

        # Guardamos el resultado en la variable result
        self.result = {"status": model_status, "objective_value": obj_value, "runtime": run_time, "solver": "highs"}

    def get_results(self):
        return self.result
