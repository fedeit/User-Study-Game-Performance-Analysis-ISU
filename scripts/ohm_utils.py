import subprocess
import time
import wmi
from glob import glob
import os
import win32gui
import win32con

ohm_exe_path = r'C:\Users\Bob\Desktop\OpenHardwareMonitor\OpenHardwareMonitor.exe'
ohm_log_path = r'C:\Users\Bob\Desktop\OpenHardwareMonitor\*.csv'

def runOHM():
    print('Executing OHM')
    subprocess.Popen([ohm_exe_path], shell=True)
    time.sleep(1)
    whnd = win32gui.FindWindow(None, 'Open Hardware Monitor')
    win32gui.ShowWindow(whnd, win32con.SW_MINIMIZE)

def killOHM():
    print('Killing OHM')
    # Get all running process
    f = wmi.WMI()
    processes = f.Win32_Process()
    # Check if any running process contains the target name
    for process in processes:
        if 'OpenHardwareMonitor' in process.name:
            # If need to kill the process, try to terminate
            try:
                process.Terminate()
            except:
                # Sometimes the process is already killed
                # because closing the game will close the launcher
                print("Process already killed")

def moveLatestLog(destination):
    print('Moving OHM log')
    logs =  glob(ohm_log_path)
    latest = logs[-1]
    os.rename(latest, destination)