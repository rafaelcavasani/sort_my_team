from functools import reduce
import random

def sort_teams(request):
	goalkeeper = sorted(request.json["goalkeeper"], key=lambda k: k['importance'])
	defender = sorted(request.json["defender"], key=lambda k: k['importance'])
	sideway = sorted(request.json["sideway"], key=lambda k: k['importance'])
	midfield = sorted(request.json["midfield"], key=lambda k: k['importance'])
	striker = sorted(request.json["striker"], key=lambda k: k['importance'])

	team1, team2 = random_teams(goalkeeper, defender, sideway, midfield, striker)

	goalkeeper_team1 = list(filter(lambda x: (x["position"] == "goalkeeper"), team1))
	goalkeeper_team2 = list(filter(lambda x: (x["position"] == "goalkeeper"), team2))
	goalkeeper_diff = goalkeeper_team1[0]["importance"] - goalkeeper_team2[0]["importance"]
	balance = balance_calculate(goalkeeper_diff)
	line_team1 = list(filter(lambda x: (x["position"] != "goalkeeper"), team1))
	line_team2 = list(filter(lambda x: (x["position"] != "goalkeeper"), team2))
	imp_line_team1, imp_line_team2 = importance_calculate(line_team1, line_team2, balance)

	total_imp_team1, total_imp_team2 = importance_calculate(team1, team2, balance)
	total_imp = total_imp_team1 - total_imp_team2
	if total_imp != 0 or total_imp != 1 or total_imp != -1:
		while check_total_imp(team1, team2, balance) == False:
			positions = ["defender", "sideway", "midfield", "striker"]
			choice_position = random.choice(positions)
			team1, team2 = change_players(team1, team2, balance, choice_position)

	return { "team1": team1, "team2": team2 }

def importance_calculate(team1, team2, balance):
	total_team1 = 0 
	total_team2 = 0 
	for t in team1:
		total_team1 += t["importance"]
	for t in team2:
		total_team2 += t["importance"]
	if balance["team"] == "team1":
		total_team1 += balance["difference"]
	else:
		total_team2 += balance["difference"]
	return total_team1, total_team2

def random_teams(goalkeeper, defender, sideway, midfield, striker):
	team1 = []
	team2 = []
	team1, team2 = include_player(team1, team2, goalkeeper)
	team1, team2 = include_player(team1, team2, defender)
	team1, team2 = include_player(team1, team2, sideway)
	team1, team2 = include_player(team1, team2, midfield)
	team1, team2 = include_player(team1, team2, striker)
	return team1, team2

def include_player(team1, team2, players):
	count_team1 = 0
	count_team2 = 0
	for p in players:
		choice_team = random.choice([0,1])
		if choice_team == 0:
			if count_team1 < len(players) / 2:
				team1.append(p)
				count_team1 += 1
			else:
				team2.append(p)
				count_team2 += 1
		else:
			if count_team2 < len(players) / 2:
				team2.append(p)
				count_team2 += 1
			else:
				team1.append(p)
				count_team1 += 1
	
	return team1, team2

def check_total_imp(team1, team2, balance):
	total_team1, total_team2 = importance_calculate(team1, team2, balance)
	total_imp = total_team1 - total_team2
	if total_imp >= -1 and total_imp <= 1:
		return True
	else:
		return False
			
def change_players(team1, team2, balance, position):
	deleted_team1 = False
	most_importance = 3
	minor_importance = 2
	while deleted_team1 == False:
		for player in team1:
			if player["position"] == position:
				if balance["team"] == "team2":
					if player["importance"] <= minor_importance:
						player_removed_team1 = player
						team1.remove(player_removed_team1)
						deleted_team1 = True
						break
				else:
					if player["importance"] > most_importance:
						player_removed_team1 = player
						team1.remove(player_removed_team1)
						deleted_team1 = True
						break
		minor_importance += 1
		most_importance -= 1

	deleted_team2 = False
	most_importance = 3
	minor_importance = 2
	while deleted_team2 == False:
		for player in team2:
			if player["position"] == position:
				if balance["team"] == "team1":
					if player["importance"] <= minor_importance:
						player_removed_team2 = player
						team2.remove(player_removed_team2)
						deleted_team2 = True
						break
				else:
					if player["importance"] > most_importance:
						player_removed_team2 = player
						team2.remove(player_removed_team2)
						deleted_team2 = True
						break
		minor_importance += 1
		most_importance -= 1
			
	team1.append(player_removed_team2)
	team2.append(player_removed_team1)
	return team1, team2

def balance_calculate(goalkeeper_diff):
	balance = {"team": "", "difference": 0}
	if goalkeeper_diff != 0 and goalkeeper_diff != 1 and goalkeeper_diff != -1:
		if goalkeeper_diff > 0:
			balance["team"] = "team1"
		else:
			balance["team"] = "team2"
			
		balance["difference"] = abs(goalkeeper_diff) + 1
	else:
		balance["difference"] = abs(goalkeeper_diff)
	return balance