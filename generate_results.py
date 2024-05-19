import pandas as pd
import random
import math
import os

def generate_round_robin(half1, half2):
    #This function needs an even number of teams
    n_teams = len(half1) + len(half2)
    if n_teams % 2:
        raise ValueError("The list must have an even number of elements.")
    rounds = n_teams - 1
    matches = []
    for i in range(rounds):
        round_matches = []
        for j in range(n_teams // 2):
            if i % 2: #Half of the teams will be home teams in even rounds, the other half will be home teams in odd rounds
                round_matches.append([half1[j], half2[j]])
            else:
                round_matches.append([half2[j], half1[j]])
        random.shuffle(round_matches)
        matches.append(round_matches)
        # Rotate half1 teams
        half1.insert(0, half1.pop(-1))
    return matches

def generate_fixtures(teams, symmetric = False):
    #This function needs an even number of teams
    n_teams = len(teams)
    if n_teams % 2:
        raise ValueError("The list must have an even number of elements.")
    random.shuffle(teams)
    half1 = teams[:n_teams // 2]
    half2 = teams[n_teams // 2:]
    #All teams play each other two times: a winter season and a summer season
    winter = generate_round_robin(half1, half2)
    if symmetric:
        summer = [[list(reversed(match)) for match in round_match] for round_match in winter]
    else:
        summer = generate_round_robin(half1, half2)
    return winter + summer

def print_schedule(schedule):
    for i, round in enumerate(schedule, 1):
        print(f"Round {i}:")
        for match in round:
            print(f"{match[0]} vs {match[1]}")
        print()

def generate_base_goals (exp_goals, team1, team2, var_factor):
    #The expected number of goals a team scores against another is the average of the two expected goals figures, plus a random variation component
    return (exp_goals.loc[team1]['ExpScored'] + exp_goals.loc[team2]['ExpConceded']) / 2 + random.uniform(-var_factor, var_factor)

def generate_goals (goals, prop = 0.9):
    #The number of scored goals a team scores against another is allowed to show a significant variation from the expected figure
    return round(random.uniform ((1 - prop) * goals, (1 + prop) * goals)) 
    
def generate_match_goals (exp_goals, match, min_goals, prop = 0.5):
    var_factor = min_goals * prop 
    base_home_goals = generate_base_goals(exp_goals, match[0], match[1], var_factor)
    base_away_goals = generate_base_goals(exp_goals, match[1], match[0], var_factor) 
    home_goals = generate_goals(base_home_goals)
    away_goals = generate_goals(base_away_goals)
    return [home_goals, away_goals]

def add_scores(schedule, exp_goals, prop = 0.1, adaptive = True):
    scores = []
    for i, round in enumerate(schedule, 1):
        round_results = []
        min_goals = exp_goals.min().min()
        for match in round:
            match_goals = generate_match_goals (exp_goals, match, min_goals, prop = 0.9)
            round_results.append([match[0], match_goals[0], match_goals[1], match[1]])
        scores.append(round_results)
        if (adaptive):
            #The expected goals figures for each team change slightly randomly after each round
            exp_goals['ExpScored'] = [x * random.uniform (1 - prop, 1 + prop) for x in exp_goals['ExpScored']]
            exp_goals['ExpConceded'] = [x * random.uniform (1 - prop, 1 + prop) for x in exp_goals['ExpConceded']]
    return scores

def print_results(results):
    for i, round in enumerate(results, 1):
        print(f'Round {i}:')
        for match in round:
            print(f'{match[0]} {match[1]} - {match[2]} {match[3]}')
        print()

def save_results(folder_path, output_path, results):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(output_path, 'w') as f:
        for i, round in enumerate(results, 1):
            f.write(f'Round {i}:\n')
            for match in round:
                f.write(f'{match[0]} {match[1]} - {match[2]} {match[3]}\n')
            f.write('\n')

def generate_results(input_path, folder_path, output_path):
    exp_goals = pd.read_excel(input_path, header = 0)
    exp_goals.set_index(exp_goals.columns[0], inplace = True)
    teams = list(exp_goals.index)
    n_teams = len(teams)
    schedule = generate_fixtures(teams, True)
    results = add_scores(schedule, exp_goals)
    save_results(folder_path, output_path, results)

def main():
    input_path = 'Data/PLexp.xlsx'
    folder_path = 'Scores'
    output_path = folder_path + '/all_match_results.txt'
    print('Generating fixtures and results...')
    generate_results(input_path, folder_path, output_path)

if __name__ == '__main__':
    main()


