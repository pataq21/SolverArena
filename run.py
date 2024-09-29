from datetime import datetime
import os
import csv

from solvers.solver_factory import SolverFactory


def run_models(mps_files, solvers):
    results = []

    for mps_file in mps_files:
        for solver_name in solvers:
            print(f"Ejecutando {solver_name} en {mps_file}...")

            solver = SolverFactory.get_solver(solver_name)

            try:
                solver.solve(mps_file)
                result = solver.get_results()
                result["model"] = os.path.basename(mps_file)
                result["solver"] = solver_name
                results.append(result)
            except Exception as e:
                print(f"Error al ejecutar {solver_name} en {mps_file}: {str(e)}")
                results.append(
                    {
                        "model": os.path.basename(mps_file),
                        "solver": solver_name,
                        "status": "error",
                        "objective_value": None,
                        "runtime": None,
                        "error": str(e),
                    }
                )

    return results


def save_results_to_csv(results):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = f"results/results_{timestamp}.csv"

    if not os.path.exists("results"):
        os.makedirs("results")
    fieldnames = ["model", "solver", "status", "objective_value", "runtime", "error"]

    with open(output_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)


if __name__ == "__main__":
    mps_files = ["mps_files/model_dataset100.mps"]

    solvers = ["highs"]

    results = run_models(mps_files, solvers)

    for result in results:
        print(result)

    save_results_to_csv(results)
