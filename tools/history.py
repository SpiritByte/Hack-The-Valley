import streamlit as st
import pandas as pd

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

image_data = [
    {
        "url": "Alex_Code.jpg",
        "short_description": "This is a description for the first image.",
        "full_description": "This is a description for the first image. This is a description for the first image. This is a description for the first image.",
        "timestamp": "2024-10-01 14:30:00",
        "location": {"latitude": 37.7749, "longitude": -122.4194} 
    },
    {
        "url": "Baron_Yuhh.jpg",
        "short_description": "This is a description for the second image.",
        "full_description": "This is a description for the second image. This is a description for the second image. This is a description for the second image.",
        "timestamp": "2024-10-02 09:15:00",
        "location": {"latitude": 34.0522, "longitude": -118.2437} 
    },
    {
        "url": "Anirudh_Mad.jpg",
        "short_description": "This is a description for the third image.",
        "full_description": "This is a description for the third image. This is a description for the third image. This is a description for the third image. This is a description for the third image.",
        "timestamp": "2024-10-03 18:45:00",
        "location": {"latitude": 40.7128, "longitude": -74.0060} 
    },
    {
        "url": "Anirudh_Bye.jpg",
        "short_description": "This is a description for the fourth image.",
        "full_description": "This is a description for the fourth image. This is a description for the fourth image.",
        "timestamp": "2024-10-04 13:10:00",
        "location": {"latitude": 51.5074, "longitude": -0.1278} 
    }
]

if "selected_image_index" not in st.session_state:
    st.session_state.selected_image_index = None

def show_details(index):
    st.session_state.selected_image_index = index

def go_back():
    st.session_state.selected_image_index = None

selected = st.text_input("Search For Memories", "")
button_clicked = st.button("OK")

def filter_images(query, data):
    if query:
        return [
            item for item in data if
            query.lower() in item["short_description"].lower() or
            query.lower() in item["full_description"].lower() or
            query.lower() in item["timestamp"]
        ]
    return data

filtered_images = filter_images(selected, image_data)

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
        for i in range(0, len(filtered_images), 2):
            cols = st.columns(2) 

            with cols[0]:
                st.image(filtered_images[i]["url"], caption=f"Taken on {filtered_images[i]['timestamp']}", use_column_width=True)
                st.subheader("Description")
                st.write(filtered_images[i]["short_description"])
                if st.button(f"More details about {filtered_images[i]['url']}", key=f"button_{i}"):
                    show_details(i)

            if i + 1 < len(filtered_images):
                with cols[1]:
                    st.image(filtered_images[i+1]["url"], caption=f"Taken on {filtered_images[i+1]['timestamp']}", use_column_width=True)
                    st.subheader("Description")
                    st.write(filtered_images[i+1]["short_description"])
                    if st.button(f"More details about {filtered_images[i+1]['url']}", key=f"button_{i+1}"):
                        show_details(i+1)

    st.write("---")
