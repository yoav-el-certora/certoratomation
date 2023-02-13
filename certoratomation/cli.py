import click
import logging


__all__ = (
    "run_server"
)

@click.group()
def cli():
    pass


@click.command()
@click.option("-h", "--host", default=None, help="Server Host")
@click.option("-p", "--port", default=None, help="Server Port")
def run_server(host: str = None, port: int = None):
    from .server.app import run_server
    run_server(host, port)
    pass


