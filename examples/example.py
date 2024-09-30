

from solver_arena.run import run_models, save_results_to_csv


if __name__ == "__main__":
    mps_files = ["mps_files/model_dataset600.mps"]
    solvers = ["highs"]

    results = run_models(mps_files, solvers)
    save_results_to_csv(results)
