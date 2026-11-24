from app.config import CHOICES

from .remainders import largest_remainders


def expand(calibrated):
    layers, total, unknown = {}, dict.fromkeys(CHOICES,0), 0
    for name, layer in calibrated['layers'].items():
        unobserved = layer['population'] if layer['status']=='zero_response' else 0
        result = largest_remainders(layer['quotas'],layer['population']-unobserved)
        layers[name] = {**result,'population':layer['population'],'unobserved':unobserved,'status':layer['status']}
        unknown += unobserved
        for key,value in result['integers'].items():
            total[key] += value
    return dict(layers=layers, totals=total, unknown=unknown, estimated=sum(total.values()))
