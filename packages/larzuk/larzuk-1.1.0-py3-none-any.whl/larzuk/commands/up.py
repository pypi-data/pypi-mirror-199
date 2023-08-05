import os
from pathlib import Path

import click
from larzuk.migration import discover_migrations, MigrationManager, MigrationAppliedError


@click.command('up')
@click.option('--target-dir', help='Target directory.', type=click.Path(file_okay=False, exists=True), required=True)
@click.option('--migration-dir', help='Migration directory.', type=click.Path(file_okay=False, exists=True), required=False, default=Path(os.getcwd(), 'migrations'))
def up_command(target_dir: Path, migration_dir: Path):
    """Apply migrations"""

    target_dir = Path(target_dir)

    mm = MigrationManager(target_dir)

    for migration in discover_migrations(migration_dir):
        try:
            mm.apply(migration)
            click.echo(f'[DONE] {migration.name} applied.')
        except MigrationAppliedError as e:
            click.echo(f'[SKIP] {e.args[0]} already applied.')
