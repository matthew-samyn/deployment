import pandas as pd
import sqlite3


df_games = pd.read_csv('../data_files/steam_games_final.csv')
df_games['date'] = pd.to_datetime(df_games['date'])
df_genres = pd.read_csv('../data_files/different_genres.csv')
df_games_genres_id = pd.read_csv('../data_files/gamesid_genreid.csv')
df_platforms_table = pd.read_csv('../data_files/platforms_table.csv')
df_game_platforms = pd.read_csv('../data_files/game_platforms.csv')


# create and connect to database
conn = sqlite3.connect('../database/steam_data_final.db')
curs = conn.cursor()

# create table games
list_games_columns = df_games.columns
games_column_names = ','.join(list_games_columns)
# print(games_column_names)
curs.execute('CREATE TABLE GAMES ('
             'id INTEGER PRIMARY KEY, '
             'name           TEXT,'
             'header_image   TEXT,'
             'short_description TEXT,'
             'price          REAL,'
             'date           TIMESTAMP,'
             'required_age   INTEGER,'
             'is_free        INTEGER,'
             'developers     TEXT,'
             'review_score   INTEGER,'
             'total_positive INTEGER,'
             'total_negative INTEGER,'
             'total_reviews  INTEGER,'
             'copies_sold    INTEGER);')

# df to sql
df_games.to_sql('GAMES', conn, if_exists='append', index=False)

# create table genre
list_genres_columns = df_genres.columns
genres_column_names = ','.join(list_genres_columns)
# print(genres_column_names)
curs.execute('CREATE TABLE GENRES ('
             'id    INTEGER PRIMARY KEY,'
             'genre TEXT);')

# df to sql
df_genres.to_sql('GENRES', conn, if_exists='append', index=False)

# create table games_genres
list_genres_games_columns = df_games_genres_id.columns
genres_games_column_names = ','.join(list_genres_games_columns)
command = 'CREATE TABLE GAMES_GENRES( ' \
          'game_id INTEGER,' \
          'genre_id INTEGER,' \
          f'PRIMARY KEY({genres_games_column_names}),' \
          f'FOREIGN KEY (game_id) REFERENCES GAMES (id),' \
          f'FOREIGN KEY (genre_id) REFERENCES GENRES (id)' \
          f');'

curs.execute(command)
# df to sql
df_games_genres_id.to_sql('GAMES_GENRES', conn, if_exists='append', index=False)


# create table platforms
# list_platforms_columns = df_platforms_table.columns
# platform_column_names = ','.join(list_platforms_columns)
# print(genres_column_names)
curs.execute('CREATE TABLE PLATFORMS ('
             'id    INTEGER PRIMARY KEY,'
             'name  TEXT);')
# df to sql
df_platforms_table.to_sql('PLATFORMS', conn, if_exists='append', index=False)


# create table games_platforms
# list_genres_games_columns = df_games_genres_id.columns
# genres_games_column_names = ','.join(list_genres_games_columns)
command = 'CREATE TABLE GAMES_PLATFORMS( ' \
          'game_id INTEGER,' \
          'platform_id INTEGER,' \
          'PRIMARY KEY(game_id, platform_id),' \
          'FOREIGN KEY (game_id) REFERENCES GAMES (id),' \
          'FOREIGN KEY (platform_id) REFERENCES PLATFORMS (id)' \
          ');'
curs.execute(command)
df_game_platforms.to_sql('GAMES_PLATFORMS', conn, if_exists='append', index=False)

# Adding Kitty Tactics
df_kitty_tactics_games = pd.read_csv("../data_files/kitty_tactics_GAMES.csv", sep=";")
df_kitty_tactics_games_genres = pd.read_csv("../data_files/kitty_tactics_GAMES_GENRES.csv")
df_kitty_tactics_games_platforms = pd.read_csv("../data_files/kitty_tactics_GAMES_PLATFORMS.csv")
df_kitty_tactics_games.to_sql('GAMES', conn, if_exists='append', index=False)
df_kitty_tactics_games_genres.to_sql('GAMES_GENRES', conn, if_exists='append', index=False)
df_kitty_tactics_games_platforms.to_sql('GAMES_PLATFORMS', conn, if_exists='append', index=False)

# try database query
# curs.execute('''
# SELECT GAMES.name, GAMES_GENRES.genre_id, GENRES.genre, GAMES.review_score
# FROM GAMES join GAMES_GENRES
# on GAMES.id = GAMES_GENRES.game_id
# join GENRES
# on GAMES_GENRES.genre_id = GENRES.id
#  ''')
#
# for row in curs.fetchall():
#     print(row)

curs.close()