from collections import Counter

from .shares import bias


def review(intake, frame, weighted, allocation):
    frame_total = sum(frame['population'].values())
    input_counts = intake['totals']
    returned = frame['counts']
    line_delta = input_counts['input']-input_counts['isolated']-sum(returned.values())
    all_observed = Counter()
    strata = {}
    for name, population in frame['population'].items():
        row, calibrated = allocation['layers'][name], weighted['layers'][name]
        if row['status']=='calibrated':
            all_observed.update(calibrated['observed'])
        strata[name] = dict(population=population, usable=calibrated['usable'],
                            unknown=row['unobserved'], allocated=sum(row['integers'].values()),
                            difference=population-row['unobserved']-sum(row['integers'].values()),
                            bias=bias(calibrated['observed'],row['integers']))
    category_delta = {key:total-sum(layer['integers'][key] for layer in allocation['layers'].values())
                      for key,total in allocation['totals'].items()}
    estimated_delta = allocation['estimated']-sum(allocation['totals'].values())
    unknown_delta = allocation['unknown']-sum(row['unknown'] for row in strata.values())
    gap = frame_total-allocation['estimated']-allocation['unknown']
    return dict(population=frame_total, estimated=allocation['estimated'], unknown=allocation['unknown'],
                population_delta=gap, return_delta=line_delta, strata=strata, category_delta=category_delta,
                estimated_delta=estimated_delta, unknown_delta=unknown_delta,
                bias=bias(all_observed,allocation['totals']),
                balanced=gap==line_delta==estimated_delta==unknown_delta==0 and not any(category_delta.values())
                and all(row['difference']==0 for row in strata.values()))
