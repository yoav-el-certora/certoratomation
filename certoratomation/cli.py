import click
import logging


__all__ = (
    "run_server"
)


@click.group()
def cli():
    pass


@click.command()
@click.option("-ra", "--run-all", is_flag=True, help="Run Server As Part Of CI")
@click.option("-h", "--host", default=None, help="Server Host")
@click.option("-p", "--port", default=None, help="Server Port")
def run_server(host: str = None, port: int = None, run_all: bool = False):
    from .server.app import run_server
    run_server(host, port)
