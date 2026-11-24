from app.modules.allocation.service import expand
from app.modules.balance.service import review
from app.modules.frame.service import align
from app.modules.returns.service import collect
from app.modules.weights.service import calibration

STAGES = ('returns','frame','weights','allocation','balance')


def run(tables, until='balance'):
    outputs = {'returns':collect(tables['returns'])}
    steps = (
        ('frame', lambda: align(outputs['returns'],tables['frame'])),
        ('weights', lambda: calibration(outputs['frame'])),
        ('allocation', lambda: expand(outputs['weights'])),
        ('balance', lambda: review(outputs['returns'],outputs['frame'],outputs['weights'],outputs['allocation'])),
    )
    for key, execute in steps:
        if until in outputs:
            break
        outputs[key] = execute()
    return outputs
