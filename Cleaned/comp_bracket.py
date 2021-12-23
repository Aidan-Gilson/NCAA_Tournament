import numpy as np
from Cleaned.score_bracket import score_bracket
from Cleaned.constants import seed_vs_seed

def comp_brackets(results, brackets, round_index=0, index=0):
    bracket_scores = [[0 for x in range(len(brackets))] for y in range(len(brackets))]
    if results["1"][0] != '':
        ordered = []
        results_copy = results.copy()
        for b in range(len(brackets)):
            bracket = brackets[b]
            score = score_bracket(bracket, results_copy)
            ordered.append((b, score))
        ordered = sorted(ordered, key=lambda x: x[1], reverse=True)
        for x in range(len(ordered)):
            bracket_scores[ordered[x][0]][x] = 1
        return bracket_scores
    else:
        if index == int(rounds[round_index]) - 1:
            next_round_index = round_index + 1
            next_index = 0
        else:
            next_round_index = round_index
            next_index = index + 1

        if results[rounds[round_index]][index] == '':
            options = [results[rounds[round_index - 1]][index * 2], results[rounds[round_index - 1]][index * 2 + 1]]
            results_copy = copy.deepcopy(results)
            results_copy[rounds[round_index]][index] = options[0]
            branch1 = comp_brackets_other(results_copy, brackets, next_round_index, next_index)

            results_copy = copy.deepcopy(results)
            results_copy[rounds[round_index]][index] = options[1]
            branch2 = comp_brackets_other(results_copy, brackets, next_round_index, next_index)
            total_branch = np.add(branch1, branch2)
            return total_branch
        else:
            return comp_brackets_other(results, brackets, next_round_index, next_index)


def comp_brackets_weighted(results, brackets, team_to_seed, round_index=0, index=0, liklihood=1):
    bracket_scores = [[0 for x in range(len(brackets))] for y in range(len(brackets))]
    if results["1"][0] != '':
        ordered = []
        results_copy = results.copy()
        for b in range(len(brackets)):
            bracket = brackets[b]
            score = score_bracket(bracket, results_copy)
            ordered.append((b, score))
        ordered = sorted(ordered, key=lambda x: x[1], reverse=True)
        for x in range(len(ordered)):
            bracket_scores[ordered[x][0]][x] = 1 * liklihood
        return bracket_scores
    else:
        if index == int(rounds[round_index]) - 1:
            next_round_index = round_index + 1
            next_index = 0
        else:
            next_round_index = round_index
            next_index = index + 1

        if results[rounds[round_index]][index] == '':
            options = [results[rounds[round_index - 1]][index * 2], results[rounds[round_index - 1]][index * 2 + 1]]
            results_copy = copy.deepcopy(results)
            results_copy[rounds[round_index]][index] = options[0]
            update = seed_vs_seed[team_to_seed[options[0]]][team_to_seed[options[1]]]
            branch1 = comp_brackets_other_weighted(results_copy, brackets, team_to_seed, next_round_index, next_index,
                                                   liklihood * update)

            results_copy = copy.deepcopy(results)
            results_copy[rounds[round_index]][index] = options[1]
            update = seed_vs_seed[team_to_seed[options[1]]][team_to_seed[options[0]]]
            branch2 = comp_brackets_other_weighted(results_copy, brackets, team_to_seed, next_round_index, next_index,
                                                   liklihood * update)
            total_branch = np.add(branch1, branch2)
            return total_branch
        else:
            return comp_brackets_other_weighted(results, brackets, team_to_seed, next_round_index, next_index,
                                                liklihood)
