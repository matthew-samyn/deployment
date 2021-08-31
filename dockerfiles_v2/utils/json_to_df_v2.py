import json
import pandas as pd
import sqlite3
from collections import OrderedDict

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 50)

# Opening JSON
with open("../../data_json/database.json", "r") as json_file:
    steam_games = json.load(json_file)

print(f"We have this many id's: {len(steam_games.keys())}")


# Getting easy-to-extract-features in dataframe
def get_features(key, games):
    ids = list(games.keys())
    column = []
    for id in ids:
        try:
            value = steam_games[str(id)][key]
            column.append(value)
        except KeyError:
            column.append(None)
    print(f"Column '{key}': {len(column)}")
    return column


easy_lst = ["name", "required_age", "is_free", "developers", "review_score",
            "total_positive", "total_negative", "total_reviews"]

features_dct = {"id": list(steam_games.keys())}
for column in easy_lst:
    features_dct[column] = get_features(column, steam_games)

df_easy = pd.DataFrame(features_dct)
df_easy["developers"] = df_easy["developers"].fillna(value="Unknown")
df_easy['developers'] = df_easy.developers.apply(lambda x: x[0])
df_easy['developers'] = df_easy.developers.replace("U", "Unknown")

# Getting genres and genre_id in dataframe
genres_dct = get_features("genres", steam_games)
genre_dct = OrderedDict()
for lst in genres_dct:
    if lst:
        for dictionary in lst:
            game_id = int(dictionary['id'])
            value = dictionary["description"]
            genre_dct[game_id] = value

df_genre = pd.DataFrame()
df_genre["id"] = list(genre_dct.keys())
df_genre["genre"] = list(genre_dct.values())
df_genre.sort_values("id", inplace=True)
df_genre.reset_index(inplace=True, drop=True)

# Getting all the genre_id for each game_id in dataframe
game_ids = []
genre_ids = []

for game_id in steam_games:
    try:
        for genres_dct in steam_games[game_id]["genres"]:
            game_ids.append(game_id)
            genre_ids.append(genres_dct["id"])
    except:
        continue
df_games_genre = pd.DataFrame({"game_id": game_ids, "genre_id": genre_ids})

# Writing dataframes to csv
df_games_genre.to_csv("../data_files/gamesid_genreid.csv", index=False)
df_genre.to_csv("../data_files/different_genres.csv", index=False)
df_easy.to_csv("../data_files/steam_games_v2.csv", index=False)
