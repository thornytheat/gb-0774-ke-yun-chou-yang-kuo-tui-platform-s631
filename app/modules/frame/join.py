import re
from fractions import Fraction

from app.config import CHOICES
from app.modules.returns.schema import blank


def probability(raw):
    raw = raw.strip()
    if not re.fullmatch(r'[0-9]{1,9}(?:\.[0-9]{1,9}|/[0-9]{1,9})?', raw):
        raise ValueError()
    value = Fraction(raw)
    if not 0 < value <= 1:
        raise ValueError()
    return str(value)


def classify(record, trips):
    raw = record['raw']
    trip, report = raw['trip'].strip(), raw['reported_layer'].strip()
    history = trips.get(trip)
    if not history:
        return {**record,'code':'UNKNOWN_TRIP'}
    last = history[-1]
    row = {**record,'trip':trip,'layer':last['layer'],'frame_lines':last['lines'],
           'from_layer':report,'moved':report!=last['layer']}
    if report not in {item['layer'] for item in history}:
        return {**row,'code':'UNKNOWN_CELL'}
    status, choice = raw['status'].strip().upper(), raw['choice'].strip()
    if status == 'NO':
        return {**row,'code':'NONRESPONSE'}
    if status != 'YES':
        return {**row,'code':'BAD_RESPONSE'}
    if blank(choice):
        return {**row,'code':'ANSWER_MISSING'}
    if choice not in CHOICES:
        return {**row,'code':'BAD_RESPONSE'}
    try:
        chance = probability(raw['probability'])
    except (ValueError, ZeroDivisionError):
        return {**row,'code':'BAD_PROBABILITY'}
    return {**row,'probability':chance,'choice':choice}
