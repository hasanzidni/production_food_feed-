import streamlit as st
from streamlit_folium import folium_static
import folium
from PIL import Image
from streamlit_app import processdata

im = Image.open("./assets/process.png")
st.set_page_config(
    page_title= "Dashboard",
    page_icon=im,
    layout="wide"
)
df = processdata()

# select_country = st.selectbox("Select the Continent", pd.unique(df["Continent"]))
# country_data = df[df['Continent'] == select_country]

m = folium.Map(location=[-22.908333, -43.196389], zoom_start=11, tiles='OpenStreetMap')
folium_static(m)