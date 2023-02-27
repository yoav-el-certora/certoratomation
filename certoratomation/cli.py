import sys

import click
import logging


__all__ = (
    "run_certora_automation"
)

from certoratomation.server.certora_test_manager import CertoraTestManager


@click.group()
def cli():
    pass


@click.command()
@click.option("-r", "--run_server", is_flag=True, help="Run Certora Automation Server")
@click.option("-c", "--run_ci", is_flag=True, help="Run Certora Automation CI Tests")
@click.option("-h", "--host", default=None, help="Server Host")
@click.option("-p", "--port", default=None, help="Server Port")
def run_certora_automation(run_server, run_ci, host: str = None, port: int = None):
    if run_server:
        from .server.app import run_server
        run_server(host, port)

    elif run_ci:
        certora_test_manager = CertoraTestManager(run_environment=True)

        return_code = certora_test_manager.run_service()
        sys.exit(return_code)
