import csv
import pandas as pd
import os

def list_files_in_folder(folder_path):
    try:
        # Use os.listdir() to get a list of all files and directories in the folder
        files_and_directories = os.listdir(folder_path)

        # Filter out only the files (excluding directories)
        files = [f for f in files_and_directories if os.path.isfile(os.path.join(folder_path, f))]

        return files
    except OSError as e:
        print(f"Error reading folder {folder_path}: {str(e)}")
        return []


def combine_CSVs(folder, dest):
    files = list_files_in_folder(folder)
    df = pd.read_csv(f'{folder}/{files[0]}', encoding='utf-8')
    for file in files[1:]:
        df2 = pd.read_csv(f'{folder}/{file}', encoding='utf-8')
        df = pd.concat([df, df2], ignore_index=True)
    chunk_size = 1000
    num_rows = 0
    list_df = [df[i:i+chunk_size]
               for i in range(0,len(df),chunk_size)]
    
    for chunk in list_df:
        chunk.to_csv(dest, mode='a', header=(num_rows == 0), index=False)
        num_rows += min([chunk_size, len(chunk)])
        print(f'wrote {num_rows} rows')

def swap_teams(game_row_dict):
    d = {}
    skips = ['Team', 'Team Score',
             'Opponent', 'Opponent Score']
    for key, val in game_row_dict.items():
        if key not in skips:
            d[key] = val
    d['Team'] = game_row_dict['Opponent']
    d['Team Score'] = game_row_dict['Opponent Score']
    d['Opponent'] = game_row_dict['Team']
    d['Opponent Score'] = game_row_dict['Team Score']
    return d
    

def get_games_by_team():
    games = pd.read_csv('games/all_games.csv', encoding='utf-8')
    games = games.drop(columns=['Unnamed: 6', 'Notes'])
    games = games.rename(columns={'Visitor/Neutral': 'Opponent',
                                  'PTS': 'Opponent Score',
                                  'Home/Neutral': 'Team',
                                  'PTS.1': 'Team Score',
                                  'Unnamed: 7': 'Overtimes'})
    new_order = ['Date', 'Start (ET)', 'Team', 'Team Score',
                 'Opponent', 'Opponent Score',
                 'Overtimes', 'Attend.', 'Arena']
    games = games.reindex(columns=new_order)
    games_dict = games.to_dict('records')

    with open('games_by_team.csv', 'w', newline='') as csvfile:
        fieldnames = list(games)
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(games_dict)):
            writer.writerow(games_dict[i])
            writer.writerow(swap_teams(games_dict[i]))

    return





