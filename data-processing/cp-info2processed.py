from cgi import test
from glob import glob
import shutil

for test_group in glob('data/raw/*/metrics*.csv'):
    print(test_group)
    dst = test_group.replace('raw', 'processed/hw-study')
    shutil.copyfile(test_group, dst)

for test_group in glob('data/raw/*/hardware*.json'):
    print(test_group)
    dst = test_group.replace('raw', 'processed/hw-study')
    shutil.copyfile(test_group, dst)