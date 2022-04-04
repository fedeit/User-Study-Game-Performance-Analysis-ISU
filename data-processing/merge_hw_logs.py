import pandas as pd
from glob import glob
import os

print('Starting merge_hw_logs.py')
for test_group in glob('data/raw/*/hardware_log*.csv'):
    print(test_group)
    try:
        append_file = list(glob(os.path.dirname(test_group) + '/append_hardware_log*.csv'))[0]
        x2 = pd.read_csv(append_file, header=[0,1])
    except:
        print('Could not find append file')
        continue
    x = pd.read_csv(test_group, header=[0,1])
    x = pd.concat([x, x2])
    x.reset_index(inplace=True, drop=True)
    x.to_csv(test_group)
print('Completed merge_hw_logs.py')
