from bs4 import BeautifulSoup
from bs4 import Comment
import requests
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver import Chrome
from time import sleep
import numpy as np
import copy
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def parse2(url):
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument('--headless')
	driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
	driver.get(url)
	sleep(3)
	sourceCode = driver.page_source
	return sourceCode

def parse(url):
	response = webdriver.Chrome()
	response.get(url)
	sleep(3)
	sourceCode = response.page_source
	return sourceCode


base_bracket_url = "https://fantasy.espn.com/tournament-challenge-bracket/2022/en/"
dad_group = "https://fantasy.espn.com/tournament-challenge-bracket/2022/en/group?groupID=4452645"
yale_group = "https://fantasy.espn.com/tournament-challenge-bracket/2021/en/group?groupID=3993790"
rounds = ["64", "32", "16", "8", "4", "2", "1"]
rounds_points = {"64": 0, "32": 10, "16": 20, "8": 40, "4": 80, "2": 160, "1": 320}

seed_vs_seed = {'1': {'1': 0.5, '2': 0.539, '3': 0.634, '4': 0.711, '5': 0.839, '6': 0.706, '7': 0.857, '8': 0.798, '9': 0.901, '10': 0.857, '11': 0.556, '12': 1.0, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.993}, '2': {'1': 0.461, '2': 0.5, '3': 0.603, '4': 0.444, '5': 0.167, '6': 0.722, '7': 0.694, '8': 0.444, '9': 0.5, '10': 0.645, '11': 0.833, '12': 0.5, '13': 0.5, '14': 0.5, '15': 0.938, '16': 0.5}, '3': {'1': 0.366, '2': 0.397, '3': 0.5, '4': 0.625, '5': 0.5, '6': 0.576, '7': 0.611, '8': 0.5, '9': 0.5, '10': 0.692, '11': 0.679, '12': 0.5, '13': 0.5, '14': 0.847, '15': 0.5, '16': 0.5}, '4': {'1': 0.289, '2': 0.556, '3': 0.375, '4': 0.5, '5': 0.563, '6': 0.333, '7': 0.333, '8': 0.364, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.69, '13': 0.79, '14': 0.5, '15': 0.5, '16': 0.5}, '5': {'1': 0.161, '2': 0.833, '3': 0.5, '4': 0.438, '5': 0.5, '6': 0.5, '7': 0.5, '8': 0.5, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.671, '13': 0.842, '14': 0.5, '15': 0.5, '16': 0.5}, '6': {'1': 0.294, '2': 0.278, '3': 0.424, '4': 0.667, '5': 0.5, '6': 0.5, '7': 0.625, '8': 0.5, '9': 0.5, '10': 0.6, '11': 0.634, '12': 0.5, '13': 0.5, '14': 0.875, '15': 0.5, '16': 0.5}, '7': {'1': 0.143, '2': 0.306, '3': 0.389, '4': 0.667, '5': 0.5, '6': 0.333, '7': 0.5, '8': 0.5, '9': 0.5, '10': 0.601, '11': 0.5, '12': 0.5, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.5}, '8': {'1': 0.202, '2': 0.556, '3': 0.5, '4': 0.636, '5': 0.5, '6': 0.5, '7': 0.5, '8': 0.5, '9': 0.518, '10': 0.5, '11': 0.5, '12': 0.5, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.5}, '9': {'1': 0.099, '2': 0.5, '3': 0.5, '4': 0.5, '5': 0.5, '6': 0.5, '7': 0.5, '8': 0.482, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.5, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.5}, '10': {'1': 0.143, '2': 0.355, '3': 0.308, '4': 0.5, '5': 0.5, '6': 0.4, '7': 0.399, '8': 0.5, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.5, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.5}, '11': {'1': 0.444, '2': 0.167, '3': 0.321, '4': 0.5, '5': 0.5, '6': 0.366, '7': 0.5, '8': 0.5, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.5, '13': 0.5, '14': 0.9, '15': 0.5, '16': 0.5}, '12': {'1': 0.1, '2': 0.5, '3': 0.5, '4': 0.31, '5': 0.329, '6': 0.5, '7': 0.5, '8': 0.5, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.5, '13': 0.75, '14': 0.5, '15': 0.5, '16': 0.5}, '13': {'1': 0.5, '2': 0.5, '3': 0.5, '4': 0.21, '5': 0.158, '6': 0.5, '7': 0.5, '8': 0.5, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.25, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.5}, '14': {'1': 0.5, '2': 0.5, '3': 0.153, '4': 0.5, '5': 0.5, '6': 0.125, '7': 0.5, '8': 0.5, '9': 0.5, '10': 0.5, '11': 0.1, '12': 0.5, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.5}, '15': {'1': 0.5, '2': 0.063, '3': 0.5, '4': 0.5, '5': 0.5, '6': 0.5, '7': 0.5, '8': 0.5, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.5, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.5}, '16': {'1': 0.007, '2': 0.5, '3': 0.5, '4': 0.5, '5': 0.5, '6': 0.5, '7': 0.5, '8': 0.5, '9': 0.5, '10': 0.5, '11': 0.5, '12': 0.5, '13': 0.5, '14': 0.5, '15': 0.5, '16': 0.5}}
seed_order = ['1', '16', "8", "9", "5", "12", "4", "13", "6", "11", "3", "14", "7", "10", "2", "15"]

