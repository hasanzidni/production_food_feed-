import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from streamlit_app import processdata
import matplotlib.pyplot as plt

im = Image.open("./assets/process.png")
st.set_page_config(
    page_title= "dashboard",
    page_icon=im,
    layout="wide"
)
df = processdata()

def pie_graf(data):
    # Graph (Pie Chart in Sidebar)
    df_target = data[['Continent', 'Element']].groupby('Element').count() #/ len(df)
    # st.table(df_target)
    fig_target = go.Figure(data=[go.Pie(labels=df_target.index,
                                    values=df_target['Continent'],
                                    hole=.3)])
    st.plotly_chart(fig_target, use_container_width=True)

def data_element_continent(data, elememt,value):
    data_element = data[data["Element"] == elememt]
    data_element = data_element.groupby('Country')['Total_production'].sum()
    data_element = data_element.sort_values(ascending=True)[-value:]
    return data_element

st.markdown("#### World's Food and Feed production")    
col1, col2, col3 = st.columns(3)
tab1, tab2, tab3  = st.tabs(["Pie Chart", "Top Food", "Top Feed"])
tab1.subheader(" Pie (food and feed) details of the World")
# Graph (Pie Chart in Sidebar)
df_target = df[['Continent', 'Element']].groupby('Element').count() #/ len(df)
fig_target = go.Figure(data=[go.Pie(labels=df_target.index,
                                    values=df_target['Continent'],
                                    hole=.3)])
tab1.plotly_chart(fig_target, use_container_width=True)

tab2.subheader("Top Food Producers")
food_world = data_element_continent(df, 'Food', 30)
tab2.bar_chart(food_world)

tab3.subheader("Top Feed Producers")
feed_world = data_element_continent(df, 'Feed',30)
tab3.bar_chart(feed_world)

data_asia = df[df["Continent"] == 'Asia']
data_africa = df[df["Continent"] == 'Africa'] 
data_europa = df[df["Continent"] == 'Europe']
data_Oceania = df[df["Continent"] == 'Oceania'] 
data_NortA = df[df["Continent"] == 'North America'] 
data_SouthA = df[df["Continent"] == 'South America'] 

food_asia = data_element_continent(data_asia, 'Food', 20)
food_africa = data_element_continent(data_africa, 'Food',20) 
food_europa = data_element_continent(data_europa, 'Food',20)
food_Oceania = data_element_continent(data_Oceania,'Food',20)
food_NortA = data_element_continent(data_NortA, 'Food',20) 
food_SouthA = data_element_continent(data_SouthA, 'Food',20)

feed_asia = data_element_continent(data_asia, 'Feed',20)
feed_africa = data_element_continent(data_africa, 'Feed',20) 
feed_europa = data_element_continent(data_europa, 'Feed',20)
feed_Oceania = data_element_continent(data_Oceania,'Feed',20)
feed_NortA = data_element_continent(data_NortA, 'Feed',20) 
feed_SouthA = data_element_continent(data_SouthA, 'Feed',20)

tab1, tab2, tab3  = st.tabs(["Pie Chart", "Top Food", "Top Feed"])

tab1.subheader(" Pie (food and feed) details of each continent")
col1, col2, col3 = tab1.columns(3)
with col1:
    st.markdown("#### Asia") 
    pie_graf(data_asia)

    st.markdown("#### Africa")
    pie_graf(data_africa)

with col2:
    st.markdown("#### Europe") 
    pie_graf(data_europa)

    st.markdown("#### Oceania")
    pie_graf(data_Oceania)
        
with col3:
    st.markdown("#### North America")
    pie_graf(data_NortA)

    st.markdown("#### South America")
    pie_graf(data_SouthA)

tab2.subheader("Top Food Producers")
col1, col2, col3 = tab2.columns(3)
with col1:
    st.markdown("#### Asia")
    st.bar_chart(food_asia)

    st.markdown("#### Africa")
    st.bar_chart(food_africa)

with col2:
    st.markdown("#### Europe") 
    st.bar_chart(food_europa)

    st.markdown("#### Oceania")
    st.bar_chart(food_Oceania)
        
with col3:
    st.markdown("#### North America")
    st.bar_chart(food_NortA)

    st.markdown("#### South America")
    st.bar_chart(food_SouthA)

tab3.subheader("Top Feed Producers")
col1, col2, col3 = tab3.columns(3)
with col1:
    st.markdown("#### Asia")
    st.bar_chart(feed_asia)

    st.markdown("#### Africa")
    st.bar_chart(feed_africa)

with col2:
    st.markdown("#### Europe") 
    st.bar_chart(feed_europa)

    st.markdown("#### Oceania")
    st.bar_chart(feed_Oceania)
        
with col3:
    st.markdown("#### North America")
    st.bar_chart(feed_NortA)

    st.markdown("#### South America")
    st.bar_chart(feed_SouthA)           

col1, col2 = st.columns(2)
with col1:
    select_element = st.selectbox("Select the Element:", pd.unique(df["Element"]))
    element_data = df[df['Element'] == select_element]

with col2:
    select_product = st.selectbox("Select the Product", pd.unique(element_data["Item"]))
    product_data = element_data[element_data['Item'] == select_product]

element_data1 = product_data.loc[:, 'Continent':'Total_production']
tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])

graf_product = px.bar(
    element_data1, 
    x='Country',
    y='Total_production',
    width= 1200, height= 700)

if select_product == None :
    select_product = ""
tab1.subheader(select_product + " Production chart Y1961 ~ Y2013")
tab1.plotly_chart(graf_product)

tab2.subheader(select_product + " Production table Y1961 ~ Y2013")
tab2.write(element_data1)

# m = folium.Map(location=[-22.908333, -43.196389], zoom_start=11, tiles='OpenStreetMap')
# folium_static(m)