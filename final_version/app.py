import sqlite3
import streamlit as st
import plotly.express as px
import random
from PIL import Image
import numpy as np

conn = sqlite3.connect('database/steam_data_final.db')
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
box_1 = st.sidebar.selectbox('What do you want to analyze?', ('Select', 'Single game', 'Two games', 'Top games', 'Time'))

if box_1 == 'Select':
    st.image(image)

# SINGLE GAME
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

# TWO GAMES
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
        # Price
        # Query price of game 1
        price_query_1 = conn.cursor()
        query = f'SELECT price FROM Games WHERE Games.name = ?'
        params = [box_1_1]
        price_query_1.execute(query, params)

        # Query price of game 2
        price_query_2 = conn.cursor()
        query = f'SELECT price FROM Games WHERE Games.name = ?'
        params = [box_1_2]
        price_query_2.execute(query, params)

        # Plot
        st.markdown(f"<h1 style='text-align: center;'>Price: {box_1_1} vs {box_1_2}</h1>", unsafe_allow_html = True)
        fig = px.bar(x=list_name_games, y=[price_query_1.fetchone()[0], price_query_2.fetchone()[0]])
        #fig.update_layout(title_text=f'Price of {box_1_1} vs {box_1_2}', title_x=0.5)
        fig.update_xaxes(title_text='Games')
        fig.update_yaxes(title_text='Price')
        st.plotly_chart(fig, use_container_width=True)

    list_name_games = [box_1_1, box_1_2]

    if box_1_3 == 'Reviews':
        # Reviews
        review_query_1 = conn.cursor()
        query = f'SELECT total_positive, total_negative FROM Games WHERE Games.name = ?'
        params = [box_1_1]
        review_query_1.execute(query, params)

        review_query_2 = conn.cursor()
        query = f'SELECT total_positive, total_negative FROM Games WHERE Games.name = ?'
        params = [box_1_2]
        review_query_2.execute(query, params)

        tuple_game_1 = review_query_1.fetchone()
        tuple_game_2 = review_query_2.fetchone()
        positive_reviews = [tuple_game_1[0], tuple_game_2[0]]
        negative_reviews = [tuple_game_1[1], tuple_game_2[1]]

        st.markdown(f"<h1 style='text-align: center;'>Reviews: {box_1_1} vs {box_1_2}</h1>", unsafe_allow_html=True)
        fig = px.bar(x=list_name_games, y=[positive_reviews, negative_reviews])
        # fig.update_layout(title_text=f'Number of positive reviews of {box_1_1} vs {box_1_2}', title_x=0.5)
        fig.update_xaxes(title_text='Games')
        fig.update_yaxes(title_text='Reviews')
        newnames = {'wide_variable_0': 'Positive reviews', 'wide_variable_1': 'Negative reviews'}
        fig.for_each_trace(lambda t: t.update(name=newnames[t.name],
                                              legendgroup=newnames[t.name],
                                              hovertemplate=t.hovertemplate.replace(t.name, newnames[t.name])))
        fig.update_layout({
            'legend_title_text': ''})
        st.plotly_chart(fig, use_container_width=True)

