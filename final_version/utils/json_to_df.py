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
    # print(f"Column '{key}': {len(column)}")
    return column


easy_lst = ["name", "required_age", "is_free", "developers", "review_score",
            "total_positive", "total_negative", "total_reviews", "header_image", "short_description"]

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
#df_games_genre.to_csv("data_files/gamesid_genreid.csv", index=False)
#df_genre.to_csv("data_files/different_genres.csv", index=False)
#df_easy.to_csv("data_files/steam_games_v2.csv", index=False)

# Price feature
def dealing_with_currencies(unformatted_price: str) -> float:
    price = 0
    if unformatted_price[0] == "$":
        price_str = price_formatted[1:].replace(',', '.').replace('--', '00')
        unrounded_price = float(price_str) * 0.85
        price += round(unrounded_price,2)
    elif unformatted_price[-1] == "€":
        price_str = price_formatted[:-1].replace(',', '.').replace('--', '00')
        price += float(price_str)
    elif unformatted_price[:4] == "CDN$":
        price_str = price_formatted[4:].replace(',', '.').replace('--', '00')
        unrounded_price = float(price_str) * 0.6642
        price += round(unrounded_price,2)
    elif unformatted_price[:3] == "CHF":
        price_str = price_formatted[3:].replace(',', '.').replace('--', '00')
        unrounded_price = float(price_str) * 0.93
        price += round(unrounded_price,2)
    elif unformatted_price[0] == "£":
        price_str = price_formatted[1:].replace(',', '.').replace('--', '00')
        unrounded_price = float(price_str) * 1.17
        price += round(unrounded_price,2)
    elif unformatted_price[0] == "₩":
        price_str = price_formatted[1:].replace(',', '').replace('--', '00')
        unrounded_price = float(price_str) * 0.00073
        price += round(unrounded_price,2)
    elif unformatted_price[-2:] == "zł":
        price_str = price_formatted[:-2].replace(',', '.').replace('--', '00')
        unrounded_price = float(price_str) * 0.22
        price += round(unrounded_price,2)
    elif unformatted_price[:2] == "RM":
        price_str = price_formatted[2:].replace(',', '.').replace('--', '00')
        unrounded_price = float(price_str) * 0.20
        price += round(unrounded_price,2)
    return price

overviews_dict = get_features("price_overview", steam_games)
game_ids = []
final_formatteds = []

for game_id in steam_games:
    try:
        discount = steam_games[game_id]["price_overview"]["discount_percent"]
        if discount == 0:
            price_formatted = steam_games[game_id]["price_overview"]["final_formatted"]
            price = dealing_with_currencies(price_formatted)
            final_formatteds.append(price)
        elif discount != 0:
            price_formatted = steam_games[game_id]["price_overview"]["initial_formatted"]
            price = dealing_with_currencies(price_formatted)
            final_formatteds.append(price)
        game_ids.append(game_id)
    except:
        game_ids.append(game_id)
        final_formatteds.append(0)


# Release date feature
release_date = []
for game_id in steam_games:
    release_date.append(steam_games[game_id]["release_date"]["date"])

df_price_date = pd.DataFrame(list(zip(game_ids, final_formatteds, release_date)), columns=['id', 'price', 'date'])
df_price_date['date'] = df_price_date['date'].str.replace('Mai','May')
df_price_date['date'] = df_price_date['date'].str.replace('lutego','January')
df_price_date['date'] = pd.to_datetime(df_price_date['date'])

# get out the platform and platform id's

platform_type = []
game_id_list = []
platform_boolean = []

for game_id in steam_games:
    counter = 0
    for platform_key in steam_games[game_id]['platforms']:
        platform_type.append(platform_key)
        game_id_list.append(game_id)
        # print(steam_games[game_id]['platforms'].values())
        # print(type(list(steam_games[game_id]['platforms'].values())))
        platform_boolean.append(list(steam_games[game_id]['platforms'].values())[counter])
        counter += 1

df_easy = pd.merge(df_easy, df_price_date, on='id')

platform_dct = {'game_id': game_id_list,
                'platform_id': platform_type,
                'booleans': platform_boolean
}

game_platforms = pd.DataFrame(platform_dct)
game_platforms = game_platforms[game_platforms.booleans == True]
game_platforms.reset_index(inplace=True, drop=True)
game_platforms = game_platforms.drop(columns = ['booleans'])

platforms_table = pd.DataFrame(
    {'id': [1, 2, 3],
     'name': ['windows', 'mac', 'linux']}
)
game_platforms['platform_id'] = game_platforms['platform_id'].replace({
    'windows': 1,
    'mac':2,
    'linux':3
})

# Adding estimation of sales numbers in df_easy
df_easy['year'] = pd.DatetimeIndex(df_easy['date']).year

def calculate_sales_for_one_game(series) -> int:
    copies = 0
    year = series["year"]
    total_reviews = series["total_reviews"]
    if year < 2014:
        copies += total_reviews * 60
    elif year >= 2014 and year <= 2016:
        copies += total_reviews * 50
    elif year == 2017:
        copies += total_reviews * 40
    elif year >= 2018 and year <= 2019:
        copies += total_reviews * 35
    elif year >= 2020:
        copies += total_reviews * 30
    return round(copies,2)

df_easy["copies_sold"] =  df_easy[["year","total_reviews"]].apply(lambda x: calculate_sales_for_one_game(x), axis=1)
df_easy.drop(["year"], inplace=True, axis=1)

# Writing dataframes to csv
df_games_genre.to_csv("../data_files/gamesid_genreid.csv", index=False)
df_genre.to_csv("../data_files/different_genres.csv", index=False)
df_easy.to_csv("../data_files/steam_games_final.csv", index=False)
game_platforms.to_csv('../data_files/game_platforms.csv', index=False)
platforms_table.to_csv('../data_files/platforms_table.csv', index=False)