import subprocess
from fastapi import APIRouter, BackgroundTasks

__all__ = ("router", "run_dev_utils", "run_new_report")

from certoratomation.server.handlers.constants import HandlersConstants

router = APIRouter()


class ProcessHolder:
    DEV_UTILS_PROCESS: list = []
    NEW_REPORT_PROCESS: list = []


def run_dev_utils():
    ProcessHolder.DEV_UTILS_PROCESS.append(
        subprocess.Popen(
            args=HandlersConstants.DEV_UTILS_RUN_COMMAND,
            cwd=HandlersConstants.DEV_UTILS,
            shell=True
        )
    )


def run_new_report():
    subprocess.run(args=HandlersConstants.NEW_REPORT_INSTALL_COMMAND,
                   cwd=HandlersConstants.NEW_REPORT,
                   shell=True
                   )
    ProcessHolder.NEW_REPORT_PROCESS.append(
        subprocess.Popen(
            args=HandlersConstants.NEW_REPORT_RUN_COMMAND,
            cwd=HandlersConstants.NEW_REPORT,
            shell=True
        )
    )


@router.post("/run_environment")
async def run_environment(
        background_tasks: BackgroundTasks,
):
    background_tasks.add_task(run_dev_utils)
    background_tasks.add_task(run_new_report)


@router.post("/kill_environment")
async def kill_environment():
    for new_report_proc in ProcessHolder.NEW_REPORT_PROCESS:
        new_report_proc.terminate()
    for dev_utils_proc in ProcessHolder.DEV_UTILS_PROCESS:
        dev_utils_proc.terminate()
