import test_gui
import datetime
import time
import pandas as pd
import json
import get_hw
import ohm_utils
import cloud_upload
import game_def
import mailer
import sys
import pyautogui
import pydirectinput

pyautogui.FAILSAFE = False
pydirectinput.FAILSAFE = False

# Timestamp used for all files
execution_time = datetime.datetime.utcnow().strftime("%m-%d-%y_%H-%M-%S")

# Define path constants
HARDWARE_LOG_PATH = './results/hardware_log_' + execution_time + '.csv'
HARDWARE_INFO_PATH = './results/hardware_' + execution_time + '.json'
METRICS_PATH = './results/metrics_' + execution_time + '.json'

# Get hardware info and dump to file
hardware = get_hw.getHardwareInfo()

# Start OpenHardwareMonitor
ohm_utils.killOHM()
ohm_utils.removeLog()
ohm_utils.runOHM()

# Get games from game_def file
# games = game_def.allGames()
games = game_def.allGames()
# how many iterations
iterations = 10

df = pd.DataFrame(columns=['game_name', 'game_params', 'init_time', 'total_time', 'times'])

startTime = time.time()

# iterate through all of the games 
for game in games:
    times = []
    iteration = -1
    while iteration < iterations - 1: # iterate through how many trials we want to test
        iteration += 1
        print(f'[INFO]========== Iteration {iteration + 1} @ {datetime.datetime.utcnow().strftime("%H:%M:%S")} ==========') # print out current date and iteration
        try:
            metrics = test_gui.test(game['name'], game['params'], iteration) # get game specific metrics
        except TimeoutError:
            e = sys.exc_info()
            mailer.notifyTimeout(str(e))
            while('y' not in input('Continue? y/n: ')): continue
            print(f'ALERT!: Restarting iteration {iteration + 1}')
            iteration -= 1
            continue
        except KeyboardInterrupt:
            exit(1)
        except:
            e = sys.exc_info()
            mailer.notifyError(str(e))
            exit(1)
        level = metrics['times'][game['times_level'][0]] - metrics['times'][game['times_level'][1]] # get game level load time
        load = metrics['times'][game['times_load'][0]] - metrics['times'][game['times_load'][1]] # get game load time.
        df = df.append({
            'game_name' : game['name'],
            'game_params' : game['params'],
            'init_time' : metrics['init_time'],
            'total_time' : metrics['total_time'],
            'load' : load,
            'level' : level,
            'times' : json.dumps(metrics['times']),
        }, ignore_index=True) # append all new data data into pandas and dataframe so we can see the data later
        # wait 10 seconds before the next game
        print(f'[INFO] Waiting 20 seconds')
        time.sleep(20)

print(f"Total Runtime: {str(time.time()-startTime)}")

# dump to json for later
df.to_json(METRICS_PATH)

# Kill Open Hardware Monitor and move log to new path
ohm_utils.killOHM()
time.sleep(2)
ohm_utils.moveLatestLog(HARDWARE_LOG_PATH)

# Dump hardware info
with open(HARDWARE_INFO_PATH, 'w+') as f:
    json.dump(hardware, f)
    
# Upload everything to the cloud
cloud_upload.uploadFile(METRICS_PATH)
cloud_upload.uploadFile(HARDWARE_INFO_PATH)
cloud_upload.uploadFile(HARDWARE_LOG_PATH)

# sending email for completetion
mailer.notifyCompletion()
