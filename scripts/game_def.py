
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
        'process_name' : ['Fortnite'],
        'window_names': []
    },
    'times_load': [1, 0],
    'times_level': [3, 2]
}

leagueOfLegends = {
    'name' : 'LoL',
    'params' : {
        'move_time' : 0.0,
        'kill_mode' : 'None',
        'window_names': ['Riot Client Main', 'League of Legends'],
        'no_fullscreen': True
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

r6 = {
    'name' : 'R6',
    'params' : {
        'move_time': 0.5,
        'kill_mode' : 'None',
        'window_names': ['Rainbow Six']
    },
    'times_load': [1, 0],
    'times_level': [8, 6]
}

civV = {
    'name' : 'CivV',
    'params' : {
        'move_time': 0.5,
        'kill_mode' : 'None',
        'window_names': ['Civilization V']
    },
    'times_load': [2, 1],
    'times_level': [5, 4]
}

civVI = {
    'name' : 'CivVI',
    'params' : {
        'move_time': 0.5,
        'kill_mode' : 'None',
        'window_names': ['Sid Meier\'s Civilization VI (DX12)']
    },
    'times_load': [4, 1],
    'times_level': [8, 6]
}

gta = {
    'name' : 'GTA5',
    'params' : {
        'move_time': 0.5,
        'kill_mode' : 'None',
        'window_names': ['Grand Theft Auto V']
    },
    'times_load': [1, 0],
    'times_level': [2, 1]
}

overwatch = {
    'name' : 'Overwatch',
    'params' : {
        'move_time': 0.5,
        'kill_mode' : 'keyboard',
        'window_names': ['Overwatch']
    },
    'times_load': [2, 1],
    'times_level': [6, 2]
}

pubg = {
    'name' : 'PUBG',
    'params' : {
        'move_time': 0.5,
        'kill_mode' : 'keyboard',
        'window_names': ['PLAYER UNKOWN\'S BATTLEGROUNDS']
    },
    'times_load': [1, 0],
    'times_level': [2, 1]
}

assassincreed = {
    'name' : 'AssassinCreed',
    'params' : {
        'move_time': 0.5,
        'kill_mode' : 'keyboard',
        'window_names': ['Assassin\'s Creed® Odyssey']
    },
    'times_load': [1, 0],
    'times_level': [3, 2]
}

def allGames():
    #return [gta]
    return [pubg, civVI, hearthstone, fortnite, minecraft, apex, csgo, r6, overwatch]
