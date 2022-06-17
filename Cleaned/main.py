import numpy as np
import pandas as pd
import json

from Cleaned.constants import base_bracket_url
from Cleaned.bracket_extraciton import get_so_far, get_bracket, get_group
from Cleaned.comp_bracket import *

from Cleaned.constants import *

game_to_results = {}
index = 0
# for x in range(1, len(rounds)):
#     game_to_results[x] = {}
#     for y in range(int(rounds[x])):
#         game_to_results[x][y] = {}

dad_group = "https://fantasy.espn.com/tournament-challenge-bracket/2022/en/group?groupID=4452645"
# yale_group = "https://fantasy.espn.com/tournament-challenge-bracket/2021/en/group?groupID=3993790"
#
#Gets the IDs of the participants
IDs = get_group(dad_group)
print(IDs)
# with open('IDs.json', 'r') as f:
#     IDs = json.load(f)

#Results is the results of the games played so far
#Team_to_seed is a dict mapping team name to seed
results, team_to_seed = get_so_far(base_bracket_url + IDs[0][0])

# with open('results.json', 'r') as f:
#     results = json.load(f)
#
# with open('team_to_seed.json', 'r') as f:
#     team_to_seed = json.load(f)

#Gets a list of the dictionary format of each bracket.
brackets = []
for x in range(len(IDs)):
    print(IDs[x])
    bracket = get_bracket(base_bracket_url + IDs[x][0])
    brackets.append(bracket)


# results['4'] = ['', '','','']
# results['2'] = ['','']
# results['1'] = ['']
#
# with open('brackets.json', 'w', encoding='utf-8') as f:
#     json.dump(brackets, f, ensure_ascii=False, indent=4)
#
# with open('results.json', 'w', encoding='utf-8') as f:
#     json.dump(results, f, ensure_ascii=False, indent=4)

# with open('team_to_seed.json', 'w', encoding='utf-8') as f:
#     json.dump(team_to_seed, f, ensure_ascii=False, indent=4)

# with open('IDs.json', 'w', encoding='utf-8') as f:
#     json.dump(IDs, f, ensure_ascii=False, indent=4)

# with open('brackets.json', 'r') as f:
#     brackets = json.load(f)

team_id = {}
for team in range(len(brackets[0]["64"])):
    team_id[brackets[0]['64'][team]] = team

game_to_results = np.zeros((7, 64, len(brackets), len(brackets)))
likelihoods = np.zeros((7, 64))

total, game_to_results, likelihoods = comp_brackets_weighted(results, brackets, team_to_seed, rounds, seed_vs_seed,
                                                             game_to_results, likelihoods, team_id)

total = comp_brackets_weighted(results, brackets)

# scores = np.sum(game_to_results, axis=tuple(range(1, game_to_results.ndim)))
# game_to_results = game_to_results[7 - np.count_nonzero(scores):7, :, :, :]
# likelihoods = likelihoods[7 - np.count_nonzero(scores):7, :]
# likelihoods = np.expand_dims(likelihoods, axis=-1)
# likelihoods = np.expand_dims(likelihoods, axis=-1)
# likelihoods = np.repeat(likelihoods, len(brackets), axis=-2)
# likelihoods = np.repeat(likelihoods, len(brackets), axis=-1)
# overall = game_to_results * likelihoods
# print(overall[1:, :, :, :])
# print(overall[25, 45, :, :])
# print(overall[1, 0, :, :])
# print(overall[25, 45, :, :])
#
# for x in range(np.count_nonzero(scores)):
#     overall_slice = overall[x, :, :, :]
#     for y in range(2 ** x):
#         print(x, y, y * 2 ** (6 - x), (y + 1) * 2 ** (6 - x))
#         game = np.sum(overall_slice[y * 2 ** (6 - x):(y + 1) * 2 ** (6 - x), :, :], axis=0, keepdims=True)
#         overall_slice[y * 2 ** (6 - x):(y + 1) * 2 ** (6 - x), :, :] = np.repeat(game, 2 ** (6 - x), axis=0)
#     overall[x, :, :, :] = overall_slice
#
# print(overall.shape)
# print(overall[0, 0, :, :])
# print(overall[0, 45, :, :])
# print(overall[1, 0, :, :])
# print(overall[1, 45, :, :])

# overall = np.repeat(overall, 64, axis=1)
# all_but_team = overall - game_to_results * likelihoods
# differance_team = game_to_results * likelihoods - all_but_team

# differance_team = differance_team[np.where(differance_team > 0.1)]
# likelihoods = np.where(likelihoods > 0.5)
# print(differance_team)
# significant_total = differance_team * likelihoods
# print(np.sum(significant_total.shape))
# nonfinished_rounds = []
# for round in game_to_results:
#     for game in game_to_results[round]:
#         if game_to_results[round][game] != {}:
#             nonfinished_rounds.append(round)
#             break

# for round in nonfinished_rounds:
#     round_matrix = np.zeros((2**(6-round), 2**round, len(brackets), len(brackets)))
#     for game in game_to_results[round]:
#         overall = np.zeros(len(brackets))
#         for team in game_to_results[round][game]:
#             overall += game_to_results[round][game][team]['result'] * game_to_results[round][game][team]['likelihood']
# for round in game_to_results:
#     for game in game_to_results[round]:
#         overall = np.zeros((len(brackets), len(brackets)))
#         for team in game_to_results[round][game]:
#             overall += game_to_results[round][game][team]['result'] * game_to_results[round][game][team]['result']
#         game_to_results[round][game][team]['overall'] = overall
#         for team in game_to_results[round][game][team]:


# # total = comp_brackets(results, brackets)
total = np.array(total) * 100

columns = ["1st", "2nd", "3rd"]
for x in range(3, len(IDs)):
    columns.append(str(x + 1) + "th")
rows = [entry[1] for entry in IDs]

df = pd.DataFrame(total, columns=columns, index=rows)
df.to_excel("DadAlwaysWins2022.xlsx")
# # df.to_excel("YSM_Class_of_2023_2.xlsx")
