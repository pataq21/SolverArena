import os
from typing import Dict, List, Any
import logging

from solverarena.solvers.solver_factory import SolverFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --- Nueva Clase Validadora ---


class InputValidationError(ValueError):
    """Custom exception for input validation errors."""

    def __init__(self, messages: List[str]):
        super().__init__("Input validation failed:\n" + "\n".join(f"- {msg}" for msg in messages))
        self.messages = messages


class InputValidator:
    """Validates the inputs for the model running process."""

    def validate(self, mps_files: List[str], solvers: Dict[str, Dict[str, Any]]):
        """
        Validates MPS files and solver configurations.

        Args:
            mps_files: List of paths to MPS files.
            solvers: Dictionary of solver configurations.

        Raises:
            InputValidationError: If any validation check fails.
        """
        errors = []
        errors.extend(self._validate_mps_files(mps_files))
        errors.extend(self._validate_solvers(solvers))

        if errors:
            raise InputValidationError(errors)
        logger.info("Input validation successful.")

    def _validate_mps_files(self, mps_files: List[str]) -> List[str]:
        """Validates the list of MPS files."""
        file_errors = []
        if not isinstance(mps_files, list):
            file_errors.append("mps_files must be a list.")
            return file_errors  # Cannot proceed if not a list

        if not mps_files:
            file_errors.append("mps_files list cannot be empty.")

        for i, mps_file in enumerate(mps_files):
            if not isinstance(mps_file, str):
                file_errors.append(f"Item at index {i} in mps_files is not a string: {mps_file!r}")
                continue
            if not os.path.isfile(mps_file):
                file_errors.append(f"Input MPS file not found: {mps_file}")
            elif not mps_file.lower().endswith(('.mps', '.mps.gz')):
                file_errors.append(f"File does not appear to be an MPS file: {mps_file}")
        return file_errors

    def _validate_solvers(self, solvers: Dict[str, Dict[str, Any]]) -> List[str]:
        """Validates the solver configuration dictionary."""
        solver_errors = []
        if not isinstance(solvers, dict):
            solver_errors.append("solvers must be a dictionary.")
            return solver_errors

        if not solvers:
            solver_errors.append("solvers dictionary cannot be empty.")

        available_solvers = SolverFactory.get_available_solvers()

        for alias, params in solvers.items():
            if not isinstance(alias, str) or not alias:
                solver_errors.append(f"Invalid execution alias (must be non-empty string): {alias!r}")

            if not isinstance(params, dict):
                solver_errors.append(
                    f"Configuration for alias '{alias}' must be a dictionary, found {type(params).__name__}.")
                continue

            if "solver_name" not in params:
                solver_errors.append(f"Missing 'solver_name' key for alias '{alias}'.")
            else:
                solver_name_value = params["solver_name"]

                if not isinstance(solver_name_value, str) or not solver_name_value:
                    solver_errors.append(f"'solver_name' for alias '{alias}' must be a non-empty string.")

                elif not SolverFactory.is_solver_supported(solver_name_value):
                    solver_errors.append(
                        f"Unsupported solver name '{solver_name_value}' for alias '{alias}'. "
                        f"Supported solvers are: {available_solvers}"
                    )

        return solver_errors
