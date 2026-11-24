import csv
from collections import Counter
from io import StringIO

from app.errors import SurveyProblem


def rows(text, schema, source):
    iterator = csv.reader(StringIO(text.removeprefix('\ufeff'), newline=''), strict=True)
    accepted, rejected = [], []
    tally = Counter(segments=1, blanks=0, input=0)
    try:
        header = next(iterator, None)
        if header is None:
            raise SurveyProblem('EMPTY_FILE', f'{source}原件为空')
        if not text.strip('\ufeff \r\n\t,'):
            raise SurveyProblem('BLANK_FILE', f'{source}原件只有空行')
        if len(header) != len(schema) or set(header) != set(schema):
            raise SurveyProblem('BAD_HEADER', f'{source}表头字段有误')
        for fields in iterator:
            if fields == header:
                tally['segments'] += 1
            elif not any(field.strip() for field in fields):
                tally['blanks'] += 1
            else:
                tally['input'] += 1
                if len(fields) != len(header):
                    rejected.append(dict(line=iterator.line_num, raw=fields, code='BAD_WIDTH'))
                else:
                    accepted.append(dict(line=iterator.line_num, raw=dict(zip(header, fields))))
    except csv.Error as exc:
        raise SurveyProblem('BAD_CSV', f'{source}原件第 {iterator.line_num} 行有误') from exc
    if tally['input'] == 0:
        raise SurveyProblem('NO_RECORDS', f'{source}原件没有记录')
    return accepted, rejected, dict(tally)
