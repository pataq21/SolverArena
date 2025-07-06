import importlib
from typing import List, Dict, Type

from solverarena.solvers.solver import Solver


class SolverFactory:
    _solver_import_paths: Dict[str, str] = {
        "highs": "solverarena.solvers.highs_solver.HiGHSSolver",
        "gurobi": "solverarena.solvers.gurobi_solver.GurobiSolver",
        "glop": "solverarena.solvers.glop_solver.GLOPSolver",
        "scip": "solverarena.solvers.scip_solver.SCIPSolver",
        "copt": "solverarena.solvers.copt_solver.CoptSolver",
    }
    # Caché for already imported classes
    _loaded_solver_classes: Dict[str, Type] = {}

    @staticmethod
    def _load_solver_class(solver_name: str) -> Type:
        """Dynamically loads the solver class on demand."""
        solver_key = solver_name.lower()

        if solver_key in SolverFactory._loaded_solver_classes:
            return SolverFactory._loaded_solver_classes[solver_key]

        import_path = SolverFactory._solver_import_paths.get(solver_key)
        if not import_path:
            raise ValueError(
                f"Solver '{solver_name}' not recognized. Available: {list(SolverFactory._solver_import_paths.keys())}"
            )

        try:
            module_path, class_name = import_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            solver_class = getattr(module, class_name)

            SolverFactory._loaded_solver_classes[solver_key] = solver_class
            return solver_class

        except ImportError as e:
            raise ImportError(f"Could not import module for solver '{solver_name}' from '{module_path}': {e}") from e
        except AttributeError:
            raise AttributeError(f"Class '{class_name}' not found in module '{module_path}' for solver '{solver_name}'")

    @staticmethod
    def get_solver(solver_name: str) -> Solver:
        """Gets an instance of a solver, dynamically loading the class if necessary."""
        solver_class = SolverFactory._load_solver_class(solver_name)
        return solver_class()

    @staticmethod
    def is_solver_supported(solver_name: str) -> bool:
        """
        Checks if a solver name is recognized by the factory without importing or instantiating it.
        """
        return solver_name.lower() in SolverFactory._solver_import_paths

    @staticmethod
    def get_available_solvers() -> List[str]:
        """
        Returns a list of names of all available/supported solvers based on configuration.
        """
        return list(SolverFactory._solver_import_paths.keys())
