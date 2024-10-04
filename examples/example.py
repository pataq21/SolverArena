

from solver_arena.run import run_models


if __name__ == "__main__":
    mps_files = [
        # 'examples/mps_files/model_dataset100.mps',
        # 'examples/mps_files/model_dataset500.mps',
        # 'examples/mps_files/model_dataset1000.mps',
        # 'examples/mps_files/model_dataset1500.mps',
        # 'examples/mps_files/model_dataset2000.mps',
        # 'examples/mps_files/model_dataset2500.mps',
        # 'examples/mps_files/model_dataset3000.mps',
        'examples/mps_files/model_dataset3500.mps',
        'examples/mps_files/model_dataset4000.mps',
        'examples/mps_files/model_dataset4500.mps',
        'examples/mps_files/model_dataset5000.mps',
        'examples/mps_files/model_dataset5500.mps',
        'examples/mps_files/model_dataset6000.mps',
        'examples/mps_files/model_dataset6500.mps',
        'examples/mps_files/model_dataset7000.mps',
        'examples/mps_files/model_dataset7500.mps',
        'examples/mps_files/model_dataset8000.mps',
    ]
    solvers = ["highs"]
    parameters = {
        "highs": {
            "presolve": "on",
            "pdlp_native_termination": True,
            "solver": "pdlp",
        },
        # "glop": {
        #     "time_limit": 3000
        # },
        # "pdlp": {
        #     "time_limit": 3000
        # },
        # "scip": {
        #     "time_limit": 3000
        # },
    }

    results = run_models(mps_files, solvers, parameters)
