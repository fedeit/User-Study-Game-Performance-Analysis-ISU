import pandas as pd
from glob import glob


for test_group in glob('data/raw/*/metrics_*.json'):
    print(test_group)
    x = pd.read_json(test_group)
    x['init_time'] += pd.Timedelta(hours=-4)
    test_group = test_group.replace('.json', '.csv')
    x.to_csv(test_group)