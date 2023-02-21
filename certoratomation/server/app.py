"""CertoraTomation Server Entrypoint"""
import multiprocessing

from fastapi import FastAPI
from .handlers import run_environment, run_test_package
import uvicorn


__all__ = (
    "certora_auto_server",
    "run_server",
    "run_ci_tests"
)

from .handlers.run_environment import run_dev_utils, run_new_report
from .handlers.run_test_package import run_tests

routers = [
    run_environment.router,
    run_test_package.router
]

certora_auto_server = FastAPI(
    title="Certora Auto Server",
)

for router in routers:
    certora_auto_server.include_router(router)


def run_server(host: str = None, port: int = None):
    uvicorn.run(
        certora_auto_server,
        host=host if host else '127.0.0.1',
        port=port if port else 5001
    )


def run_ci_tests():
    dev_utils_server = multiprocessing.Process(
        target=run_dev_utils,
        name='certora automation localhost',
        daemon=True
    )
    new_report_server = multiprocessing.Process(
        target=run_new_report,
        name='certora automation localhost',
        daemon=True
    )

    dev_utils_server.start()
    new_report_server.start()

    return_code = run_tests()

    dev_utils_server.terminate()
    new_report_server.terminate()

    return return_code
