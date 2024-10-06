import cv2
import streamlit as st
import numpy as np
import time
import requests
import base64
import random


# ESP32-CAM URL (change this to your ESP32-CAM's IP address)
esp32_camera_url = "http://192.168.202.47/cam-hi.jpg"  # Replace with ESP32-CAM's IP
api_url = "https://htv-project.onrender.com/api/new-memory"

if 'last_upload_time' not in st.session_state:
    st.session_state.last_upload_time = 0
if 'image' not in st.session_state:
    st.session_state.image = None


# Function to capture an image from the ESP32-CAM
def capture_image():
    try:
        response = requests.get(esp32_camera_url)
        if response.status_code == 200:
            img_array = np.frombuffer(response.content, np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)
            return frame
        else:
            st.error("Failed to capture image from ESP32-CAM.")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Function to send the image and random location to the API
def send_image_to_api(image, locationX, locationY):
    if image is not None:
        _, img_encoded = cv2.imencode('.jpg', image)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')  # Convert to Base64

        data = {
            'base64_image': img_base64,  # Sending Base64-encoded image
            'locationX': locationX,
            'locationY': locationY
        }

        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 200:  
                st.success(f"Image uploaded successfully with location: {locationX}, {locationY}!")
            else:
                st.error(f"Failed to upload image: {response.status_code}")
        except Exception as e:
            st.error(f"Error uploading image: {e}")
    else:
        st.warning("No image captured. Try again.")

base_latitude = 43.783458
base_longitude = -79.187899

delta_latitude = 0.01  # Change as needed
delta_longitude = 0.01  # Change as needed

def generate_random_coordinates():
    random_latitude = round(random.uniform(base_latitude - delta_latitude, base_latitude + delta_latitude), 6)
    random_longitude = round(random.uniform(base_longitude - delta_longitude, base_longitude + delta_longitude), 6)
    return random_latitude, random_longitude


# Streamlit app interface
st.title("ESP32-CAM Image Capture and Upload with Random Location")
while True:
    current_time = time.time()
    if current_time - st.session_state.last_upload_time >= 5:  # Capture every 5 seconds
        st.session_state.image = capture_image()
        locationX, locationY = generate_random_coordinates()
        
        # Send the captured image and random coordinates to the API
        send_image_to_api(st.session_state.image, locationX, locationY)
        
        # Update last upload time
        st.session_state.last_upload_time = current_time
        
        time.sleep(5)  # Wait for 5 seconds before the next capture
