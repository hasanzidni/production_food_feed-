# python -m streamlit run Country.py
import streamlit as st
import pandas as pd
import pycountry_convert as pc
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
# import geopandas


im = Image.open("./assets/process.png")
st.set_page_config(
    page_title="Dashboard",
    page_icon=im,
    layout="wide",
)

def predata1():
    fao = pd.read_csv('./FAO.csv',encoding = "ISO-8859-1")
    fao = fao.fillna(method = 'bfill', axis = 1)
    fao.drop(['Area Abbreviation','Area Code','Element Code','latitude','longitude'], inplace=True, axis=1)
    fao.rename(columns={"Area":"Country"}, inplace=True)
    fao.rename(columns={"Item Code":"Code"}, inplace=True)
    renamedata(fao)
    indexAge = fao[ (fao['Country'] == 'Timor-Leste')].index
    fao.drop(indexAge , inplace=True)
    fao['Total_production'] = fao.loc[:, 'Y1961':'Y2013'].sum(axis=1)
    fao['Abbreviation'] = [pc.country_name_to_country_alpha2(x, cn_name_format="default") 
                for x in fao['Country']]
    fao['Continent'] = [pc.country_alpha2_to_continent_code(x) 
                for x in fao['Abbreviation']]
    fao['Continent'] = fao['Continent'].map(pc.convert_continent_code_to_continent_name)
    return fao

def predata2():
    latlong = pd.read_csv('./Lat_long.csv',encoding = "ISO-8859-1")
    latlong.rename(columns={"country":"Abbreviation"}, inplace=True)
    return latlong

# def predata3():
#     df = geopandas.read_file('./countries.geojson')
#     # df = pd.DataFrame(geodata.drop(columns=["geometry"]))
#     # geodata.rename(columns={"ADMIN":"Country"}, inplace=True)
#     # geodata['Abbreviation'] = [pc.country_name_to_country_alpha2(x, cn_name_format="default") 
#     #             for x in geodata['Country']]
#     df['lon'] = df.geometry.x  # extract longitude from geometry
#     df['lat'] = df.geometry.y  # extract latitude from geometry
#     df = df[['lon','lat']]     # only keep longitude and latitude
#     st.write(df.head())        # show on table for testing only
#     st.map(df)                 # show on map

def renamedata(df):
    df['Country'] = df['Country'].replace(['Bolivia (Plurinational State of)'],['Bolivia'])
    df['Country'] = df['Country'].replace(['China, Taiwan Province of'],['Taiwan'])
    df['Country'] = df['Country'].replace(['China, Hong Kong SAR'],['Hong Kong'])
    df['Country'] = df['Country'].replace(['China, Macao SAR'],['Macao'])
    df['Country'] = df['Country'].replace(['China, mainland'],['China'])
    df['Country'] = df['Country'].replace(['Iran (Islamic Republic of)'],['Iran'])
    df['Country'] = df['Country'].replace(['Republic of Korea'],['Korea, Republic of'])
    df['Country'] = df['Country'].replace(['The former Yugoslav Republic of Macedonia'],['Macedonia'])
    df['Country'] = df['Country'].replace(['Venezuela (Bolivarian Republic of)'],['Venezuela'])

def processdata():
    fao = predata1()
    latlong = predata2()
    data = pd.merge(fao, latlong, on="Abbreviation")
    data.drop(['name'], inplace=True, axis=1)
    index_value = [60,59,0,1,2,3,4,61,62,58,
        5,6,7,8,9,10,11,12,13,14,15,
        16,17,18,19,20,21,22,23,24,25,
        26,27,28,29,30,31,32,33,34,35,
        36,37,38,39,40,41,42,43,44,45,
        46,47,48,49,50,51,52,53,54,55,
        56,57]
    data = data[[data.columns[i] for i in index_value]]
    return data

df = processdata()

select_country = st.selectbox("Select the Country", pd.unique(df["Country"]))
country_data = df[df['Country'] == select_country]
# st.text(" Production Food and Feed in %s " % (select_country))
country_data_locations = country_data.drop_duplicates(subset=['Country'],keep='last')
benua = country_data_locations['Continent'].squeeze()
st.write(select_country + " is a country on a continent "+ benua)
maps = folium.Map(location=[pd.unique(country_data_locations['latitude']), pd.unique(country_data_locations['longitude'])],
                zoom_start=5, tiles='Stamen Terrain')
folium.Marker(location=[pd.unique(country_data_locations['latitude']), pd.unique(country_data_locations['longitude'])],
            popup=pd.unique(country_data_locations['Country']),
            icon=folium.Icon(color="green", icon="info-sign")).add_to(maps)
# maps = folium.Map(location=[-0.789275, 113.921327], zoom_start=3, tiles='OpenStreetMap',width='100%')
if st.checkbox('Show Map', False, key=1):
    folium_static(maps, width=1200, height=400)
    # print(pd.unique(country_data['latitude']))

# food = country_data['Element'].value_counts()['Food'] 
# feed = country_data['Element'].value_counts()['Feed'] 
# print (food)

# Graph (Pie Chart in Sidebar)
df_target = country_data[['Country', 'Element']].groupby('Element').count() #/ len(df)
# st.table(df_target)
fig_target = go.Figure(data=[go.Pie(labels=df_target.index,
                                    values=df_target['Country'],
                                    hole=.3)])
st.markdown("## {0}'s Food and Feed production".format(str(select_country)))
st.plotly_chart(fig_target, use_container_width=True)

Element = country_data['Element'].unique()
# select_element = st.multiselect("Select the Element", Element)
container = st.container()
all = st.checkbox("Select all")
 
if all:
    select_element = container.multiselect("Select the Element:",
         ['Food', 'Feed'],['Food', 'Feed'])
else:
    select_element =  container.multiselect("Select the Element:",
        Element,default=['Food', 'Feed'])
mask_element = country_data['Element'].isin(select_element)
element_data = country_data[mask_element]

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
element_data1 = element_data.loc[:, 'Continent':'Total_production']
# st.write(element_data1)

state_total_graph = px.bar(
    element_data1, 
    x='Item',
    y='Total_production',
    text_auto='.2s',
    width= 1200, height= 700)

if select_element == None :
    select_element = ""
tab1.subheader(select_country + "'s total food and feed production")
tab1.plotly_chart(state_total_graph)

tab2.subheader(select_country + "'s total food and feed production")
tab2.write(element_data1)

select_product = st.selectbox("Select the Product", pd.unique(element_data["Item"]))
product_data = element_data[element_data['Item'] == select_product]

tab1, tab2 = st.tabs(["📈 Chart", "🗃 Data"])
product = product_data.melt(id_vars =['Item'], 
                            value_vars =product_data.loc[:, 'Y1961':'Y2013'], 
                            var_name ='Year', value_name ='Production')

graf_product = px.bar(
    product, 
    x='Year',
    y='Production',
    width= 1200, height= 700)

if select_product == None :
    select_product = ""
tab1.subheader(select_product + " Production chart Y1961 ~ Y2013")
tab1.plotly_chart(graf_product)

tab2.subheader(select_product + " Production table Y1961 ~ Y2013")
tab2.write(product)

