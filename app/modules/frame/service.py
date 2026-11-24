from collections import Counter

from .join import classify
from .register import versions


def align(admitted, source):
    trips = versions(source)
    people = Counter()
    for history in trips.values():
        last = history[-1]
        people[last['layer']] += last['tickets']
    valid, invalid, no_answer = [], [], []
    for record in admitted['accepted']:
        row = classify(record, trips)
        code = row.get('code')
        if code == 'NONRESPONSE':
            no_answer.append(row)
        elif code:
            invalid.append(row)
        else:
            valid.append(row)
    return dict(trips=trips,population=dict(sorted(people.items())),valid=valid,invalid=invalid,nonresponse=no_answer,
                reasons=dict(Counter(row['code'] for row in invalid)), moved=sum(row['moved'] for row in valid),
                counts={'valid':len(valid),'invalid':len(invalid),'nonresponse':len(no_answer)})
