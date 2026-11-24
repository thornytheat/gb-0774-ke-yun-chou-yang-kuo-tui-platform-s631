import pytest

from app.errors import SurveyProblem
from app.modules.ledger.identity import canonical, sha
from app.modules.ledger.service import archive
from app.modules.ledger.storage import Archive
from app.modules.release.service import release


@pytest.fixture
def archived(tmp_path,tables):
    store=Archive(tmp_path/'seal.db')
    key=archive(store,tables)['id']
    return store.read(key)


def test_seal_recompute(archived):
    output=release(*archived)
    actual=output.pop('seal')
    assert output.pop('verified') and actual==sha(canonical(output))


def test_bad_original(archived):
    archived[1]['returns']+='\n'
    with pytest.raises(SurveyProblem) as error:
        release(*archived)
    assert error.value.code=='BAD_SEAL'


def test_bad_results(archived):
    archived[2]['balance']['estimated']=0
    with pytest.raises(SurveyProblem) as error:
        release(*archived)
    assert error.value.status==409


def test_does_not_release_unbalanced(archived):
    manifest, tables, results=archived
    results['balance']['balanced']=False
    manifest['result_sha256']=sha(canonical(results))
    with pytest.raises(SurveyProblem) as error:
        release(manifest,tables,results)
    assert error.value.code=='UNBALANCED'


def test_evidence_has_exclusions(archived):
    output=release(*archived)
    assert {name:len(rows) for name,rows in output['excluded'].items()}=={'intake':6,'alignment':4,'nonresponse':2}
    assert output['originals']['returns'].startswith('\ufeff')


def test_api_export(client):
    key=client.post('/api/runs',json={'sample':'dirty'}).json['id']
    response=client.get('/api/export/'+key)
    assert response.headers['Content-Disposition'].startswith('attachment;')
    assert response.json['results']['balance']['unknown']==40
