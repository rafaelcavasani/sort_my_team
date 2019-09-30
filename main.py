import random

goalkeeper = [{"name": "Edson", "position": "goalkeeper", "importance": 2},
              {"name": "Joãozinho", "position": "goalkeeper", "importance": 4}]
goalkeeper = sorted(goalkeeper, key=lambda k: k['importance'])

defender = [{"name": "Silvaca", "position": "defender", "importance": 1},
            {"name": "Raul", "position": "defender", "importance": 3}]
defender = sorted(defender, key=lambda k: k['importance'])

sideway = [{"name": "Caião", "position": "sideway", "importance": 2},
           {"name": "Fabinho", "position": "sideway", "importance": 3},
		   {"name": "Japa", "position": "sideway", "importance": 2},
           {"name": "Camila", "position": "sideway", "importance": 5}]
sideway = sorted(sideway, key=lambda k: k['importance'])

midfield = [{"name": "Longarezi", "position": "midfield", "importance": 5},
			{"name": "Cavasani", "position": "midfield", "importance": 4},
			{"name": "Bertola", "position": "midfield", "importance": 2},
			{"name": "Gabriel", "position": "midfield", "importance": 3}]
midfield = sorted(midfield, key=lambda k: k['importance'])

striker = [{"name": "Amanda", "position": "striker", "importance": 4},
		   {"name": "Banhato", "position": "striker", "importance": 2}]
striker = sorted(striker, key=lambda k: k['importance'])

def importance_calculate():
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
	return {"team1": total_team1, "team2": total_team2}

def include_player(players):
	count_team1 = 0
	count_team2 = 0
	importance_team1 = 0
	importance_team2 = 0

	for p in players:
		choice_team = random.choice([0,1])
		if choice_team == 0:
			if count_team1 < len(players) / 2:
				team1.append(p)
				count_team1 += 1
				importance_team1 += p["importance"]
			else:
				team2.append(p)
				count_team2 += 1
				importance_team2 += p["importance"]
		else:
			if count_team2 < len(players) / 2:
				team2.append(p)
				count_team2 += 1
				importance_team2 += p["importance"]
			else:
				team1.append(p)
				count_team1 += 1
				importance_team1 += p["importance"]
	
	return {"team1": importance_team1, "team2": importance_team2}

def check_total_imp():
	total = importance_calculate()
	total_imp = total["team1"] - total["team2"]
	if total_imp >= -1 and total_imp <= 1:
		return True
	else:
		return False

def balance_line_importance():
	while check_total_imp() == False:
		positions = ["defender", "sideway", "midfield", "striker"]
		choice_position = random.choice(positions)
		change_players(choice_position)
			
def change_players(position):
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

def balance_calculate():
	goalkeeper_diff = goalkeeper_imp["team1"] - goalkeeper_imp["team2"]
	if goalkeeper_diff != 0 and goalkeeper_diff != 1 and goalkeeper_diff != -1:
		if goalkeeper_diff > 0:
			balance["team"] = "team1"
		else:
			balance["team"] = "team2"
			
		balance["difference"] = abs(goalkeeper_diff) + 1
	else:
		balance["difference"] = abs(goalkeeper_diff)

team1 = []
team2 = []
balance = {"team": "", "difference": 0}

goalkeeper_imp = include_player(goalkeeper)
defender_imp = include_player(defender)
sideway_imp = include_player(sideway)
midfield_imp = include_player(midfield)
striker_imp = include_player(striker)

line_imp = {}
line_imp["team1"] = defender_imp["team1"] + sideway_imp["team1"] + midfield_imp["team1"] + striker_imp["team1"]
line_imp["team2"] = defender_imp["team2"] + sideway_imp["team2"] + midfield_imp["team2"] + striker_imp["team2"]

total_imp = (goalkeeper_imp["team1"] + line_imp["team1"]) - (goalkeeper_imp["team2"] + line_imp["team2"])
if total_imp != 0 or total_imp != 1 or total_imp != -1:
	balance_calculate()
	print(balance)
	balance_line_importance()

print("**************************************")
print("team 1: \n")
print(team1, importance_calculate())
print("\nteam 2: \n")
print(team2)
print("**************************************\n\n")