import pandas as pd
from glob import glob
import os
import ast
import process_trial

print('Recomputing times')
for test_group in glob('data/raw/*/metrics_*.csv'):
    print(test_group)
    df = pd.read_csv(test_group)
    for index, row in df.iterrows():
        game = process_trial.getGame(row['game_name'])
        times = ast.literal_eval(row['times'])
        level = times[game['times_level'][0]] - times[game['times_level'][1]] # get game level load time
        df.at[index, 'level'] = level
        load = times[game['times_load'][0]] - times[game['times_load'][1]] # get game load time.
        df.at[index, 'load'] = load
    df.to_csv(test_group)
print('Done recomputing times')