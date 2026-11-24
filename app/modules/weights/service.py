from collections import defaultdict

from .calibration import calibrate_layer


def calibration(frame):
    strata = defaultdict(list)
    for response in frame['valid']:
        strata[response['layer']].append(response)
    layers = {name:calibrate_layer(size,strata[name]) for name,size in frame['population'].items()}
    return {'layers':layers,'calibrated_layers':sum(layer['status']=='calibrated' for layer in layers.values()),
            'unobserved_population':sum(layer['population'] for layer in layers.values() if layer['status']=='zero_response')}