def score_bracket(bracket, results):
	points = 0
	for key in bracket.keys():
		if key != "points":
			bracket[key] = set(bracket[key])
			results[key] = set(results[key])
			points += rounds_points[key] * len(bracket[key] & results[key])
	return points

def get_so_far(url):
	bracket = {"64": [], "32": [], "16": [], "8": [], "4": [], "2": [], "1": []}

	data = requests.get(url)
	print(url)

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
			team_to_seed[team2] = seed_order[index+1]
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
	# print(mydivs)
	if len(mydivs) == 0:
		mydivs = soup.find_all("span", {"class": "actual winner"})
	# print(mydivs)
	teams = mydivs[0].find_all("span", {"class": "name"})
	# print(teams)
	team1 = teams[0].text.strip()
	# team2 = teams[1].text.strip()
	bracket["1"].append("")

	bracket["points"] = 1920

	return bracket, team_to_seed

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
				return {'64': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], '32': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], '16': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], '8': ['1', '1', '1', '1', '1', '1', '1', '1'], '4': ['1', '1', '1', '1'], '2': ['1', '1'], '1': ['1'], 'points': 260}

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
		mydivs = soup.find_all("div", {"class": "slot wWinner userPickable"})
		teams = mydivs[0].find_all("span", {"class": "name"})
	team1 = teams[0].text.strip()
	team2 = teams[1].text.strip()
	bracket["1"].append(team2)
	if team1 == team2:
		bracket["points"] += 320

	return bracket

def get_group(group):
	IDs = []
	soup = BeautifulSoup(parse2(group))
	mydivs = soup.find_all("table", {"class": "type_entries"})
	entries = mydivs[0].find_all("a", {"class": "entry"})
	for entry in entries:
		IDs.append((entry.get('href'), entry.text.strip()))
	return IDs

def comp_brackets_other(results, brackets, round_index=0, index=0):
	bracket_scores = [[0 for x in range(len(brackets))] for y in range(len(brackets))]
	if results["1"][0] != '':
		ordered = []
		results_copy = results.copy()
		for b in range(len(brackets)):
			bracket = brackets[b]
			score = score_bracket(bracket, results_copy)
			ordered.append((b, score))
		ordered = sorted(ordered, key= lambda x: x[1], reverse=True)
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

