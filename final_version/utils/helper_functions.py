import sqlite3

import pandas as pd
import streamlit as st



def display_os(conn):
    curs = conn.cursor()
    command = '''
        SELECT GAMES.name, PLATFORMS.name
        FROM GAMES
        join GAMES_PLATFORMS
        on GAMES.id = GAMES_PLATFORMS.game_id
        join PLATFORMS
        on GAMES_PLATFORMS.platform_id = PLATFORMS.id
    '''
    curs.execute(command)
    result = curs.fetchall()

    games = []
    os = []
    for row in result:
        games.append(row[0])
        os.append(row[1])

    oses = pd.DataFrame({
        'game_name': games,
        'os': os
    })
    indexes = []
    for ind, row in oses.iterrows():
        if row.game_name.startswith('Tom Cl'):
            indexes.append(ind)

    for index in indexes:
        oses.drop(index=index, inplace=True)
    oses = oses[oses.game_name != 'Bounce']
    print(oses.value_counts())
    oses = oses.reset_index(drop=True)
    oses_pivot = oses.pivot(index='game_name', columns='os', values='os')
    oses_pivot = oses_pivot.fillna('')
    oses_pivot = oses_pivot.replace({
        'windows': 'yes', 'linux': 'yes' , 'mac': 'yes'
    })
    oses_pivot = oses_pivot[['windows', 'linux', 'mac']]
    print(oses_pivot)

    st.dataframe(data=oses_pivot, width=None, height=None)
