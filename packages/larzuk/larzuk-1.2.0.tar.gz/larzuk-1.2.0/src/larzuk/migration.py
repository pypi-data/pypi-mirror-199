import os
import sqlite3
import importlib.util
from pathlib import Path
from dataclasses import dataclass
from types import ModuleType, FunctionType
from typing import Iterable

from d2txt import D2TXT
from diff_match_patch import diff_match_patch


class MigrationSpec(ModuleType):
    target: str
    migrate: FunctionType


class MigrationAppliedError(RuntimeError):
    ...


@dataclass
class Migration:
    name: str
    spec: MigrationSpec


class MigrationManager:
    target_dir: Path
    db: sqlite3.Connection

    def __init__(self, target_dir: Path):
        self.target_dir = target_dir
        self.db = self.connect_db()

    def connect_db(self):
        db_file = self.target_dir.joinpath('larzuk.sqlite')
        initialized = db_file.exists()

        db = sqlite3.connect(db_file)

        if not initialized:
            sql = 'CREATE TABLE migrations (name TEXT NOT NULL, target TEXT NULL, diff TEXT NULL)'
            db.execute(sql)

        return db

    def apply(self, migration: Migration):
        sql = 'SELECT COUNT(*) FROM migrations WHERE name = ?'
        row = self.db.execute(sql, (migration.name,)).fetchone()

        if row[0] > 0:
            raise MigrationAppliedError(migration.name)

        target_path = Path(self.target_dir, migration.spec.target)
        origin_text = target_path.read_text(encoding='utf-8')

        txt_file = D2TXT.load_txt(target_path)
        migration.spec.migrate(txt_file)
        txt_file.to_txt(target_path)

        modified_text = target_path.read_text(encoding='utf-8')

        dmp = diff_match_patch()
        patches = dmp.patch_make(modified_text, origin_text)

        sql = 'INSERT INTO migrations (name, target, diff) VALUES(?, ?, ?)'
        self.db.execute(sql, (migration.name, migration.spec.target, dmp.patch_toText(patches),))
        self.db.commit()

    def get_applied_names(self) -> Iterable[str]:
        sql = 'SELECT name FROM migrations'

        return map(lambda row: row[0], self.db.execute(sql).fetchall())

    def reverse(self, name: str):
        sql = 'SELECT target, diff FROM migrations WHERE name = ?'
        row = self.db.execute(sql, (name,)).fetchone()

        target_path = Path(self.target_dir, row[0])

        dmp = diff_match_patch()
        patches = dmp.patch_fromText(row[1])

        reversed_text, _ = dmp.patch_apply(patches, target_path.read_text(encoding='utf-8'))
        target_path.write_text(reversed_text, encoding='utf-8')

        sql = 'DELETE FROM migrations WHERE name = ?'
        self.db.execute(sql, (name,))
        self.db.commit()


def discover_migrations(base_dir: Path) -> list[Migration]:
    migrations = []

    for filename in filter(lambda f: f[-3:] == '.py', os.listdir(base_dir)):
        spec = importlib.util.spec_from_file_location(filename, Path(base_dir, filename))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        migrations.append(Migration(name=filename, spec=module))

    return migrations
