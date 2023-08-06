import click

from panorama_sidekick.panorama import Panorama
from panorama_sidekick.show import device_groups, firewalls


@click.group()
@click.pass_context
@click.option("--hostname", envvar="PANORAMA_HOSTNAME", help="Panorama hostname")
@click.option("--api_key", envvar="PANORAMA_KEY", help="Panorama API key")
def cli(ctx: click.Context, hostname: str, api_key: str) -> None:
    """A Palo Alto Panorama Sidekick"""
    ctx.obj = Panorama(hostname, api_key)


@cli.group()
def show() -> None:
    """List basic information."""


show.add_command(device_groups)
show.add_command(firewalls)
