import pandas as pd
import sqlite3


df_games = pd.read_csv('../data_files/steam_games_v2.csv')
df_genres = pd.read_csv('../data_files/different_genres.csv')
df_games_genres_id = pd.read_csv('../data_files/gamesid_genreid.csv')


# create and connect to database
conn = sqlite3.connect('../dockerfiles_v2/steam_data_v000000000.db')
curs = conn.cursor()

# create table games
list_games_columns = df_games.columns
games_column_names = ','.join(list_games_columns)
print(games_column_names)
curs.execute(f'CREATE TABLE GAMES ({games_column_names}, PRIMARY KEY (id))')
# df to sql
df_games.to_sql('GAMES', conn, if_exists='append', index=False)

# create table genre
list_genres_columns = df_genres.columns
genres_column_names = ','.join(list_genres_columns)
curs.execute(f'CREATE TABLE GENRES ({genres_column_names}, PRIMARY KEY (id))')
# df to sql
df_genres.to_sql('GENRES', conn, if_exists='append', index=False)

# create table games_genres
list_genres_games_columns = df_games_genres_id.columns
genres_games_column_names = ','.join(list_genres_games_columns)
command = f'CREATE TABLE GAMES_GENRES ({genres_games_column_names}, PRIMARY KEY({genres_games_column_names}), FOREIGN KEY (game_id) REFERENCES GAMES (id), FOREIGN KEY (genre_id) REFERENCES GENRES (id))'
curs.execute(command)

# df to sql
df_games_genres_id.to_sql('GAMES_GENRES', conn, if_exists='append', index=False)

curs.execute('''
SELECT 
    m.name
    , p.*
FROM
    sqlite_master m
    JOIN pragma_foreign_key_list(m.name) p ON m.name != p."table"
WHERE m.type = 'table'
ORDER BY m.name
;
'''
)
print(curs.fetchall())
for row in curs.fetchall():
    print(row)



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