def comp_brackets_other_weighted(results, brackets, team_to_seed, round_index=0, index=0, liklihood = 1):
	bracket_scores = [[0 for x in range(len(brackets))] for y in range(len(brackets))]
	if results["1"][0] != '':
		ordered = []
		results_copy = results.copy()
		for b in range(len(brackets)):
			bracket = brackets[b]
			score = score_bracket(bracket, results_copy)
			ordered.append((b, score))
		ordered = sorted(ordered, key= lambda x: x[1], reverse=True)
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
			branch1 = comp_brackets_other_weighted(results_copy, brackets, team_to_seed, next_round_index, next_index, liklihood * update)

			results_copy = copy.deepcopy(results)
			results_copy[rounds[round_index]][index] = options[1]
			update = seed_vs_seed[team_to_seed[options[1]]][team_to_seed[options[0]]]
			branch2 = comp_brackets_other_weighted(results_copy, brackets, team_to_seed, next_round_index, next_index, liklihood * update)
			total_branch = np.add(branch1, branch2)
			return total_branch
		else:
			return comp_brackets_other_weighted(results, brackets, team_to_seed, next_round_index, next_index, liklihood)

IDs = get_group(dad_group)

# IDs = [('entry?entryID=45713262', 'Aidansg'), ('entry?entryID=43978522', 'sanersully'),
# 	   ('entry?entryID=43512529', 'mgsully65 1'), ('entry?entryID=46065031', 'low risk low reward'),
# 	   ('entry?entryID=42007304', 'Cgilly61 1'), ('entry?entryID=38023192', 'Ameliasg97 1'),
# 	   ('entry?entryID=37600596', 'smgilson 1'), ('entry?entryID=43377775', 'KMG2021'),
# 	   ('entry?entryID=43902748', 'TGilly'), ('entry?entryID=38025176', 'JMGilly_1')]

print(base_bracket_url + IDs[0][0])
results, team_to_seed = get_so_far(base_bracket_url + IDs[0][0])

print(results)
print(team_to_seed)

# print(team_to_seed)

