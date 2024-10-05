import streamlit as st
import pandas as pd
import requests

r = requests.get('https://htv-project.onrender.com/api/getrecords').json()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

map_data = [{"inbound": 1, "outbound": 1, "lon": float(r[i]["locationx"]), "lat": float(r[i]["locationy"]), "lon2": float(r[i + 1]["locationx"]), "lat2": float(r[i]["locationy"])} for i in range(len(r) - 1)]

location_data = pd.DataFrame(map_data)
st.subheader("Today's GPS Trace")
st.map(location_data)
