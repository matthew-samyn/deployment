import sqlite3
import streamlit as st
import plotly.express as px

conn = sqlite3.connect('steam_data_v2_1.db')
curs = conn.cursor()

# All Game Names
curs.execute('''
SELECT name, id
FROM Games
;''')

list_games_query = curs.fetchall()

list_games = []
for game_name in list_games_query:
    list_games.append(game_name[0])

list_id = []
for game_name in list_games_query:
    list_id.append(game_name[1])

#print(list_games)
#print(list_id)


# Streamlit
st.title("Steam Dashboard 🎮")

box_1 = st.sidebar.selectbox('What do you want to do?',
                                    ('Analyse one game', 'Compare two games', 'Compare all games'))

if box_1 == 'Analyse one game':
    box_1_1 = st.sidebar.selectbox('Select the game',
                                   list_games)

    box_1_2 = st.sidebar.selectbox('Select desired feature',
                                   (['Reviews']))
    if box_1_2 == 'Reviews':
        query = f'SELECT total_positive, total_negative FROM Games WHERE Games.name = ?'
        params = [box_1_1]
        curs.execute(query, params)

        fig = px.pie(values=curs.fetchone(), names=['Positive reviews', 'Negative reviews'])
        fig.update_layout(title_text=f'Reviews for {box_1_1}', title_x=0.5)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        st.plotly_chart(fig, use_container_width=True)

conn.close()