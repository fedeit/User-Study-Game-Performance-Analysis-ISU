import test_gui
import datetime
import time
import pandas as pd
import json
import get_hw
import ohm_utils
import cloud_upload

time.sleep(4)

# Timestamp used for all files
execution_time = datetime.datetime.utcnow().strftime("%m-%d-%y_%H-%M-%S")

# Define path constants
HARDWARE_LOG_PATH = './results/hardware_log_' + execution_time + '.csv'
HARDWARE_INFO_PATH = './results/hardware_' + execution_time + '.json'
METRICS_PATH = './results/metrics_' + execution_time + '.json'

# Get hardware info and dump to file
hardware = get_hw.getHardwareInfo()
with open(HARDWARE_INFO_PATH, 'w+') as f:
    json.dump(hardware, f)

# Start OpenHardwareMonitor
ohm_utils.killOHM()
ohm_utils.runOHM()

# Below are all of the different params for each game
hearthstone = {
    'name' : 'Hearthstone',
    'params' : {
        'move_time' : 0.0,
        'kill_mode' : 'os',
        'process_name' : ['Hearth', 'Battle'],
        'window_names': ['Battle.net', 'Hearthstone']
    },
    'times_load': [2, 1],
    'times_level': [3, 2]
}

fortnite = {
    'name' : 'Fortnite',
    'params' : {
        'move_time' : 0.0,
        'kill_mode' : 'keyboard',
        'window_names': []
    },
    'times_load': [1, 0],
    'times_level': [3, 2]
}

leagueOfLegends = {
    'name' : 'LoL',
    'params' : {
        'move_time' : 0.0,
        'kill_mode' : 'os',
        'move_time': 0.5,
        'process_name' : ['League'],
        'window_names': ['Riot Client Main', 'League of Legends'],
    },
    'times_load': [0, 0],
    'times_level': [0, 0]
}

minecraft = {
    'name' : 'Minecraft',
    'params' : {
        'window_names': ['Minecraft Launcher', 'Minecraft 1.18.1'],
        'move_time' : 0.0,
        'kill_mode' : 'keyboard'
    },
    'times_load': [2, 1],
    'times_level': [4, 3]
}

apex = {
    'name' : 'Apex',
    'params' : {
        'move_time' : 0.0,
        'kill_mode' : 'keyboard',
        'window_names': ['Apex Legends'],
    },
    'times_load': [2, 0],
    'times_level': [4, 3]
}

csgo = {
    'name' : 'CSGO',
    'params' : {
        'process_name' : ['csgo.exe'],
        'move_time': 0.5,
        'kill_mode' : 'os',
        'window_names': ['Counter-Strike: Global Offensive']
    },
    'times_load': [2, 1],
    'times_level': [5, 4]
}

# games we want to run
games = [minecraft, csgo, apex, hearthstone]
# how many iterations
iterations = 10

df = pd.DataFrame(columns=['game_name', 'game_params', 'init_time', 'total_time', 'times'])

# iterate through all of the games 
for game in games:
    times = []
    for i in range(iterations): # iterate through how many trials we want to test
        print(f'[INFO] Iteration {i + 1} @ {datetime.datetime.utcnow().strftime("%H:%M:%S")}') # print out current date and iteration
        metrics = test_gui.test(game['name'], game['params']) # get game specific metrics
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
        print(f'[INFO] Waiting 10 seconds')
        time.sleep(10)

# dump to json for later
df.to_json(METRICS_PATH)

# Kill Open Hardware Monitor and move log to new path
ohm_utils.killOHM()
time.sleep(2)
ohm_utils.moveLatestLog(HARDWARE_LOG_PATH)

# Upload everything to the cloud
cloud_upload.uploadFile(METRICS_PATH)
cloud_upload.uploadFile(HARDWARE_INFO_PATH)
cloud_upload.uploadFile(HARDWARE_LOG_PATH)
