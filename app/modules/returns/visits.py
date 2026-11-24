from collections import defaultdict

from .schema import blank


def select_visits(rows, rejected):
    visits = defaultdict(list)
    for row in rows:
        raw = row['raw']
        ticket, visit = raw['ticket'].strip(), raw['visit'].strip()
        if blank(ticket) or blank(visit):
            rejected.append({**row, 'code':'MISSING_KEY'})
        elif not visit.isascii() or not visit.isdecimal() or not 1 <= len(visit) <= 6 or int(visit) == 0:
            rejected.append({**row,'code':'BAD_REV'})
        else:
            visits[ticket].append({**row, 'ticket':ticket, 'visit':int(visit)})
    chosen = []
    for ticket, events in sorted(visits.items()):
        latest = max(event['visit'] for event in events)
        heads = []
        for event in events:
            if event['visit'] < latest:
                rejected.append({**event,'code':'OLDER_VISIT','winning_visit':latest})
            else:
                heads.append(event)
        signatures = {tuple((key,value.strip()) for key,value in sorted(event['raw'].items()) if key!='visit')
                      for event in heads}
        if len(signatures) > 1:
            rejected.extend({**event,'code':'VISIT_CONFLICT'} for event in heads)
        else:
            winner, *duplicates = heads
            chosen.append(winner)
            rejected.extend({**event,'code':'REPEAT_VISIT','winner_line':winner['line']} for event in duplicates)
    return chosen
