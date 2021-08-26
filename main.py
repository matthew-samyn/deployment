import json
import pandas as pd
import sqlite3

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
print(df.shape)
print(df.isna().any())
df = df.drop_duplicates("id")
print(df.shape)

df.to_csv("steam_games_v1")





