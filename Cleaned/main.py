import numpy as np
import pandas as pd
import json

from Cleaned.constants import base_bracket_url
from Cleaned.bracket_extraciton import get_so_far, get_bracket, get_group
from Cleaned.comp_bracket import *

from Cleaned.constants import *

game_to_results = {}
index = 0
for x in range(len(rounds)):
    game_to_results[x] = {}
    for y in range(int(rounds[x])):
        game_to_results[x][y] = {}

dad_group = "https://fantasy.espn.com/tournament-challenge-bracket/2021/en/group?groupID=3150699"
# yale_group = "https://fantasy.espn.com/tournament-challenge-bracket/2021/en/group?groupID=3993790"
#
# #Gets the IDs of the participants
# IDs = get_group(dad_group)

with open('IDs.json', 'r') as f:
  IDs = json.load(f)
#
# #Results is the results of the games played so far
# #Team_to_seed is a dict mapping team name to seed
# results, team_to_seed = get_so_far(base_bracket_url + IDs[0][0])

with open('results.json', 'r') as f:
  results = json.load(f)

with open('team_to_seed.json', 'r') as f:
  team_to_seed = json.load(f)

# #Gets a list of the dictionary format of each bracket.
# brackets = []
# for x in range(len(IDs)):
#     print(IDs[x])
#     bracket = get_bracket(base_bracket_url + IDs[x][0])
#     brackets.append(bracket)
#
#
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

with open('brackets.json', 'r') as f:
  brackets = json.load(f)


total, game_to_results = comp_brackets_weighted(results, brackets, team_to_seed, rounds, seed_vs_seed, game_to_results)
print(game_to_results)
# # total = comp_brackets(results, brackets)
total = np.array(total) * 100

columns = ["1st", "2nd", "3rd"]
for x in range(3, len(IDs)):
    columns.append(str(x + 1) + "th")
rows = [entry[1] for entry in IDs]

df = pd.DataFrame(total, columns=columns, index=rows)
df.to_excel("DadAlwaysWins2_3.xlsx")
# # df.to_excel("YSM_Class_of_2023_2.xlsx")
