import re
import pytest
import os
import csv
from unittest.mock import MagicMock, patch, call

from solverarena.run import run_models, run_solver_on_model, CSV_FIELDNAMES


# --- Fixtures (Reusable data for tests) ---

@pytest.fixture
def mock_solver():
    """Creates a basic mock of a solver."""
    solver = MagicMock()
    solver.get_results.return_value = {
        "status": "optimal",
        "objective_value": 123.45,
        "runtime": 0.5,
        "memory_used_MB": 100.0,
        "error": None,
    }
    return solver


@pytest.fixture
def mock_solver_factory(mocker, mock_solver):
    """Mocks SolverFactory.get_solver to return our mock_solver."""

    target = 'solverarena.run.SolverFactory.get_solver'
    mock_patch = mocker.patch(target, return_value=mock_solver)
    return mock_patch


@pytest.fixture
def apply_mock_factory_for_partial_failure(mocker):
    """
    Mocks SolverFactory.get_solver to return different mocks
    based on the solver name, simulating one failure.
    """
    solver_ok = MagicMock(name="MockSolverOK_PF")
    solver_ok.get_results.return_value = {
        "status": "optimal", "objective_value": 10, "runtime": 1,
        "memory_used_MB": 50, "error": None,
    }
    solver_ok.solve = MagicMock()

    solver_fail = MagicMock(name="MockSolverFail_PF")
    error_msg_internal = "Solver 2 crashed (from fixture)"
    solver_fail.solve.side_effect = Exception(error_msg_internal)

    def side_effect_logic(name):
        if name == 'solver1':
            return solver_ok
        elif name == 'solver2':
            return solver_fail
        else:
            return MagicMock()

    target = 'solverarena.run.SolverFactory.get_solver'
    mocker.patch(target, side_effect=side_effect_logic)


# --- Tests for run_solver_on_model ---

def test_run_solver_on_model_success(mocker, mock_solver_factory, mock_solver):
    """Verifies the success case for run_solver_on_model."""
    mps_file = "model1.mps"
    execution_alias = "test_alias"
    parameters = {"solver_name": "mock_solver", "param1": "value1"}

    mocker.patch('os.path.basename', return_value=mps_file)

    result = run_solver_on_model(mps_file, execution_alias, parameters)

    mock_solver_factory.assert_called_once_with("mock_solver")
    mock_solver.solve.assert_called_once_with(mps_file, {"param1": "value1"})
    mock_solver.get_results.assert_called_once()

    expected_result = {
        "execution_alias": execution_alias,
        "model": mps_file,
        "solver": "mock_solver",
        "status": "optimal",
        "objective_value": 123.45,
        "runtime": 0.5,
        "memory_used_MB": 100.0,
        "error": None,
    }
    assert result['status'] == expected_result['status']
    assert result['objective_value'] == expected_result['objective_value']
    assert result['execution_alias'] == execution_alias
    assert result['model'] == mps_file
    assert result['solver'] == 'mock_solver'

    assert all(key in result for key in CSV_FIELDNAMES)


def test_run_solver_on_model_solve_error(mocker, mock_solver_factory, mock_solver):
    """Verifies error handling during solver.solve()."""
    mps_file = "model_err.mps"
    execution_alias = "fail_alias"
    parameters = {"solver_name": "mock_solver"}
    error_message = "Solver crashed during solve"

    mock_solver.solve.side_effect = Exception(error_message)
    mocker.patch('os.path.basename', return_value=mps_file)

    result = run_solver_on_model(mps_file, execution_alias, parameters)

    mock_solver_factory.assert_called_once_with("mock_solver")
    mock_solver.solve.assert_called_once()
    mock_solver.get_results.assert_not_called()

    assert result["status"] == "error"
    assert error_message in result["error"]
    assert result["objective_value"] is None
    assert result["runtime"] is None
    assert result["execution_alias"] == execution_alias
    assert result["model"] == mps_file
    assert result["solver"] == 'mock_solver'
    assert all(key in result for key in CSV_FIELDNAMES)


def test_run_solver_on_model_get_results_error(mocker, mock_solver_factory, mock_solver):
    """Verifies error handling during solver.get_results()."""
    mps_file = "model_res_err.mps"
    execution_alias = "res_fail_alias"
    parameters = {"solver_name": "mock_solver"}
    error_message = "Failed to retrieve results"

    mock_solver.get_results.side_effect = Exception(error_message)
    mocker.patch('os.path.basename', return_value=mps_file)

    result = run_solver_on_model(mps_file, execution_alias, parameters)

    # Verifications
    mock_solver_factory.assert_called_once_with("mock_solver")
    mock_solver.solve.assert_called_once()
    mock_solver.get_results.assert_called_once()

    assert result["status"] == "error"
    assert error_message in result["error"]
    assert result["execution_alias"] == execution_alias
    assert result["model"] == mps_file
    assert result["solver"] == 'mock_solver'
    assert all(key in result for key in CSV_FIELDNAMES)


def test_run_solver_on_model_factory_error(mocker):
    """Verifies error handling if SolverFactory.get_solver fails."""
    mps_file = "model_fac_err.mps"
    execution_alias = "fac_fail_alias"
    parameters = {"solver_name": "unknown_solver"}
    error_message = "Solver not found"

    target = 'solverarena.run.SolverFactory.get_solver'
    mocker.patch(target, side_effect=ValueError(error_message))

    mocker.patch('os.path.basename', return_value=mps_file)

    result = run_solver_on_model(mps_file, execution_alias, parameters)

    assert result["status"] == "error"
    assert error_message in result["error"]
    assert result["objective_value"] is None
    assert result["execution_alias"] == execution_alias
    assert result["model"] == mps_file
    assert result["solver"] == 'unknown_solver'
    assert all(key in result for key in CSV_FIELDNAMES)


