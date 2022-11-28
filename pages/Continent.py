import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from Country import processdata

benua_Asia = "Asia covers an area of 44,579,000 square kilometres (17,212,000 sq mi), about 30% of Earth's total land area and 8.7% of Earth's total surface area. The continent, which has long been home to the majority of the human population, was the site of many of the first civilizations. Its 4.7 billion people constitute roughly 60% of the world's population. "
benua_Europa = "Europe covers an area 10.18 square kilometres (3.93 million sq mi), or 2% of Earth's surface (6.8% of land area), making it the second-smallest continent (using the seven-continent model). Politically, Europe is divided into about fifty sovereign states, of which Russia is the largest and most populous, spanning 39% of the continent and comprising 15% of its population. Europe had a total population of about 745 million (about 10% of the world population) in 2021"
benua_NorthAmerica = "North America covers an area of about 24,709,000 square kilometres (9,540,000 square miles), about 16.5% of Earth's land area and about 4.8% of its total surface. North America is the third-largest continent by area, following Asia and Africa, and the fourth by population after Asia, Africa, and Europe. In 2013, its population was estimated at nearly 579 million people in 23 independent states, or about 7.5% of the world's population."
benua_SouthAmerica = "South America has an area of 17,840,000 square kilometers (6,890,000 sq mi). Its population as of 2021 has been estimated at more than 434 million."
benua_Africa = "Africa is the world's second-largest and second-most populous continent, after Asia in both cases. At about 30.3 million km2 (11.7 million square miles) including adjacent islands, it covers 6% of Earth's total surface area and 20% of its land area. With 1.4 billion people as of 2021, it accounts for about 18% of the world's human population."
benua_Oceania = "Oceania is estimated to have a land area of 8,525,989 square kilometres (3,291,903 sq mi) and a population of around 44.5 million as of 2021. When compared with the continents, the region of Oceania is the smallest in land area and the second least populated after Antarctica."

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

select_continent = st.selectbox("Select the Continent", pd.unique(df["Continent"]))
continent_data = df[df['Continent'] == select_continent]
if select_continent == 'Asia':
    lan = 14.6709
    long = 75.0453
    st.write(benua_Asia)
elif select_continent == 'Africa':
    lan = 6.2958712
    long = 25.1235002
    st.write(benua_Africa)
elif select_continent == 'Oceania':
    lan = -23.24954
    long = 127.4240
    st.write(benua_Oceania)
elif select_continent == 'Europe':
    lan = 64.61600
    long = 61.24236
    st.write(benua_Europa)
elif select_continent == 'North America':
    lan = 50.557619
    long = -97.5759
    st.write(benua_NorthAmerica)
elif select_continent == 'South America':
    lan = -19.6598
    long = -69.45098
    st.write(benua_SouthAmerica)
else:
    lan = 7.823425
    long = 12.46307

maps = folium.Map(location=[lan,long],
                zoom_start=3, tiles='Stamen Terrain')
country_data_locations = continent_data.drop_duplicates(subset=['Country'],keep='last')
country_data_locations = country_data_locations[["Country", "latitude", "longitude"]]
for index, location_info in country_data_locations.iterrows():
    folium.Marker([location_info["latitude"], location_info["longitude"]],
                 popup=pd.unique(location_info["Country"])).add_to(maps)
# st.write(country_data_locations)
# maps = folium.Map(location=[-0.789275, 113.921327], zoom_start=3, tiles='OpenStreetMap',width='100%')
# if st.checkbox('Show Map', False, key=1):
    

tab1, tab2 = st.tabs(["List of countries on the continent " + select_continent,"Map on continents "+ select_continent])
tab1.subheader("List of countries on the continent " + select_continent )
tab1.write(country_data_locations)


tab2.subheader("Map on continents "+ select_continent)
with tab2:
    folium_static(maps, width=1200, height=600)

    