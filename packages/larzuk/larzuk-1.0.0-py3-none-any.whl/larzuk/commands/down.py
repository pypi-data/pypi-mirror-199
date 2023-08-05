from pathlib import Path

import click
from larzuk.migration import MigrationManager


@click.command('down')
@click.argument('count', type=int, default=1)
@click.option('--target-dir', help='Target directory.', type=click.Path(file_okay=False, exists=True), required=True)
def down_command(count: int, target_dir: Path):
    """Reverse migrations"""

    target_dir = Path(target_dir)

    mm = MigrationManager(target_dir)

    for name in list(reversed(list(mm.get_applied_names())))[:count]:
        mm.reverse(name)
        click.echo(f'[DONE] {name} reversed.')
