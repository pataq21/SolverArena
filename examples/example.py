

from solver_arena.run import run_models


if __name__ == "__main__":
    mps_files = ["examples/mps_files/model_dataset100.mps"]
    solvers = ["pdlp", "scip", "glop"]

    results = run_models(mps_files, solvers)
