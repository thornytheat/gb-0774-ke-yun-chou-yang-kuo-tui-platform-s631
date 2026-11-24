def test_leading_zero(dirty):  # TRAP-08
    assert '0001' in dirty['frame']['trips'] and '1' not in dirty['frame']['trips']
    assert dirty['frame']['valid'][0]['ticket']=='00011'


def test_missing_choice(dirty):  # TRAP-07
    row=next(row for row in dirty['frame']['invalid'] if row['code']=='ANSWER_MISSING')
    assert row['raw']['choice']=='N/A' and row['ticket']=='00032'


def test_current_layer(dirty):
    frame=dirty['frame']
    assert frame['population']=={'城北':100,'枢纽':150,'末班':40}
    assert frame['moved']==1
    assert frame['valid'][0]['layer']=='枢纽' and frame['valid'][0]['frame_lines']==[6]


def test_same_revision_same_ticket_count(dirty):
    assert dirty['frame']['trips']['0003']==[dict(revision=1,layer='城北',tickets=75,lines=[4,8])]


def test_newest_nonresponse(dirty):
    row=next(row for row in dirty['frame']['nonresponse'] if row['ticket']=='00014')
    assert row['visit']==2 and row['line']==20


def test_frame_conflicting_revision(client,tables):
    tables['frame']+='0001,2,城北,100\n'
    response=client.post('/api/survey/frame',json={'tables':tables})
    assert (response.status_code,response.json['code'])==(422,'FRAME_CONFLICT')


def test_missing_trip_separate(dirty):
    assert dirty['frame']['reasons']=={'BAD_PROBABILITY':1,'ANSWER_MISSING':1,'UNKNOWN_TRIP':1,'UNKNOWN_CELL':1}
