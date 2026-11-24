from fractions import Fraction

from app.modules.weights.calibration import calibrate_layer


def test_calibration_exact(dirty):  # TRAP-10
    layer=dirty['weights']['layers']['枢纽']
    assert layer['factor']=='50/3' and layer['base_sum']=='9'
    assert sum(Fraction(row['calibrated']) for row in layer['rows'])==150


def test_unequal_capture(dirty):
    layer=dirty['weights']['layers']['枢纽']
    assert {row['ticket']:row['base'] for row in layer['rows']}=={'00011':'3','00012':'4','00013':'2'}


def test_no_response_mass(dirty):
    layer=dirty['weights']['layers']['末班']
    assert (layer['status'],layer['factor'],layer['rows'])==('zero_response',None,[])
    assert dirty['weights']['unobserved_population']==40


def test_equal_capture(dirty):
    assert dirty['weights']['layers']['城北']['quotas']==dict.fromkeys(('direct','transfer','other'),'100/3')


def test_zero_population(dirty):
    answer=dirty['frame']['valid'][0]
    output=calibrate_layer(0,[answer])
    assert output['status']=='zero_population' and output['rows'][0]['calibrated']=='0'


def test_weights_contract_failure(client,tables):
    tables['frame']='trip,revision,layer,tickets\n0001,1,枢纽,-1\n'
    response=client.post('/api/survey/weights',json={'tables':tables})
    assert (response.status_code,response.json['code'])==(422,'BAD_FRAME')
