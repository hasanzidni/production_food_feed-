import streamlit as st
from streamlit_folium import folium_static
import folium


st.set_page_config(layout="wide")

m = folium.Map(location=[-22.908333, -43.196389], zoom_start=11, tiles='OpenStreetMap')
folium_static(m)