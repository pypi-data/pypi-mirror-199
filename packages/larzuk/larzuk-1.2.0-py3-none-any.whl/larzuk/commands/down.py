from pathlib import Path

import click
from larzuk.migration import MigrationManager


@click.command('down')
@click.argument('count', type=int, default=1)
@click.option('--target-dir', help='Target directory.', type=click.Path(file_okay=False, exists=True), required=True)
@click.option('--all', 'reverse_all', help='Reverse all migrations.', type=bool, is_flag=True)
def down_command(count: int, target_dir: Path, reverse_all: bool):
    """Reverse migrations"""

    target_dir = Path(target_dir)

    mm = MigrationManager(target_dir)

    names = list(reversed(list(mm.get_applied_names())))

    if not reverse_all:
        names = names[:count]

    for name in names:
        mm.reverse(name)
        click.echo(f'[DONE] {name} reversed.')
