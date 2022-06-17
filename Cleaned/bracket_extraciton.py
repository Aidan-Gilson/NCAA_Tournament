from bs4 import BeautifulSoup
import requests

from Cleaned.constants import seed_order
from Cleaned.parser import *

#Gets the actual games and results that have been played
def get_so_far(url):
    print(url)
    bracket = {"64": [], "32": [], "16": [], "8": [], "4": [], "2": [], "1": []}
    data = requests.get(url)
    soup = BeautifulSoup(data.text, features='html.parser')
    index = 0
    team_to_seed = {}
    for x in range(1, 64):
        class_i = "matchup m_" + str(x)
        mydivs = soup.find_all("div", {"class": class_i})
        if mydivs == []:
            class_ii = class_i + " userPickable"
            mydivs = soup.find_all("div", {"class": class_ii})
            if mydivs == []:
                class_ii = class_i + " homeOnBottom" + " userPickable"
                mydivs = soup.find_all("div", {"class": class_ii})
            mydivs = mydivs[0].find_all("span", {"class": "name"})
            team1 = mydivs[0].text.strip()
            team2 = mydivs[1].text.strip()
            team3 = mydivs[2].text.strip()
            team4 = mydivs[3].text.strip()
        else:
            mydivs = mydivs[0].find_all("div", {"class": "slots"})
            team1 = mydivs[0].find_all("div", {"class": "slot s_1"})
            team1 = team1[0].find_all("span", {"class": "name"})
            team1 = team1[0].text.strip()

            team2 = mydivs[0].find_all("div", {"class": "slot s_2"})
            team2 = team2[0].find_all("span", {"class": "name"})
            team2 = team2[0].text.strip()
        if x <= 32:
            bracket["64"].append(team1)
            bracket["64"].append(team2)
            team_to_seed[team1] = seed_order[index]
            team_to_seed[team2] = seed_order[index + 1]
            index += 2
            if index == 16:
                index = 0
        elif x <= 48:
            bracket["32"].append(team1)
            bracket["32"].append(team3)
        elif x <= 56:
            bracket["16"].append(team1)
            bracket["16"].append(team3)
        elif x <= 60:
            bracket["8"].append(team1)
            bracket["8"].append(team3)
        elif x <= 62:
            bracket["4"].append(team1)
            bracket["4"].append(team3)
        elif x <= 63:
            bracket["2"].append(team1)
            bracket["2"].append(team3)

    mydivs = soup.find_all("div", {"class": "slot userPickable"})
    if len(mydivs) == 0:
        mydivs = soup.find_all("span", {"class": "actual winner"})
    teams = mydivs[0].find_all("span", {"class": "name"})
    team1 = teams[0].text.strip()
    # team2 = teams[1].text.strip()
    bracket["1"].append(team1)
    bracket["points"] = 1920
    return bracket, team_to_seed

#Gets the picks for a bracket for each game
def get_bracket(url):
    bracket = {"64": [], "32": [], "16": [], "8": [], "4": [], "2": [], "1": [], "points": 0}
    data = requests.get(url)
    soup = BeautifulSoup(data.text, features='html.parser')
    classes = []
    for x in range(1, 64):
        class_i = "matchup m_" + str(x)

        mydivs = soup.find_all("div", {"class": class_i})

        if mydivs == []:
            class_ii = class_i + " userPickable"
            mydivs = soup.find_all("div", {"class": class_ii})

            if mydivs == []:
                class_ii = class_i + " homeOnBottom" + " userPickable"
                mydivs = soup.find_all("div", {"class": class_ii})
            try:
                mydivs = mydivs[0].find_all("span", {"class": "name"})
            except:
                return {'64': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                               '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                               '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                               '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                        '32': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1',
                               '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                        '16': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                        '8': ['1', '1', '1', '1', '1', '1', '1', '1'], '4': ['1', '1', '1', '1'], '2': ['1', '1'],
                        '1': ['1'], 'points': 260}

            team1 = mydivs[0].text.strip()
            team2 = mydivs[1].text.strip()
            team3 = mydivs[2].text.strip()
            team4 = mydivs[3].text.strip()
        else:
            mydivs = mydivs[0].find_all("div", {"class": "slots"})
            team1 = mydivs[0].find_all("div", {"class": "slot s_1"})
            team1 = team1[0].find_all("span", {"class": "name"})
            team1 = team1[0].text.strip()

            team2 = mydivs[0].find_all("div", {"class": "slot s_2"})
            team2 = team2[0].find_all("span", {"class": "name"})
            team2 = team2[0].text.strip()

        if x <= 32:
            bracket["64"].append(team1)
            bracket["64"].append(team2)
        elif x <= 48:
            bracket["32"].append(team2)
            bracket["32"].append(team4)
            if team1 == team2:
                bracket["points"] += 10
            if team3 == team4:
                bracket["points"] += 10
        elif x <= 56:
            bracket["16"].append(team2)
            bracket["16"].append(team4)
            if team1 == team2:
                bracket["points"] += 20
            if team3 == team4:
                bracket["points"] += 20
        elif x <= 60:
            bracket["8"].append(team2)
            bracket["8"].append(team4)
            if team1 == team2:
                bracket["points"] += 40
            if team3 == team4:
                bracket["points"] += 40
        elif x <= 62:
            bracket["4"].append(team2)
            bracket["4"].append(team4)
            if team1 == team2:
                bracket["points"] += 80
            if team3 == team4:
                bracket["points"] += 80
        elif x <= 63:
            bracket["2"].append(team2)
            bracket["2"].append(team4)
            if team1 == team2:
                bracket["points"] += 160
            if team3 == team4:
                bracket["points"] += 160
    try:
        mydivs = soup.find_all("div", {"class": "slot userPickable"})
        teams = mydivs[0].find_all("span", {"class": "name"})
    except:
        try:
            mydivs = soup.find_all("div", {"class": "slot wWinner userPickable"})
            teams = mydivs[0].find_all("span", {"class": "name"})
        except:
            mydivs = soup.find_all("div", {"class": "slot s_2 correct wWinner userPickable"})
            teams = mydivs[0].find_all("span", {"class": "name"})
    team1 = teams[0].text.strip()
    team2 = teams[1].text.strip()
    bracket["1"].append(team2)
    if team1 == team2:
        bracket["points"] += 320

    return bracket

#Gets the IDs of all the participants in a group
def get_group(group):
    IDs = []
    soup = BeautifulSoup(parse2(group))
    mydivs = soup.find_all("table", {"class": "type_entries"})
    entries = mydivs[0].find_all("a", {"class": "entry"})
    for entry in entries:
        IDs.append((entry.get('href'), entry.text.strip()))
    return IDs