# aidan = {'64': ['Gonzaga', 'Norfolk St', 'Oklahoma', 'Missouri', 'Creighton', 'UCSB', 'Virginia', 'Ohio', 'USC', 'Drake', 'Kansas', 'E Washington', 'Oregon', 'VCU', 'Iowa', 'Grand Canyon', 'Michigan', 'Texas Southern', 'LSU', 'St. Bonaventure', 'Colorado', 'Georgetown', 'Florida State', 'UNC Greensboro', 'BYU', 'UCLA', 'Texas', 'Abil Christian', 'UConn', 'Maryland', 'Alabama', 'Iona', 'Baylor', 'Hartford', 'North Carolina', 'Wisconsin', 'Villanova', 'Winthrop', 'Purdue', 'North Texas', 'Texas Tech', 'Utah State', 'Arkansas', 'Colgate', 'Florida', 'Virginia Tech', 'Ohio State', 'Oral Roberts', 'Illinois', 'Drexel', 'Loyola Chicago', 'Georgia Tech', 'Tennessee', 'Oregon State', 'Oklahoma State', 'Liberty', 'San Diego State', 'Syracuse', 'West Virginia', 'Morehead State', 'Clemson', 'Rutgers', 'Houston', 'Cleveland State'], '32': ['Gonzaga', 'Missouri', 'Creighton', 'Virginia', 'USC', 'Kansas', 'Oregon', 'Iowa', 'Michigan', 'St. Bonaventure', 'Georgetown', 'Florida State', 'BYU', 'Texas', 'Maryland', 'Alabama', 'Baylor', 'North Carolina', 'Villanova', 'North Texas', 'Texas Tech', 'Arkansas', 'Virginia Tech', 'Ohio State', 'Illinois', 'Georgia Tech', 'Tennessee', 'Oklahoma State', 'Syracuse', 'West Virginia', 'Rutgers', 'Houston'], '16': ['Gonzaga', 'Creighton', 'USC', 'Iowa', 'Michigan', 'Florida State', 'BYU', 'Alabama', 'Baylor', 'Villanova', 'Texas Tech', 'Ohio State', 'Illinois', 'Tennessee', 'Syracuse', 'Houston'], '8': ['Gonzaga', 'USC', 'Michigan', 'Alabama', 'Baylor', 'Ohio State', 'Illinois', 'Houston'], '4': ['Gonzaga', 'Alabama', 'Baylor', 'Houston'], '2': ['Gonzaga', 'Houston'], '1': ['Gonzaga'], 'points': 410}
# robbie = {'64': ['Gonzaga', 'Norfolk St', 'Oklahoma', 'Missouri', 'Creighton', 'UCSB', 'Virginia', 'Ohio', 'USC', 'Drake', 'Kansas', 'E Washington', 'Oregon', 'VCU', 'Iowa', 'Grand Canyon', 'Michigan', 'Texas Southern', 'LSU', 'St. Bonaventure', 'Colorado', 'Georgetown', 'Florida State', 'UNC Greensboro', 'BYU', 'UCLA', 'Texas', 'Abil Christian', 'UConn', 'Maryland', 'Alabama', 'Iona', 'Baylor', 'Hartford', 'North Carolina', 'Wisconsin', 'Villanova', 'Winthrop', 'Purdue', 'North Texas', 'Texas Tech', 'Utah State', 'Arkansas', 'Colgate', 'Florida', 'Virginia Tech', 'Ohio State', 'Oral Roberts', 'Illinois', 'Drexel', 'Loyola Chicago', 'Georgia Tech', 'Tennessee', 'Oregon State', 'Oklahoma State', 'Liberty', 'San Diego State', 'Syracuse', 'West Virginia', 'Morehead State', 'Clemson', 'Rutgers', 'Houston', 'Cleveland State'], '32': ['Gonzaga', 'Missouri', 'Creighton', 'Virginia', 'Drake', 'Kansas', 'VCU', 'Iowa', 'Michigan', 'St. Bonaventure', 'Georgetown', 'Florida State', 'UCLA', 'Texas', 'Maryland', 'Alabama', 'Baylor', 'Wisconsin', 'Villanova', 'Purdue', 'Utah State', 'Arkansas', 'Virginia Tech', 'Ohio State', 'Illinois', 'Georgia Tech', 'Tennessee', 'Oklahoma State', 'Syracuse', 'West Virginia', 'Rutgers', 'Houston'], '16': ['Gonzaga', 'Creighton', 'Kansas', 'Iowa', 'Michigan', 'Georgetown', 'Texas', 'Alabama', 'Baylor', 'Villanova', 'Arkansas', 'Ohio State', 'Illinois', 'Oklahoma State', 'Syracuse', 'Houston'], '8': ['Gonzaga', 'Iowa', 'Michigan', 'Texas', 'Baylor', 'Arkansas', 'Oklahoma State', 'Houston'], '4': ['Gonzaga', 'Michigan', 'Arkansas', 'Oklahoma State'], '2': ['Gonzaga', 'Arkansas'], '1': ['Arkansas'], 'points': 370}
#
# IDs = [aidan, robbie]


brackets = []
for x in range(len(IDs)):
	print(IDs[x])
	bracket = get_bracket(base_bracket_url + IDs[x][0])
	print(bracket)
	brackets.append(bracket)


# total = comp_brackets_other_weighted(results, brackets, team_to_seed)
# total = np.array(total) *100
total = comp_brackets_other(results, brackets)
total = total / np.sum(total[0]) * 100


# columns = ["1st", "2nd"]
columns = ["1st", "2nd", "3rd"]
for x in range(3, len(IDs)):
	columns.append(str(x+1)+"th")
rows = [entry[1] for entry in IDs]

df = pd.DataFrame(total, columns = columns, index = rows)
#
df.to_excel("DadAlwaysWins2022_elite8.xlsx")
# df.to_excel("YSM_Class_of_2023_2.xlsx")