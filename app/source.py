from app.config import EXAMPLES, MAX_BYTES
from app.errors import SurveyProblem

NAMES = {'returns','frame'}


def sources(body):
    if isinstance(body,dict) and set(body)=={'sample'}:
        sample = body['sample']
        if sample not in ('dirty','clean'):
            raise SurveyProblem('NO_SAMPLE','找不到样例',404)
        return {name:(EXAMPLES/sample/f'{name}.csv').read_bytes().decode() for name in sorted(NAMES)}
    if isinstance(body,dict) and set(body)=={'tables'}:
        texts = body['tables']
        if isinstance(texts,dict) and set(texts)==NAMES and all(isinstance(text,str) for text in texts.values()):
            try:
                if any(len(text.encode()) > MAX_BYTES for text in texts.values()):
                    raise SurveyProblem('TOO_LARGE','单份原件超过 350 KB',413)
            except UnicodeEncodeError as exc:
                raise SurveyProblem('BAD_INPUT','原件含非法字符') from exc
            return texts
    raise SurveyProblem('BAD_INPUT','请选择样例或提交两份 CSV')
