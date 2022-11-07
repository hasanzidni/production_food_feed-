import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from streamlit_app import processdata

im = Image.open("./assets/process.png")
st.set_page_config(
    page_title= "Dashboard",
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

st.markdown("#### World's Food and Feed production")
pie_graf(df)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("#### Europe's Food and Feed production")
    data_asia = df[df["Continent"] == 'Asia'] 
    pie_graf(data_asia)

    st.markdown("#### Africa's Food and Feed production")
    data_africa = df[df["Continent"] == 'Africa'] 
    pie_graf(data_africa)

with col2:
    st.markdown("#### Europe's Food and Feed production")
    data_europa = df[df["Continent"] == 'Europe'] 
    pie_graf(data_europa)

    st.markdown("#### Africa's Food and Feed production")
    data_Oceania = df[df["Continent"] == 'Oceania'] 
    pie_graf(data_Oceania)
    
with col3:
    st.markdown("#### North America's Food and Feed production")
    data_NortA = df[df["Continent"] == 'North America'] 
    pie_graf(data_NortA)

    st.markdown("#### South America's Food and Feed production")
    data_SouthA = df[df["Continent"] == 'South America'] 
    pie_graf(data_SouthA)


col1, col2 = st.columns(2)
with col1:
    select_element = st.selectbox("Select the Element:", pd.unique(df["Element"]))
    element_data = df[df['Element'] == select_element]

with col2:
    select_product = st.selectbox("Select the Product", pd.unique(element_data["Item"]))
    product_data = element_data[element_data['Item'] == select_product]



st.write(product_data)

m = folium.Map(location=[-22.908333, -43.196389], zoom_start=11, tiles='OpenStreetMap')
folium_static(m)