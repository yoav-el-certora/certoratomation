import subprocess
from typing import Literal

from fastapi import APIRouter, BackgroundTasks

__all__ = ("router", "run_tests")

from pydantic import BaseModel

from certoratomation.server.certora_test_manager import CertoraTestManager

router = APIRouter()


class RunTestsResponse(BaseModel):
    run_status: Literal['Started_Running', "Error_Running"]


def run_tests():
    certora_test_manager = CertoraTestManager()

    return_code = certora_test_manager.run_service()
    return return_code


@router.post("/run_test_package", response_model=RunTestsResponse, status_code=201)
def run_test_package(
        background_tasks: BackgroundTasks
):
    background_tasks.add_task(run_tests)
    return RunTestsResponse(run_status='Started_Running')
