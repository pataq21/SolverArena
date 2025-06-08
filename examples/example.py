from solverarena import run_models

if __name__ == "__main__":
    mps_files = [
        "examples/mps_files/model_dataset100.mps",
    ]

    solvers = {
        "highs_default": {
            "solver_name": "cbc",
            "presolve": "on",
            "time_limit": 3600,
            "solver": "ipm"
        },
        "highs_no_presolve": {
            "solver_name": "highs",
            "presolve": "off",
            "time_limit": 1800,
            "solver": "simplex"
        }
    }
    results = run_models(mps_files, solvers)
