import pandas as pd
import sqlite3


df = pd.read_csv('../data_files/steam_games_v1')

# create and connect to database
conn = sqlite3.connect('../database/steam_data_v2.db')
curs = conn.cursor()

# create sql command
df_columns = df.columns
column_names = ','.join(df_columns)

curs.execute(f'CREATE TABLE GAMES ({column_names})')

# df to sql
df.to_sql('GAMES', conn, if_exists='replace', index=False)



curs.close()
