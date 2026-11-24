from app.errors import SurveyProblem
from app.modules.ledger.identity import canonical, sha


def authenticate(manifest, tables, results):
    if {key:sha(text) for key,text in tables.items()} != manifest['files']:
        raise SurveyProblem('BAD_SEAL','原始样本摘要校验失败',409)
    if sha(canonical(results)) != manifest['result_sha256']:
        raise SurveyProblem('BAD_SEAL','扩推结果摘要校验失败',409)
    if not results['balance']['balanced']:
        raise SurveyProblem('UNBALANCED','人口或回收行尚未对平',409)