# Top 10 GAMES
elif box_1 == 'Top games':
    box_1_1 = st.sidebar.selectbox('Select features',
                                   (['Developers', 'Price', 'Review score', 'Positive reviews', 'Negative reviews']))
    box_color = st.sidebar.selectbox('Select color',
                                   (['Lightskyblue','Midnightblue', 'Red', 'Aquamarine', 'Magenta']))
    color = box_color.lower()
    if box_1_1 == 'Developers':
        developer_query = conn.cursor()
        developer_query.execute('''SELECT developers, COUNT(developers) FROM Games GROUP BY developers
                                ORDER BY COUNT(developers) DESC LIMIT 10;''')

        list_developer=[]
        list_developer_count=[]

        for developer in developer_query.fetchall():
            list_developer.append(developer[0])
            list_developer_count.append(developer[1])

        st.markdown(f"<h1 style='text-align: center;'>Top 10: {box_1_1}</h1>", unsafe_allow_html=True)
        fig = px.bar(y=list_developer, x=list_developer_count, orientation='h',
                     labels={'x': 'Game count', 'y': 'Developers'}, color_discrete_sequence=[color], height=600)
        st.plotly_chart(fig, use_container_width=True)

    elif box_1_1 == 'Price':
        price_query = conn.cursor()
        price_query.execute('''SELECT name, price FROM Games ORDER BY price DESC LIMIT 10;''')

        list_nominal = []
        list_numerical = []

        for entries in price_query.fetchall():
            list_nominal.append(entries[0])
            list_numerical.append(entries[1])

        st.markdown(f"<h1 style='text-align: center;'>Top 10: {box_1_1}</h1>", unsafe_allow_html=True)
        fig = px.bar(x=list_nominal, y=list_numerical,
                     labels={'x': 'Games', 'y': 'Price'}, color_discrete_sequence=[color], height=600)
        st.plotly_chart(fig, use_container_width=True)

    elif box_1_1 == 'Review score':
        query = conn.cursor()
        query.execute('''SELECT name, review_score FROM Games ORDER BY review_score DESC LIMIT 10;''')

        list_nominal = []
        list_numerical = []

        for entries in query.fetchall():
            list_nominal.append(entries[0])
            list_numerical.append(entries[1])

        st.markdown(f"<h1 style='text-align: center;'>Top 10: {box_1_1}</h1>", unsafe_allow_html=True)
        fig = px.bar(y= list_nominal, x= list_numerical, orientation='h',
                    labels={'x': box_1_1, 'y': 'Games'}, color_discrete_sequence=[color], height=600)

        st.plotly_chart(fig, use_container_width=True)

    elif box_1_1 == 'Positive reviews':
        query = conn.cursor()
        query.execute('''SELECT name, total_positive FROM Games ORDER BY total_positive DESC LIMIT 10;''')

        list_nominal = []
        list_numerical = []

        for entries in query.fetchall():
            list_nominal.append(entries[0])
            list_numerical.append(entries[1])

        st.markdown(f"<h1 style='text-align: center;'>Top 10: {box_1_1}</h1>", unsafe_allow_html=True)
        fig = px.bar(y= list_nominal, x= list_numerical, orientation='h',
                    labels={'x': box_1_1, 'y': 'Games'}, color_discrete_sequence=[color], height=600)

        st.plotly_chart(fig, use_container_width=True)

    elif box_1_1 == 'Negative reviews':
        query = conn.cursor()
        query.execute('''SELECT name, total_negative FROM Games ORDER BY total_negative DESC LIMIT 10;''')

        list_nominal = []
        list_numerical = []

        for entries in query.fetchall():
            list_nominal.append(entries[0])
            list_numerical.append(entries[1])

        st.markdown(f"<h1 style='text-align: center;'>Top 10: {box_1_1}</h1>", unsafe_allow_html=True)
        fig = px.bar(y= list_nominal, x= list_numerical, orientation='h',
                    labels={'x': box_1_1, 'y': 'Games'}, color_discrete_sequence=[color], height=600)

        st.plotly_chart(fig, use_container_width=True)

elif box_1 == 'Time':
    box_1_1 = st.sidebar.selectbox('Select time',
                                   (['Monthly', 'Daily']))
    box_color = st.sidebar.selectbox('Select color',
                                   (['Lightskyblue','Midnightblue', 'Red', 'Aquamarine', 'Magenta']))
    color = box_color.lower()
    if box_1_1 == 'Monthly':
        # extract month for each row
        command = '''
                SELECT COUNT(*), strftime('%m', date) as publish_month
                FROM GAMES
                GROUP BY publish_month
                '''
        curs.execute(command)
        release_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        game_count = []
        for publish_tuple in curs.fetchall():
            game_count.append(publish_tuple[0])

        st.markdown(f"<h1 style='text-align: center;'>Released games per month</h1>", unsafe_allow_html=True)
        fig = px.bar(x=release_month, y=game_count, labels={'x': 'Month', 'y': 'Game count'},
                     color_discrete_sequence=[color], height=400)
        average = np.mean(game_count)
        fig.add_hline(y=average, line_dash="dot",
                      annotation_text="Average",
                      annotation_position="top left",
                      line_color="red")
        st.plotly_chart(fig, use_container_width=True)

conn.close()
