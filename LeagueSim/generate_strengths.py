import pandas as pd
import random
import os

def add_expected_goals(teams, goals, prop = 0.5):
    n_teams = len(teams)
    n_rounds = 2 * n_teams - 2
    expected_goals = goals / n_rounds
    var_factor = prop * min(expected_goals) #Introduces random variation in the number of expected goals
    variations = [random.uniform(-var_factor, var_factor) for _ in range(n_teams)]
    return [x + y for x, y in zip(expected_goals, variations)]
    
def generate_strengths(input_file, folder_path, output_path):
    df = pd.read_excel(input_file, header = 0)
    teams = df.iloc[:, 0] 
    goals_scored = df.iloc[:, 1] 
    goals_conceded = df.iloc[:, 2]
    exp_scored = add_expected_goals(teams, goals_scored)
    exp_conceded = add_expected_goals(teams, goals_conceded)
    data = {
        'Team': teams,
        'ExpScored': exp_scored,
        'ExpConceded': exp_conceded
    }

    df = pd.DataFrame(data)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    df.to_excel(output_path, index = False)

def main():
    input_file = 'Raw data/PL2223.xlsx'
    folder_path = 'Data'
    output_path = 'Data/PLexp.xlsx'
    print('Generating team strengths...')
    generate_strengths('Raw data/PL2223.xlsx', 'Data', 'Data/PLexp.xlsx')

if __name__ == "__main__":
    main()

