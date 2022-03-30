from glob import glob
from sys import argv
import wmi
from os.path import basename, splitext, isdir


# Get all running process
ti = 0
f = wmi.WMI()
processes = f.Win32_Process()
# Get each process name to kill
for process in processes:
    print(process.name)
