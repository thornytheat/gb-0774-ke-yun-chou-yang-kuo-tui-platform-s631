import pytest

from app.errors import SurveyProblem
from app.modules.allocation.remainders import largest_remainders
from app.pipeline import run
from app.source import sources


def test_tie_is_stable(dirty):  # TRAP-24
    layer=dirty['allocation']['layers']['城北']
    assert layer['integers']=={'direct':34,'transfer':33,'other':33} and layer['winners']==['direct']


def test_unequal_remainders(dirty):
    layer=dirty['allocation']['layers']['枢纽']
    assert layer['remainders']=={'direct':'2/3','transfer':'0','other':'1/3'}
    assert layer['integers']=={'direct':67,'transfer':50,'other':33}


def test_dirty_integer_report(dirty):
    assert dirty['allocation']['totals']=={'direct':101,'transfer':83,'other':66}


def test_clean_includes_last_service():
    output=run(sources({'sample':'clean'}))['allocation']
    assert (output['estimated'],output['unknown'])==(290,0)
    assert output['layers']['末班']['integers']=={'direct':20,'transfer':20,'other':0}


def test_zero_kept_unknown(dirty):
    row=dirty['allocation']['layers']['末班']
    assert row['unobserved']==40 and sum(row['integers'].values())==0


def test_bad_quota_rejected():
    with pytest.raises(SurveyProblem) as exc:
        largest_remainders({'direct':'1/3','transfer':'1/3','other':'1/3'},2)
    assert exc.value.code=='BAD_QUOTA'
