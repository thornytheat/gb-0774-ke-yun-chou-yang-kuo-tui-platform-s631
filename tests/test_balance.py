from app.modules.balance.service import review
from app.pipeline import run
from app.source import sources


def test_population_conserves(dirty):
    row=dirty['balance']
    assert (row['population'],row['estimated'],row['unknown'],row['population_delta'])==(290,250,40,0)


def test_line_conserves(dirty):
    assert dirty['balance']['return_delta']==0 and dirty['balance']['balanced'] is True


def test_within_layer_conserves(dirty):
    assert {k:(v['allocated'],v['unknown'],v['difference']) for k,v in dirty['balance']['strata'].items()} == {'城北':(100,0,0),'末班':(0,40,0),'枢纽':(150,0,0)}


def test_bias_exact(dirty):
    assert dirty['balance']['bias']['direct']=={'raw':'1/3','adjusted':'101/250','shift_pp':'106/15'}
    assert dirty['balance']['bias']['other']['shift_pp']=='-104/15'


def test_no_zero_comparison(dirty):
    assert all(row['shift_pp'] is None for row in dirty['balance']['strata']['末班']['bias'].values())
    assert run(sources({'sample':'clean'}))['balance']['unknown']==0


def test_missing_allocation_surfaces(dirty):
    dirty['allocation']['estimated']-=1
    actual=review(dirty['returns'],dirty['frame'],dirty['weights'],dirty['allocation'])
    assert actual['population_delta']==1 and not actual['balanced']


def test_detect_category_swap_even_when_population_conserves(dirty):
    dirty['allocation']['totals']['direct']-=1
    dirty['allocation']['totals']['other']+=1
    actual=review(dirty['returns'],dirty['frame'],dirty['weights'],dirty['allocation'])
    assert actual['population_delta']==0 and not actual['balanced']
    assert actual['category_delta']=={'direct':-1,'transfer':0,'other':1}
