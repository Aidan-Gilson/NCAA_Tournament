import numpy as np
import pandas as pd

from Cleaned.constants import base_bracket_url
from Cleaned.bracket_extraciton import get_so_far, get_bracket, get_group
from Cleaned.comp_bracket import *

dad_group = "https://fantasy.espn.com/tournament-challenge-bracket/2021/en/group?groupID=3150699"
yale_group = "https://fantasy.espn.com/tournament-challenge-bracket/2021/en/group?groupID=3993790"

IDs = get_group(dad_group)

results, team_to_seed = get_so_far(base_bracket_url + IDs[0][0])

brackets = []
for x in range(len(IDs)):
    print(IDs[x])
    bracket = get_bracket(base_bracket_url + IDs[x][0])
    brackets.append(bracket)

total = comp_brackets_weighted(results, brackets, team_to_seed)
# total = comp_brackets(results, brackets)
total = np.array(total) * 100

columns = ["1st", "2nd", "3rd"]
for x in range(3, len(IDs)):
    columns.append(str(x + 1) + "th")
rows = [entry[1] for entry in IDs]

df = pd.DataFrame(total, columns=columns, index=rows)
df.to_excel("DadAlwaysWins2_3.xlsx")
# df.to_excel("YSM_Class_of_2023_2.xlsx")
