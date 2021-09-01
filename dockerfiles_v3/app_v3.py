import sqlite3
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import random
from PIL import Image

conn = sqlite3.connect('./database/steam_data_v3.db')
curs = conn.cursor()

# All Game Names
curs.execute('''
SELECT name, id
FROM Games
ORDER BY name ASC
;''')

list_games_query = curs.fetchall()

list_games = []
for game_name in list_games_query:
    list_games.append(game_name[0])

list_id = []
for game_name in list_games_query:
    list_id.append(game_name[1])

# Streamlit
image = Image.open('steam_logo.png')

st.sidebar.title("Steam Dashboard")
box_1 = st.sidebar.selectbox('What do you want to analyze?', ('Select', 'Single game', 'Two games', 'All games'))

if box_1 == 'Select':
    st.image(image)

elif box_1 == 'Single game':
    # if users want to use random
    if st.sidebar.button('Random'):
        box_1_1 = st.sidebar.selectbox('Select game', [random.choice(list_games)])
        new_list = list(list_games)
        # if user wants to reset
        if st.sidebar.button('Reset'):
            box_1_1 = st.sidebar.selectbox('Select game', list_games)
            new_list = list(list_games)

    # if user selects on his own
    else:
        box_1_1 = st.sidebar.selectbox('Select game', list_games)
        new_list = list(list_games)

    box_1_2 = st.sidebar.selectbox('Select desired feature', (['Select', 'Reviews']))

    # Description
    descr = conn.cursor()
    query = f'SELECT short_description FROM Games WHERE Games.name = ?'
    params = [box_1_1]
    descr.execute(query, params)

    # Image
    img = conn.cursor()
    query = f'SELECT header_image FROM Games WHERE Games.name = ?'
    params = [box_1_1]
    img.execute(query, params)

    # id
    id_query = conn.cursor()
    query = f'SELECT id FROM Games WHERE Games.name = ?'
    params = [box_1_1]
    id_query.execute(query, params)

    if box_1_2 == 'Select':
        link_steam = f"https://store.steampowered.com/app/{id_query.fetchone()[0]}/"
        col1, col2, col3 = st.columns([1, 6, 1])
        with col1:
            st.write("")
        with col2:
            st.markdown(f"[![image_game]({img.fetchone()[0]})]({link_steam})")
        with col3:
            st.write("")

        # st.title(f'{box_1_1}')
        # Description
        st.text(descr.fetchone()[0])

    elif box_1_2 == 'Reviews':
        # Name
        curs = conn.cursor()
        query = f'SELECT total_positive, total_negative FROM Games WHERE Games.name = ?'
        params = [box_1_1]
        curs.execute(query, params)

        st.markdown(f"<h1 style='text-align: center;'>{box_1_1}</h1>", unsafe_allow_html=True)
        fig = px.pie(values=curs.fetchone(), names=['Positive reviews', 'Negative reviews'])
        fig.update_layout(title_text=f'Reviews for {box_1_1}', title_x=0.5)
        fig.update_traces(textposition='inside', textinfo='value+percent')
        st.plotly_chart(fig, use_container_width=True)

elif box_1 == 'Two games':
    # if random button clicked
    if st.sidebar.button('Random'):
        box_1_1 = st.sidebar.selectbox('Select game #1', [random.choice(list_games)])
        new_list = list(list_games)
        new_list.remove(box_1_1)
        box_1_2 = st.sidebar.selectbox('Select game #2', [random.choice(new_list)])
        # if user wants to reset
        if st.sidebar.button('Reset'):
            box_1_1 = st.sidebar.selectbox('Select game #1', list_games)
            new_list = list(list_games)
            new_list.remove(box_1_1)
            box_1_2 = st.sidebar.selectbox('Select game #2', new_list)

    # if user select two games
    else:
        box_1_1 = st.sidebar.selectbox('Select game #1', list_games)
        new_list = list(list_games)
        new_list.remove(box_1_1)
        box_1_2 = st.sidebar.selectbox('Select game #2', new_list)

    box_1_3 = st.sidebar.selectbox('Select features to compare',
                                   (['Select', 'Price', 'Reviews']))

    list_name_games = [box_1_1, box_1_2]
    if box_1_3 == 'Select':
        st.markdown(f"<h1 style='text-align: center;'>{box_1_1}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>vs</h1>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'>{box_1_2}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)

        # Gif here?
        #col1, col2 = st.columns(2)
        #col1.markdown("![Foo](https://i.gifer.com/origin/57/570998fe4bf6c8c6827a3cb1c3d23003_w200.gif)")
        #col2.markdown("![Foo](https://i.gifer.com/4dg6.gif)")

    elif box_1_3 == 'Price':
        # Price PROBLEM! Keeps changing?!
        price_query = conn.cursor()
        query = f'SELECT price FROM Games WHERE Games.name = ? or Games.name = ?'
        params = list_name_games
        price_query.execute(query, params)

        st.markdown(f"<h1 style='text-align: center;'>Price: {box_1_1} vs {box_1_2}</h1>", unsafe_allow_html = True)
        fig = px.bar(x=list_name_games, y=[price_query.fetchone()[0], price_query.fetchone()[0]])
        #fig.update_layout(title_text=f'Price of {box_1_1} vs {box_1_2}', title_x=0.5)
        fig.update_xaxes(title_text='Games')
        fig.update_yaxes(title_text='Price')
        st.plotly_chart(fig, use_container_width=True)

    if box_1_3 == 'Reviews':
        # Reviews not working properly yet
        review_query = conn.cursor()
        query = f'SELECT total_positive, total_negative FROM Games WHERE Games.name = ? or Games.name = ?'
        params = list_name_games
        review_query.execute(query, params)

        st.markdown(f"<h1 style='text-align: center;'>Reviews: {box_1_1} vs {box_1_2}</h1>", unsafe_allow_html=True)
        fig = px.bar(x=list_name_games, y=[review_query.fetchone()[0], review_query.fetchone()[0]])
        #fig.update_layout(title_text=f'Number of positive reviews of {box_1_1} vs {box_1_2}', title_x=0.5)
        fig.update_xaxes(title_text='Games')
        fig.update_yaxes(title_text='Reviews')
        st.plotly_chart(fig, use_container_width=True)

elif box_1 == 'All games':
    box_1_1 = st.sidebar.selectbox('Select features',
                                   (['Select', 'Developers', 'Price', 'Reviews']))
    if box_1_1 == 'Developers':
        developer_query = conn.cursor()
        developer_query.execute('''SELECT developers, COUNT(developers) FROM Games GROUP BY developers
        HAVING COUNT(developers)>5 ORDER BY COUNT(developers);''')


        list_developer=[]
        list_developer_count=[]
        for developer in developer_query.fetchall():
            list_developer.append(developer[0])
            list_developer_count.append(developer[1])


        fig = px.bar(y=list_developer, x=list_developer_count, orientation='h', labels={'x': 'Game count', 'y': 'Developers'},
                     color_discrete_sequence=['midnightblue'], height=800)
        fig.update_layout(title_text='Top developers by number of games on Steam', title_x=0.6)
        st.plotly_chart(fig, use_container_width=True)

conn.close()
