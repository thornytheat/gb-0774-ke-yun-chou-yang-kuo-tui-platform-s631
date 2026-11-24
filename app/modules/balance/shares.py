from fractions import Fraction

from app.config import CHOICES


def bias(observed, allocated):
    n, total = sum(observed.values()), sum(allocated.values())
    result = {}
    for key in CHOICES:
        unweighted = Fraction(observed[key],n) if n else None
        adjusted = Fraction(allocated[key],total) if total else None
        difference = (adjusted-unweighted)*100 if unweighted is not None and adjusted is not None else None
        result[key] = dict(raw=str(unweighted) if unweighted is not None else None,
                           adjusted=str(adjusted) if adjusted is not None else None,
                           shift_pp=str(difference) if difference is not None else None)
    return result
