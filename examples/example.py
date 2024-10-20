from solverarena.run import run_models

if __name__ == "__main__":
    mps_files = [
        "examples/mps_files/model_dataset100.mps",
        "examples/mps_files/model_dataset200.mps",
    ]

    solvers = ["glop"]
    parameters = {
        "highs": {
            "presolve": "on",
        }
    }

    results = run_models(mps_files, solvers, parameters)
