from collections import Counter

from .csv_input import rows
from .schema import RETURNS
from .visits import select_visits


def collect(text):
    records, rejected, counts = rows(text, RETURNS, '回收')
    accepted = select_visits(records, rejected)
    return dict(totals={**counts,'selected':len(accepted),'isolated':len(rejected)},
                accepted=accepted, rejected=sorted(rejected,key=lambda r:r['line']),
                reasons=dict(Counter(row['code'] for row in rejected)))
