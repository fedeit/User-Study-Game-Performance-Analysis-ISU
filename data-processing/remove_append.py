from glob import glob
import os

for test_group in glob('data/raw/*/append_*'):
    print(test_group)
    os.remove(test_group)