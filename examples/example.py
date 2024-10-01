

from solver_arena.run import run_models


if __name__ == "__main__":
    mps_files = ["mps_files/model_dataset600.mps"]
    solvers = ["highs", "glop", "pdlp", "scip"]

    results = run_models(mps_files, solvers)
