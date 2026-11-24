def test_module_pages(client):
    for tab,text in {'balance':'分层有效矩阵','returns':'回收裁决','frame':'班次出票沿革','weights':'分层校准证据',
                     'allocation':'尾差分配证据','archive':'近期扩推批次','release':'归档并校验'}.items():
        result=client.get('/survey/'+tab)
        assert result.status_code==200 and text in result.get_data(as_text=True)


def test_select_layer(client):
    answer=client.get('/survey/allocation?layer=枢纽').get_data(as_text=True)
    assert '200/3' in answer and '67' in answer


def test_failed_archival_does_not_write(client,tables):
    tables['frame']='broken,header\n'
    assert client.post('/api/runs',json={'tables':tables}).json['code']=='BAD_HEADER'
    assert client.get('/api/runs').json['runs']==[]
