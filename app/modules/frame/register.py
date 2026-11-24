from collections import defaultdict

from app.errors import SurveyProblem
from app.modules.returns.csv_input import rows
from app.modules.returns.schema import FRAME, blank


def versions(text):
    records, rejected, _ = rows(text, FRAME, '出票')
    if rejected:
        raise SurveyProblem('BAD_FRAME', f'出票表第 {rejected[0]["line"]} 行列数错误')
    grouped = defaultdict(dict)
    for row in records:
        raw = row['raw']
        trip, revision, layer, tickets = (raw[key].strip() for key in FRAME)
        if blank(trip) or blank(layer) or not all(v.isascii() and v.isdecimal() and len(v)<=9 for v in (revision,tickets)) or int(revision)==0:
            raise SurveyProblem('BAD_FRAME', f'出票表第 {row["line"]} 行定义不合法')
        revision, tickets = int(revision), int(tickets)
        prior = grouped[trip].get(revision)
        if prior and (prior['layer'],prior['tickets'])!=(layer,tickets):
            raise SurveyProblem('FRAME_CONFLICT', f'班次 {trip} 同版出票存在冲突')
        if prior:
            prior['lines'].append(row['line'])
        else:
            grouped[trip][revision]=dict(revision=revision,layer=layer,tickets=tickets,lines=[row['line']])
    return {trip: sorted(items.values(),key=lambda row:row['revision']) for trip,items in sorted(grouped.items())}
