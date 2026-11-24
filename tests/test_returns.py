import pytest

from app.errors import SurveyProblem
from app.modules.returns.service import collect


def test_bom(dirty):  # TRAP-02
    assert dirty['returns']['accepted'][0]['raw']['ticket']=='00011'


def test_header(dirty):  # TRAP-04
    assert dirty['returns']['totals']==dict(segments=2,blanks=1,input=18,selected=12,isolated=6)


def test_bad_width(dirty):  # TRAP-05
    row=next(x for x in dirty['returns']['rejected'] if x['code']=='BAD_WIDTH')
    assert (row['line'],row['raw'][-1])==(18,'多列')


def test_latest_then_duplicates(dirty,tables):  # TRAP-19
    header,*records=tables['returns'].splitlines()
    reversed_report=collect('\n'.join([header,*reversed(records)]))
    assert reversed_report['reasons']==dirty['returns']['reasons']
    assert [(r['ticket'],r['visit'],r['raw']['choice']) for r in reversed_report['accepted']] == [(r['ticket'],r['visit'],r['raw']['choice']) for r in dirty['returns']['accepted']]
    assert dirty['returns']['accepted'][0]['raw']['choice']=='transfer'


def test_conflict(dirty):  # TRAP-14
    assert [r['line'] for r in dirty['returns']['rejected'] if r['code']=='VISIT_CONFLICT']==[9,10]
    assert '00024' not in {r['ticket'] for r in dirty['returns']['accepted']}


def test_no_revision_guess(client,tables):
    text = tables['returns']+'07023,0004,末班,0,YES,1/2,other\n'
    assert collect(text)['reasons']['BAD_REV']==1
    response=client.post('/api/survey/returns',json={'tables':{**tables,'returns':'a,b\n'}})
    assert (response.status_code,response.json['code'])==(422,'BAD_HEADER')


def test_empty_source():
    with pytest.raises(SurveyProblem) as exc:
        collect('\n')
    assert exc.value.code=='BLANK_FILE'
