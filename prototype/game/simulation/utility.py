def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)


def average(elements):
    return sum(elements) / len(elements)


def trendline(elements):
    deltas = []

    elements_to_check = min(5, len(elements) - 1)
    for i in range(0, elements_to_check):
        deltas.append(elements[-i - 1] - elements)

    return average(deltas), elements[-1]
