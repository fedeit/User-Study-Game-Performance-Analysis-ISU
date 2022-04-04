from glob import glob
import pandas as pd
import process_trial
import json, os
from tqdm import tqdm

print(os.getcwd())
print('Process testset')

for test_group in tqdm(glob('data/raw/*/metrics_*.csv')):
    try:
        platform = test_group.split('/')[2]
        df = pd.read_csv(test_group)
        df['init_time'] = pd.to_datetime(df['init_time'])  
        df.reset_index(inplace=True)
        for index, row in df.iterrows():
            row['times'] = json.loads(row['times'])
            hw_log = test_group.replace('metrics_', 'hardware_log_')
            process_trial.compute(row, hw_log, index, platform)
    except:
        print(f'ERROR: {test_group}')
print('Process testset completed')