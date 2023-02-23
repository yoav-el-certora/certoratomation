import sys

import click
import logging


__all__ = (
    "run_certora_automation"
)

from certoratomation.server.test_runner import CertoraTestRunner


@click.group()
def cli():
    pass


@click.command()
@click.option("-r", "--run_server", is_flag=True, help="Run Certora Automation Server")
@click.option("-c", "--run_ci", is_flag=True, help="Run Certora Automation CI Tests")
@click.option("-h", "--host", default=None, help="Server Host")
@click.option("-p", "--port", default=None, help="Server Port")
def run_certora_automation(run_server, run_ci, host: str = None, port: int = None):
    # x = CertoraTestRunner(env='stg')
    # x.init_test_data()

    if run_server:
        from .server.app import run_server
        run_server(host, port)

    elif run_ci:
        from .server.app import run_ci_tests
        return_code = run_ci_tests()
        sys.exit(return_code)
