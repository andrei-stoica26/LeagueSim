import pandas as pd
import os

def spaced_string (x, n_spaces):
    s = str(x)
    return ' ' * (n_spaces - len(s)) + s

def spaced_list (lx, n_spaces = 6):
    s = ''
    for x in lx:
        s += spaced_string(x, n_spaces)
    return s

def split_match(match):
    match = match.split(' - ') #Match format: Team 1 (can contain spaces) int - int Team 2 (can contain spaces)
    match = [x.split(' ') for x in match]
    #Everything except the last element for the home team and the first one for the away team (i.e. the scores) is joined to recover team names
    return [' '.join(match[0][:-1]), int(match[0][-1]), int(match[1][0]), ' '.join(match[1][1:])]
    
class FootballTeam:
    def __init__(self, name, wins = 0, draws = 0, defeats = 0, goals_scored = 0, goals_conceded = 0):
        self.name = name
        self.wins = wins
        self.draws = draws
        self.defeats = defeats
        self.goals_scored = goals_scored
        self.goals_conceded = goals_conceded
        self.matches = wins + draws + defeats
        self.goal_difference = goals_scored - goals_conceded
        self.points = (wins * 3) + (draws * 1)

    def update_stats(self, goals_scored = 0, goals_conceded = 0):
        self.wins += (goals_scored > goals_conceded)
        self.draws += (goals_scored == goals_conceded)
        self.defeats += (goals_scored < goals_conceded)
        self.goals_scored += goals_scored
        self.goals_conceded += goals_conceded
        self.matches = self.wins + self.draws + self.defeats
        self.goal_difference = self.goals_scored - self.goals_conceded
        self.points = (self.wins * 3) + (self.draws * 1)
        
    def __str__(self):
        spaces = " " * (20 - len(self.name))
        return self.name + spaces + spaced_list([self.matches, self.wins, self.draws, self.defeats, self.goals_scored, self.goals_conceded, self.goal_difference, self.points])

class FootballTable:
    def __init__(self):
        self.teams = {}

    def add_team(self, team_name):
        if team_name not in self.teams:
            self.teams[team_name] = FootballTeam(team_name)

    def update_team_stats(self, team_name, goals_scored = 0, goals_conceded = 0):
            self.teams[team_name].update_stats(goals_scored, goals_conceded)
                                                  
    def print_table(self):
        sorted_teams = sorted(self.teams.values(), key=lambda x: (x.points, x.goal_difference, x.goals_scored), reverse = True)
        for idx, team in enumerate(sorted_teams, start=1):
            print(' ' * (idx < 10) + f"{idx}. {team}")
    def write_table (self, file_path):
        sorted_teams = sorted(self.teams.values(), key=lambda x: (x.points, x.goal_difference, x.goals_scored), reverse = True)
        with open(file_path, 'w') as f:
            for idx, team in enumerate(sorted_teams, start=1):
                f.write(' ' * (idx < 10) + f"{idx}. {team}\n") #An extra space is added for teams ranked 1 to 9 for alignment purposes
    
def create_league(teams_path, scores_path, folder_path):
    exp_goals = pd.read_excel(teams_path, header = 0)
    exp_goals.set_index(exp_goals.columns[0], inplace = True)
    teams = list(exp_goals.index)
    table = FootballTable()
    for x in teams:
        table.add_team(x)
    with open(scores_path) as f:
        rounds = f.read()
    rounds = rounds.split('\n\n')[:-1] #Removing an empty round at the end
    n_matches = len(rounds[0]) - 1
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for i, r in enumerate(rounds, start = 1):
        round_matches = r.split('\n')[1:]
        for match in round_matches:
            result = split_match(match)
            table.update_team_stats(result[0], result[1], result[2])
            table.update_team_stats(result[3], result[2], result[1])
        table.write_table(f'Tables/Round {i}.txt') 

def main():
    teams_path = "Data/PLexp.xlsx"
    scores_path = "Scores/all_match_results.txt"
    folder_path = 'Tables'
    print('Creating league tables...')
    create_league(teams_path, scores_path, folder_path)

if __name__ == '__main__':
    main()
