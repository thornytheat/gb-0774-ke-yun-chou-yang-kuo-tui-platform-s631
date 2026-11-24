from collections import Counter
from fractions import Fraction

from app.config import CHOICES


def calibrate_layer(population, answers):
    inverse = [(row, 1 / Fraction(row['probability'])) for row in answers]
    raw_mass = sum((weight for _,weight in inverse), Fraction())
    factor = Fraction(population) / raw_mass if raw_mass and population else None
    projected = dict.fromkeys(CHOICES, Fraction())
    evidence = []
    for row, weight in inverse:
        adjusted = weight * factor if factor is not None else Fraction()
        projected[row['choice']] += adjusted
        evidence.append(dict(ticket=row['ticket'], choice=row['choice'], line=row['line'],
                             base=str(weight), calibrated=str(adjusted), probability=row['probability'],
                             frame_lines=row['frame_lines']))
    count = Counter(row['choice'] for row in answers)
    status = 'zero_response' if not raw_mass else 'zero_population' if not population else 'calibrated'
    return dict(population=population, usable=len(answers), status=status, base_sum=str(raw_mass),
                factor=str(factor) if factor is not None else None, rows=evidence,
                observed={key:count[key] for key in CHOICES}, quotas={key:str(val) for key,val in projected.items()})
