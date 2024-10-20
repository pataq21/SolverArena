from solver_arena.run import run_models

if __name__ == "__main__":
    mps_files = [
        "examples/mps_files/model_dataset100.mps",
        "examples/mps_files/model_dataset200.mps",
    ]

    solvers = ["gurobi", "highs"]
    parameters = {
        "highs": {
            "presolve": "on",
            "pdlp_native_termination": True,
            "solver": "pdlp",
        }
    }

    results = run_models(mps_files, solvers, parameters)
