"""
test_service.py

Generic test for services (training or prediction). Set up the service folder
(copy model code, download model artifact if necessary), install model
dependencies and set current working directory to service folder, then run:
python -m akerbp.mlops.services.test_service
"""
import json
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from typing import Any, Dict, Tuple, Union

from akerbp.mlops.core import config
from akerbp.mlops.core.logger import get_logger

service_name = config.ENV_VARS.service_name

logger = get_logger(__name__)

client_secrets = config.client_secrets


def mock_saver(*args, **kwargs):
    pass


def run_tests(test_path: Union[Path, str], path_type: str = "file") -> None:
    """
    Run tests with pytest. Raises exception subprocess.CalledProcessError
    if pytest fails.

    Input
      - test_path: path to tests with pytest (string or a list of strings) All
        should have the same format (see next parameter)
      - path_type: either 'file' (test_path refers then to files/folders) or
        'module' (test_path refers then to modules)

    """
    command = [
        sys.executable,
        "-m",
        "pytest",
        "--quiet",
        "-o",
        "log_cli=true",
        "--color=no",
        "-W ignore:numpy.ufunc size changed",
    ]
    if path_type == "module":
        command.append("--pyargs")
    if isinstance(test_path, str) or isinstance(test_path, Path):
        command.append(str(test_path))
    elif isinstance(test_path, list):
        command += test_path
    else:
        raise ValueError("Input should be string or list of strings")
    logger.info(f"Run tests: {test_path}")
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command exited with error {e.stdout}") from e


def get_model_test_data(test_import_path: str) -> Tuple[Dict, bool]:
    """
    Read input and validation function from the model test file
    """
    service_test = import_module(test_import_path).ServiceTest()
    input = getattr(service_test, f"{service_name}_input")
    check = getattr(service_test, f"{service_name}_check")
    return input, check


def test_service(input: Dict, check: Any) -> None:
    """
    Generic service test. Call service with the model's test input data and
    validate the output.
    """
    logger.info(f"Test {service_name} service")
    service = import_module(f"akerbp.mlops.services.{service_name}").service

    if service_name == "training":
        response = service(data=input, secrets=client_secrets, saver=mock_saver)
    elif service_name == "prediction":
        response = service(data=input, secrets=client_secrets)
    else:
        raise Exception("Unknown service name")

    assert response["status"] == "ok"
    # assert check(response[service_name])


if __name__ == "__main__":
    logger = get_logger(name="akerbp.mlops.services.test_service.py")

    c = config.read_service_settings()
    run_tests(c.test_file)
    input, check = get_model_test_data(c.test_import_path)
    test_service(input, check)
    # Share input with main process:
    print(json.dumps(input))
