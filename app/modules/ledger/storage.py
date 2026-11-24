import json
import sqlite3
from contextlib import contextmanager, closing
from pathlib import Path

from app.errors import SurveyProblem

from .identity import canonical


class Archive:
    def __init__(self, filename):
        self.filename = filename
        Path(filename).parent.mkdir(exist_ok=True,parents=True)
        with self.connect() as db:
            db.executescript('''CREATE TABLE IF NOT EXISTS runs(
                id TEXT PRIMARY KEY, created TEXT NOT NULL, document TEXT NOT NULL, results TEXT NOT NULL
            ); CREATE TABLE IF NOT EXISTS originals(
                id TEXT REFERENCES runs(id), name TEXT NOT NULL, csv TEXT NOT NULL, PRIMARY KEY(id,name)
            );''')

    @contextmanager
    def connect(self):
        with closing(sqlite3.connect(self.filename,timeout=10)) as db, db:
            db.execute('PRAGMA foreign_keys=ON')
            yield db

    def add(self, manifest, tables, results):
        key = manifest['id']
        with self.connect() as db:
            created = db.execute('INSERT OR IGNORE INTO runs VALUES (?,?,?,?)',
                                 (key,manifest['created'],canonical(manifest),canonical(results))).rowcount
            if created:
                db.executemany('INSERT INTO originals VALUES (?,?,?)',[(key,name,csv) for name,csv in tables.items()])
        return bool(created)

    def read(self,key):
        with self.connect() as db:
            row = db.execute('SELECT document,results FROM runs WHERE id=?',(key,)).fetchone()
            tables = dict(db.execute('SELECT name,csv FROM originals WHERE id=?',(key,)))
        if not row:
            raise SurveyProblem('NO_RUN','找不到扩推归档',404)
        manifest, results = map(json.loads,row)
        return manifest,tables,results

    def recent(self):
        with self.connect() as db:
            rows = db.execute('SELECT document FROM runs ORDER BY created DESC,id LIMIT 40').fetchall()
        return [json.loads(row[0]) for row in rows]
