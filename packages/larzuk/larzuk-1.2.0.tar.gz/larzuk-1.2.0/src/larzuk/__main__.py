import click
from larzuk.commands import command_group


@click.group(commands=command_group)
@click.version_option(message='%(version)s')
def cli():
    """A command-line tool to help modding-as-code for game Diablo II: Resurrected."""


if __name__ == '__main__':
    cli()
