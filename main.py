import json
import pandas as pd
from collections import defaultdict

data = open("database.json")

steam_games = json.load(data)

features = ["name", "publishers"]
def get_values_for_one_game(data: json, values: list) -> pd.DataFrame:
    ids = data.keys()

    dct = {"id":ids}

    for value in values:
        lst = []
        for id in ids:
            lst.append(steam_games[id][value])
        dct[value] = lst

    return pd.DataFrame(dct)

df = get_values_for_one_game(steam_games, features)

