from constants import rounds_points

def score_bracket(bracket, results):
    points = 0
    for key in bracket.keys():
        if key != "points":
            bracket[key] = set(bracket[key])
            results[key] = set(results[key])
            points += rounds_points[key] * len(bracket[key] & results[key])
    return points
