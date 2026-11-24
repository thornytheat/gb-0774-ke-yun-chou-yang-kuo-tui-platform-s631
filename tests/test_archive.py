import sqlite3
from concurrent.futures import ThreadPoolExecutor

import pytest

from app.main import create_app
from app.modules.ledger.service import archive
from app.modules.ledger.storage import Archive


def test_create_manifest(client):
    answer=client.post('/api/runs',json={'sample':'dirty'})
    assert answer.status_code==201 and answer.json['manifest']['version']=='survey-2026.1'
    assert set(answer.json['manifest']['files'])=={'returns','frame'}


def test_replay_same(client):
    first=client.post('/api/runs',json={'sample':'dirty'}).json
    second=client.post(f"/api/runs/{first['id']}/rerun").json
    assert second=={**first,'reused':True}
    assert len(client.get('/api/runs').json['runs'])==1


def test_rollback_two_tables(tmp_path,tables):
    store=Archive(tmp_path/'rollback.db')
    with store.connect() as db:
        db.execute("CREATE TRIGGER reject_input BEFORE INSERT ON originals WHEN NEW.name='returns' BEGIN SELECT RAISE(ABORT,'bad original'); END")
    with pytest.raises(sqlite3.IntegrityError):
        archive(store,tables)
    with store.connect() as db:
        assert store.recent()==[] and db.execute('SELECT count(*) FROM originals').fetchone()[0]==0


def test_original_stays_across_app_reopen(tmp_path):
    path=tmp_path/'lasting.db'
    first=create_app(path).test_client().post('/api/runs',json={'sample':'dirty'}).json
    row=create_app(path).test_client().get(f"/api/runs/{first['id']}").json
    assert row['manifest']==first['manifest'] and row['allocation']['estimated']==250


def test_same_source_concurrent(tmp_path,tables):
    store=Archive(tmp_path/'race.db')
    with ThreadPoolExecutor(max_workers=3) as pool:
        result=list(pool.map(lambda _:archive(store,tables),range(3)))
    assert len(store.recent())==1 and sum(item['reused'] for item in result)==2


def test_missing_run(client):
    response=client.post('/api/runs/missing/rerun')
    assert (response.status_code,response.json['code'])==(404,'NO_RUN')
