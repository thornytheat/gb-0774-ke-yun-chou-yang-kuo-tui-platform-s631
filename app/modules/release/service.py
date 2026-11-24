from app.modules.ledger.identity import canonical, sha

from .audit import authenticate


def release(manifest,tables,results):
    authenticate(manifest,tables,results)
    excluded = {
        'intake':results['returns']['rejected'], 'alignment':results['frame']['invalid'],
        'nonresponse':results['frame']['nonresponse'],
    }
    payload = dict(manifest=manifest,originals=tables,results=results,excluded=excluded)
    return dict(**payload,seal=sha(canonical(payload)),verified=True)
