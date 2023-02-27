"""CertoraTomation Server Entrypoint"""

from fastapi import FastAPI
from .handlers import run_environment, run_test_package
import uvicorn


__all__ = (
    "certora_auto_server",
    "run_server"
)

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
