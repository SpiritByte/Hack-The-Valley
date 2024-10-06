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

image_data = [{"url": x["file_url"], "short_description": x["caption"], "full_description": x["descp"], "timestamp": x["timestamp"], "location": {"latitude": float(x["locationx"]), "longitude": float(x["locationy"])}} for x in r if x["voice_note"] == "Yes"]

if "selected_image_index" not in st.session_state:
    st.session_state.selected_image_index = None

def show_details(index):
    st.session_state.selected_image_index = index
    st.rerun()

def go_back():
    st.session_state.selected_image_index = None
    st.rerun()

st.markdown(
    """
    <style>
    .custom-button {
        margin-bottom: 1.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.session_state.selected_image_index is None:
    col1, col2 = st.columns([3, 0.3])

    with col1:
        search = st.text_input("Search for alerts", "")

    with col2:
        st.markdown('<div class="custom-button">', unsafe_allow_html=True)
        button = st.button("OK")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    col1, col2, col3 = st.columns([3, 0.4, 0.5])

    with col1:
        search = st.text_input("Search for alerts", "")

    with col2:
        st.markdown('<div class="custom-button">', unsafe_allow_html=True)
        button = st.button("OK")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="custom-button">', unsafe_allow_html=True)
        button = st.button("Return")
        st.markdown('</div>', unsafe_allow_html=True)
        if button:
            go_back()


def filter_images(query, data):
    if query:
        return [
            item for item in data if
            query.lower() in item["short_description"].lower() or
            query.lower() in item["full_description"].lower() or
            query.lower() in item["timestamp"]
        ]
    return data

filtered_images = filter_images(search, image_data)

if st.session_state.selected_image_index is not None:

    image = image_data[st.session_state.selected_image_index]
    
    st.image(image["url"], caption=f"Taken on {image['timestamp']}", use_column_width=True)
    st.subheader("Full Description")
    st.write(image["full_description"])

    location_data = pd.DataFrame(
        [{"latitude": image["location"]["latitude"], "longitude": image["location"]["longitude"]}]
    )
    st.subheader("Location on Map")
    st.map(location_data)
    
    if st.button("Back to gallery"):
        go_back()

# If no image is selected, show the image gallery
else:
    if not filtered_images:
        st.write("No results found.")
    else:
        for i in range(0, len(filtered_images)):
            cols = st.columns([3, 0.7]) 

            with cols[0]:
                st.warning(filtered_images[i]["short_description"], icon="⚠️")

            with cols[1]:
                if st.button(f"Show details", key=f"button_{i}"):
                    show_details(i)


    st.write("---")
