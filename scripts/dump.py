import json
import game_def

with open("game_def.json", "w") as outfile:
    json.dump(game_def.allGames(), outfile)