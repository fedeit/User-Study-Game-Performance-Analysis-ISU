import pandas as pd
from glob import glob
import os

print('Starting json2csv.py')
for test_group in glob('data/raw/*/metrics_*.json'):
    print(test_group)
    try:
        append_file = list(glob(os.path.dirname(test_group) + '/append_metrics*.json'))[0]
        x2 = pd.read_json(append_file)
    except: print('Could not find append file')
    x = pd.read_json(test_group)
    x = pd.concat([x, x2])
    x.reset_index(inplace=True)
    x = x.rename(columns = {'index':'iteration'})
    x['iteration'] = x['iteration'] % 10
    x['init_time'] = x['init_time'].dt.tz_localize("UTC").dt.tz_convert("America/New_York")
    test_group = test_group.replace('.json', '.csv')
    x.to_csv(test_group)
print('Completed json2csv.py')