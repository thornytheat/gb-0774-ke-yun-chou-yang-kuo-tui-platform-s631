RETURNS = ('ticket', 'trip', 'reported_layer', 'visit', 'status', 'probability', 'choice')
FRAME = ('trip', 'revision', 'layer', 'tickets')
MISSING = {'', '-', 'NULL', 'N/A', '未知'}


def blank(value):
    return value.strip().upper() in MISSING
