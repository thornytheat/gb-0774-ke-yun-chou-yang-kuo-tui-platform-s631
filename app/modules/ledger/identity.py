import hashlib
import json

from app.config import SPEC


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',',':'))


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def identity(inputs):
    hashes = {key:sha(text) for key,text in inputs.items()}
    return sha(canonical({'files':hashes,'version':SPEC})), hashes
