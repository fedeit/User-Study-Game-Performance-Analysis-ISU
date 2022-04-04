from glob import glob
import os

for test_group in glob('data/raw/*/metrics_*.json'):
    print(test_group)
    os.remove(test_group)