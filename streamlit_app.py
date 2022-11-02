# python -m streamlit run streamlit_app.py
from operator import index
from turtle import title
from mysqlx import Row
import streamlit as st
import pandas as pd
import pycountry_convert as pc
from PIL import Image
import plotly.express as px
import tkinter

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

Element = country_data['Element'].unique()
# select_element = st.multiselect("Select the Element", Element)
container = st.container()
all = st.checkbox("Select all")
 
if all:
    select_element = container.multiselect("Select the Element:",
         ['Food', 'Feed'],['Food', 'Feed'])
else:
    select_element =  container.multiselect("Select the Element:",
        Element)
mask_element = country_data['Element'].isin(select_element)
element_data = country_data[mask_element]
element_data = element_data.loc[:, 'Continent':'Total_production']

st.write(element_data)
if not st.checkbox('Hide Graph', False, key=1):
    state_total_graph = px.bar(
    element_data, 
    x='Item',
    y='Total_production')
    st.plotly_chart(state_total_graph)

# select_product = st.sidebar.selectbox("Select the Product", pd.unique(element_data["Item"]))
# product_data = element_data[element_data['Item'] == select_product]

