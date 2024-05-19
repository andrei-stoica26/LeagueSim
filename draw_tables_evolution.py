import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def find_ordered_teams(input_file, folder_path):
    #Gets the team names from the final standings for plotting purposes
    df = pd.read_excel(input_file, header = 0)
    n_teams = len(df.iloc[:, 0])
    n_rounds = 2 * n_teams - 2
    with open(f'{folder_path} {n_rounds}.txt') as f:
        #Split by final round number, discard the second element, and then extract the team name
        teams = [' '.join(x.split(str(n_rounds))[0].split()[1:])
                          for x in f.read()[:-1].split('\n')]
    return(teams)  

def find_positions(folder_path, teams):
    positions = {key: [] for key in teams}
    n_rounds = 2 * len(teams) - 2
    for i in range(1, n_rounds + 1):
        with open(f'{folder_path} {i}.txt') as f:
            table = [x.replace('.', '').split()
                          for x in f.read()[:-1].split('\n')]
        for line in table:
            #Recover team names by joining the list except the last 8 elements and the first one
            #The first element: team ranking
            #The last 8 elements: matches, wins, draws, losses, goals scored, goals conceded, goal difference, points
            positions[' '.join(line[1:-8])].append(int(line[0]))
    return(positions)

def draw_tables_evolution(input_file, folder_path, image_folder_path):
    teams = find_ordered_teams(input_file, folder_path)
    positions = find_positions(folder_path, teams)
    plt.figure(figsize=(15, 10))
    for team in positions:
        plt.plot(positions[team], label = team, lw = 1, marker='o', markersize = 5)
    plt.xlabel('Round number')
    plt.ylabel('Position')
    plt.title('Tables evolution')
    plt.gca().invert_yaxis()
    plt.yticks(range(1, len(positions) + 1), range(1, len(positions) + 1))
    plt.xticks(range(0, 2 * len(positions) - 2), range(1, 2 * len(positions) - 1))
    plt.legend(loc='upper right', bbox_to_anchor=(1.15, 1), borderaxespad=0.)
    plt.tight_layout()
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)
    plt.savefig(f'{image_folder_path}/Position changes.png', dpi=300,
                bbox_inches='tight')
        
def main():
    input_file = 'Raw data/PL2223.xlsx'
    folder_path = 'Tables/Round'
    image_folder_path = 'Images'
    print('Plotting the evolution of league standings...')
    draw_tables_evolution(input_file, folder_path, image_folder_path)

if __name__ == "__main__":
    main()
