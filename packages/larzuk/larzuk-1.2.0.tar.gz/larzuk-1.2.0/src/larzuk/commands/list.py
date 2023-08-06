from pathlib import Path

import click
from larzuk.migration import MigrationManager


@click.command('list')
@click.option('--target-dir', help='Target directory.', type=click.Path(file_okay=False, exists=True), required=True)
def list_command(target_dir: Path):
    """List all applied migrations"""

    target_dir = Path(target_dir)
    mm = MigrationManager(target_dir)

    for name in mm.get_applied_names():
        click.echo(f'{name}')
