import pandas as pd
import json, os
from datetime import timedelta


f = open('data/game_def.json')
game_def = json.load(f)


def getHardwareLog(start_date, end_date, hwlogpath):
    df = pd.read_csv(hwlogpath, header=[1])
    df['Time'] = pd.to_datetime(df['Time']).dt.tz_localize("America/New_York")
    mask = (df['Time'] >= start_date) & (df['Time'] <= end_date)
    segment = df.loc[mask]
    return segment

def getGame(target):
    for game in game_def:
        if game['name'] == target: return game

def compute(trial, hwlogpath, index, platform):
    if not os.path.exists(f'data/processed/hw-study/{platform}/'):
        os.mkdir(f'data/processed/hw-study/{platform}/')
    trialStart = trial['init_time']
    
    idxLoad = getGame(trial['game_name'])['times_load']
    loadStart = trialStart + pd.Timedelta(seconds=trial['times'][idxLoad[1]])
    loadEnd = trialStart + pd.Timedelta(seconds=trial['times'][idxLoad[0]])

    hw_df = getHardwareLog(loadStart, loadEnd, hwlogpath)
    hw_df.to_csv(f'data/processed/hw-study/{platform}/{trial["game_name"]}-game-{trial["iteration"]}.csv')

    idxLevel = getGame(trial['game_name'])['times_level']
    levelStart = trialStart + pd.Timedelta(seconds=trial['times'][idxLevel[1]])
    levelEnd = trialStart + pd.Timedelta(seconds=trial['times'][idxLevel[0]])
    
    hw_df = getHardwareLog(levelStart, levelEnd, hwlogpath)
    hw_df.to_csv(f'data/processed/hw-study/{platform}/{trial["game_name"]}-level-{trial["iteration"]}.csv')