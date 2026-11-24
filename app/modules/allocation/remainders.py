from fractions import Fraction

from app.config import CHOICES
from app.errors import SurveyProblem


def largest_remainders(values, total):
    exact = {key:Fraction(values[key]) for key in CHOICES}
    if any(value < 0 for value in exact.values()) or sum(exact.values()) != total:
        raise SurveyProblem('BAD_QUOTA', '配额与分层人口不一致')
    floors = {key:int(val) for key,val in exact.items()}
    order = sorted(CHOICES, key=lambda key: exact[key]-floors[key], reverse=True)
    winners = order[:total-sum(floors.values())]
    result = {key:floor+int(key in winners) for key,floor in floors.items()}
    return dict(integers=result, floors=floors, winners=winners,
                remainders={key:str(exact[key]-floors[key]) for key in floors})
