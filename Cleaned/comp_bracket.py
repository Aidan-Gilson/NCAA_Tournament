import numpy as np
from Cleaned.score_bracket import score_bracket
from Cleaned.constants import seed_vs_seed
from Cleaned.constants import *
import copy


# Compare brackets as though each game is 50-50
def comp_brackets(results, brackets, round_index=0, index=0):
    # An array of brackets vs place where each cell is the chance of the bracket getting that place.
    bracket_scores = [[0 for x in range(len(brackets))] for y in range(len(brackets))]

    # Scores the brackets this way if the round is completed.
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

    # Scores the brackets this way if there are still games to be played
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


def comp_brackets_weighted(results, brackets, team_to_seed, rounds, seed_vs_seed, game_to_results, round_index=0, index=0, likelihood=1):
    bracket_scores = [[0 for x in range(len(brackets))] for y in range(len(brackets))]

    # Scores the brackets this way if the round is completed.
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
        return np.array(bracket_scores), game_to_results
    else:
        # Checks if we have checked every game in a round
        if index == int(rounds[round_index]) - 1:
            next_round_index = round_index + 1
            next_index = 0
        else:
            next_round_index = round_index
            next_index = index + 1

        # If the next game to be checked has not been played
        if results[rounds[round_index]][index] == '':

            # Get the two teams that are playing in this game on this recursion.
            options = [results[rounds[round_index - 1]][index * 2], results[rounds[round_index - 1]][index * 2 + 1]]

            # Create a new branch if the first team wins the game
            results_copy = copy.deepcopy(results)
            # Mark them as winning
            results_copy[rounds[round_index]][index] = options[0]
            # Finds the likelihood of this team actually winning the match
            update1 = seed_vs_seed[team_to_seed[options[0]]][team_to_seed[options[1]]]
            # Starts the new recursion.
            branch1, game_to_results = comp_brackets_weighted(results_copy, brackets, team_to_seed, rounds, seed_vs_seed, game_to_results,
                                             next_round_index, next_index,
                                             likelihood * update1)
            if options[0] in game_to_results[round_index][index]:
                game_to_results[round_index][index][options[0]]['result'] = (game_to_results[round_index][index][options[0]]['likelihood'] * game_to_results[round_index][index][options[0]]['result'] + likelihood * update1 * branch1) / (game_to_results[round_index][index][options[0]]['likelihood'] + update1 * likelihood)
                game_to_results[round_index][index][options[0]]['likelihood'] = game_to_results[round_index][index][options[0]]['likelihood'] + likelihood * update1
            else:
                game_to_results[round_index][index][options[0]] = {'result': branch1, 'likelihood':  likelihood * update1}
            # Create a new branch if the second team wins the game
            results_copy = copy.deepcopy(results)
            results_copy[rounds[round_index]][index] = options[1]
            update2 = seed_vs_seed[team_to_seed[options[1]]][team_to_seed[options[0]]]
            branch2, game_to_results = comp_brackets_weighted(results_copy, brackets, team_to_seed, rounds, seed_vs_seed, game_to_results,
                                             next_round_index, next_index,
                                             likelihood * update2)
            if options[1] in game_to_results[round_index][index]:
                game_to_results[round_index][index][options[1]]['result'] = (game_to_results[round_index][index][options[1]]['likelihood'] * game_to_results[round_index][index][options[1]]['result'] + likelihood * update2 * branch1) / (game_to_results[round_index][index][options[1]]['likelihood'] + update2 * likelihood)
                game_to_results[round_index][index][options[1]]['likelihood'] = game_to_results[round_index][index][options[1]]['likelihood'] + likelihood * update2
            else:
                game_to_results[round_index][index][options[1]] = {'result': branch2, 'likelihood': likelihood * update2}


            total_branch = np.add(branch1 * update1, branch2 * update2)
            return total_branch, game_to_results

        # If the game has been played
        else:
            return comp_brackets_weighted(results, brackets, team_to_seed, rounds, seed_vs_seed, game_to_results, next_round_index,
                                          next_index,
                                          likelihood)