# --- Tests for run_models ---

@pytest.fixture
def setup_test_environment(tmp_path):
    """Creates dummy MPS files and output directory."""
    models_dir = tmp_path / "models"
    models_dir.mkdir()
    mps_file1 = models_dir / "m1.mps"
    mps_file2 = models_dir / "m2.mps"
    mps_file1.touch()  # Create empty files
    mps_file2.touch()

    output_dir = tmp_path / "results"

    return {"mps_files": [str(mps_file1), str(mps_file2)], "output_dir": output_dir}


def test_run_models_success_basic(mocker, setup_test_environment, mock_solver_factory, mock_solver):
    """Verifies a basic successful run of run_models with 1 model, 1 solver."""
    mps_files = setup_test_environment["mps_files"][:1]
    output_dir = setup_test_environment["output_dir"]
    solvers = {"cbc_default": {"solver_name": "cbc"}}

    mocker.patch('os.path.isfile', return_value=True)

    results_list = run_models(mps_files, solvers, output_dir)
    assert os.path.isdir(output_dir)
    mock_solver_factory.assert_called_once_with("cbc")
    mock_solver.solve.assert_called_once_with(mps_files[0])

    # Verify the returned result list
    assert len(results_list) == 1
    assert results_list[0]["model"] == os.path.basename(mps_files[0])
    assert results_list[0]["execution_alias"] == "cbc_default"
    assert results_list[0]["status"] == "optimal"

    # Verify CSV file content
    output_files = list(setup_test_environment["output_dir"].glob("results_*.csv"))
    assert len(output_files) == 1
    output_csv = output_files[0]

    with open(output_csv, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["model"] == os.path.basename(mps_files[0])
        assert rows[0]["execution_alias"] == "cbc_default"
        assert rows[0]["status"] == "optimal"
        assert rows[0]["objective_value"] == "123.45"


def test_run_models_multiple_solvers_models(mocker, setup_test_environment, mock_solver_factory, mock_solver):
    """Verifies execution with multiple models and solvers."""
    mps_files = setup_test_environment["mps_files"]
    output_dir = setup_test_environment["output_dir"]
    solvers = {
        "cbc_alias": {"solver_name": "cbc"},
        "gurobi_alias": {"solver_name": "gurobi", "TimeLimit": 60}
    }

    mocker.patch('os.path.isfile', return_value=True)

    results_list = run_models(mps_files, solvers, output_dir)

    assert mock_solver.solve.call_count == 4

    expected_calls = [
        call(mps_files[0]), call(mps_files[1]),
        call(mps_files[0], {'TimeLimit': 60}), call(mps_files[1], {'TimeLimit': 60}),
    ]
    mock_solver.solve.assert_has_calls(expected_calls, any_order=True)

    assert len(results_list) == 4

    output_files = list(setup_test_environment["output_dir"].glob("results_*.csv"))
    assert len(output_files) == 1
    with open(output_files[0], mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 4


def test_run_models_mps_file_not_found(mocker, setup_test_environment):
    """Verifies that FileNotFoundError is raised if an MPS file doesn't exist."""
    mps_files = setup_test_environment["mps_files"]
    output_dir = setup_test_environment["output_dir"]
    solvers = {"cbc_default": {"solver_name": "cbc"}}

    mocker.patch('os.path.isfile', side_effect=[False, True])
    expected_path_escaped = re.escape(mps_files[0])
    match_pattern = f"MPS file not found: {expected_path_escaped}"
    with pytest.raises(FileNotFoundError, match=match_pattern):
        run_models(mps_files, solvers, output_dir)


def test_run_models_invalid_solver_config(mocker, setup_test_environment):
    """Verifies that ValueError is raised if solver config is invalid."""
    mps_files = setup_test_environment["mps_files"]
    output_dir = setup_test_environment["output_dir"]
    # Invalid configuration (missing 'solver_name')
    solvers = {"bad_alias": {"param1": "value"}}

    mocker.patch('os.path.isfile', return_value=True)

    with pytest.raises(ValueError, match="Invalid configuration for alias 'bad_alias'"):
        run_models(mps_files, solvers, output_dir)


def test_run_models_partial_failure(mocker, setup_test_environment, apply_mock_factory_for_partial_failure):
    """Verifies that it continues if one solver fails, but logs the error."""
    mps_files = setup_test_environment["mps_files"][:1]
    output_dir = setup_test_environment["output_dir"]
    solvers = {
        "ok_solver": {"solver_name": "solver1"},
        "fail_solver": {"solver_name": "solver2"}
    }
    error_msg = "Solver 2 crashed"
    mocker.patch('os.path.isfile', return_value=True)

    mocker.patch('os.path.basename', return_value="m1.mps")

    results_list = run_models(mps_files, solvers, output_dir)

    assert len(results_list) == 2
    # The first should be success
    assert results_list[0]["execution_alias"] == "ok_solver"
    assert results_list[0]["status"] == "optimal"
    assert results_list[0]["error"] is None
    # The second should be failure
    assert results_list[1]["execution_alias"] == "fail_solver"
    assert results_list[1]["status"] == "error"
    assert error_msg in results_list[1]["error"]

    output_files = list(setup_test_environment["output_dir"].glob("results_*.csv"))
    assert len(output_files) == 1
    with open(output_files[0], mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["status"] == "optimal"
        assert rows[1]["status"] == "error"
        assert error_msg in rows[1]["error"]
