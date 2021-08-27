import sqlite3
import streamlit as st
import plotly.express as px

conn = sqlite3.connect('steam_data_v2.db')
curs = conn.cursor()

curs.execute('''
SELECT COUNT(publishers)
FROM Games
GROUP BY publishers
HAVING COUNT(publishers)>10
ORDER BY COUNT(publishers);''')
publishers_count = curs.fetchall()

curs.execute(''' 
SELECT publishers
FROM Games
GROUP BY publishers
HAVING COUNT(publishers)>10
ORDER BY COUNT(publishers);''')
publishers = curs.fetchall()

lst=[]
for publisher in publishers:
     lst.append(publisher[0])

lst_count=[]
for publisher in publishers_count:
     lst_count.append(publisher[0])


# Streamlit
st.title("Top steam publishers")
st.markdown("The chart is very nice")

# Plotly
fig = px.bar(y=lst, x=lst_count, orientation='h', labels={'x':'Game count', 'y':'Publishers'},
             color_discrete_sequence=['indianred'], height=500)
fig.update_layout(title_text='Top publishers by number of games on Steam', title_x=0.6)
st.plotly_chart(fig, use_container_width=True)

conn.close()