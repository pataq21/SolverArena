from solverarena import run_models

if __name__ == "__main__":
    mps_files = [
        "examples/mps_files/model_dataset100.mps",
    ]

    solvers = {
        "highs": {
            "solver_name": "highs",
        },
        "scip": {
            "solver_name": "scip",
        },
        "copt": {
            "solver_name": "copt",
        },
        "glop": {
            "solver_name": "glop",
        }
    }
    results = run_models(mps_files, solvers)
