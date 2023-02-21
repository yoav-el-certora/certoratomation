import subprocess
from typing import Literal

from fastapi import APIRouter, BackgroundTasks, HTTPException, status

__all__ = ("router", "run_tests")

from pydantic import BaseModel

from certoratomation.server.handlers.constants import HandlersConstants

router = APIRouter()


class RunTestsResponse(BaseModel):
    run_status: Literal['Started_Running', "Error_Running"]


def run_tests():
    return subprocess.run(
        args=HandlersConstants.RUN_TEST_COMMAND,
        cwd=HandlersConstants.TEST_PACKAGE,
        shell=True
    )


@router.post("/run_test_package", response_model=RunTestsResponse, status_code=201)
def run_test_package(
        background_tasks: BackgroundTasks
):
    background_tasks.add_task(run_tests)
    return RunTestsResponse(run_status='Started_Running')
