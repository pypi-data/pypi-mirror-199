import click

from panorama_sidekick.panorama import Panorama
from panorama_sidekick.show import device_groups, firewalls


@click.group()
@click.pass_context
@click.option("--hostname", envvar="PANORAMA_HOSTNAME")
@click.option("--api_key", envvar="PANORAMA_KEY")
def cli(ctx: click.Context, hostname: str, api_key: str) -> None:
    """Main console script entry point."""
    ctx.obj = Panorama(hostname, api_key)


@cli.group()
def show() -> None:
    """Command group for showing lists of things."""


show.add_command(device_groups)
show.add_command(firewalls)
