# import streamlit as st
# import requests
# import base64
# import time
# from datetime import datetime

# summary = requests.get("https://htv-project.onrender.com/api/summary").json()["summary"]
# summary_paragraphs = [p for p in summary.split("\n") if p.strip()]

# highlight = requests.get("https://htv-project.onrender.com/api/highlight").json()["highlight"]
# highlight_paragraphs = [p for p in highlight.split("\n") if p.strip()]

# # Mock user data (would come from an API)
# user_name = "Alexander"

# # def autoplay_audio(file_path: str):
# #     with open(file_path, "rb") as f:
# #         data = f.read()
# #         b64 = base64.b64encode(data).decode()
# #         md = f"""
# #             <audio controls autoplay="true">
# #             <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
# #             </audio>
# #             """
# #         st.markdown(
# #             md,
# #             unsafe_allow_html=True,
# #         )

# # def helpbtnCallback():
# #     autoplay_audio("voice.mp3")

# def autoplay_audio(file_path: str):
#     with open(file_path, "rb") as f:
#         data = f.read()
#         b64 = base64.b64encode(data).decode()
#         md = f"""
#             <audio id="helpAudio" controls autoplay="true" onended="document.getElementById('helpAudio').remove();">
#             <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
#             </audio>
#             """
#         st.markdown(md, unsafe_allow_html=True)

# def helpbtnCallback():
#     st.session_state["show_audio"] = True

#     # Get the latest data from the /api/latest endpoint
#     url_latest = "https://htv-project.onrender.com/api/latest"
#     response_latest = requests.get(url_latest)

#     if response_latest.status_code == 200:
#         latest_data = response_latest.json()
        
#         # Assuming the first entry is the one we want
#         descp = latest_data[0]["descp"]
#         timestamp = latest_data[0]["timestamp"]

#         # Parse the timestamp and calculate the minutes ago
#         timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
#         now = datetime.now()
#         time_diff = now - timestamp_obj
#         minutes_ago = int(time_diff.total_seconds() / 60)

#         # Format the string "X minutes ago..."
#         time_str = f"{minutes_ago} minutes ago..."

#         # Combine the time string and description
#         combined_text = f"{time_str} {descp}"

#         # Pass the combined text to the /api/text-to-speech API
#         url_tts = "https://htv-project.onrender.com/api/text-to-speech"
#         data_tts = {
#             "text": combined_text
#         }
#         response_tts = requests.post(url_tts, json=data_tts)

#         if response_tts.status_code == 200:
#             # The response contains the audio file, store it in a variable
#             audio_file = response_tts.content

#             # Save the audio file to a local file (optional)
#             with open("output_audio.mp3", "wb") as f:
#                 f.write(audio_file)

#             print("Audio file has been saved to 'output_audio.mp3'")

#             # Optionally, autoplay the saved audio file
#             autoplay_audio("output_audio.mp3")
#         else:
#             print(f"Failed to retrieve audio. Status code: {response_tts.status_code}, Message: {response_tts.text}")

#     else:
#         print(f"Failed to get latest data. Status code: {response_latest.status_code}, Message: {response_latest.text}")

#     st.session_state["show_audio"] = False

# # Initialize session state for the audio player if it doesn't exist
# if "show_audio" not in st.session_state:
#     st.session_state["show_audio"] = False




# # Dashboard Page
# def dashboard():
#     st.title(f"Welcome, {user_name}!")

#     # st.button("HELP - Environmental Context Assistance", type="primary", on_click=helpbtnCallback)
#         # Add the button to play the help audio

#     # # Display the help button (unconditionally)
#     # if st.button("HELP - Environmental Context Assistance"):
#     #     helpbtnCallback()  # Play the audio when clicked

#         # Display the help button (unconditionally)
#     if st.button("HELP - Environmental Context Assistance"):
#         helpbtnCallback()  # Play the audio when clicked

#     # Conditionally show the audio player below the title
#     if st.session_state["show_audio"]:
#         autoplay_audio("voice.mp3")  # This will autoplay the audio

#     st.subheader("Your day so far:")
#     st.write("""Here's a brief summary of what you've done today:""")

#     for summary in summary_paragraphs:
#         st.write(f"- {summary}")
    
#     st.write("""Check out your today's highlight:""")
#     for highlight in highlight_paragraphs:
#         st.write(f"- {highlight}")

# dashboard()

import streamlit as st
import requests
import base64
import time
from datetime import datetime

summary = requests.get("https://htv-project.onrender.com/api/summary").json()["summary"]
summary_paragraphs = [p for p in summary.split("\n") if p.strip()]

highlight = requests.get("https://htv-project.onrender.com/api/highlight").json()["highlight"]
highlight_paragraphs = [p for p in highlight.split("\n") if p.strip()]

# Mock user data (would come from an API)
user_name = "Baron"

def autoplay_audio(file_path: str):
    """Plays audio on the UI from the file path provided."""
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio id="helpAudio" controls autoplay="true" onended="document.getElementById('helpAudio').remove();">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(md, unsafe_allow_html=True)

def helpbtnCallback():
    """Callback to handle fetching latest description and generating text-to-speech audio."""
    st.session_state["show_audio"] = False  # Initially disable showing audio until processed

    # Get the latest data from the /api/latest endpoint
    url_latest = "https://htv-project.onrender.com/api/latest"
    response_latest = requests.get(url_latest)

    if response_latest.status_code == 200:
        latest_data = response_latest.json()
        
        # Assuming the first entry is the one we want
        descp = latest_data[0]["descp"]
        timestamp = latest_data[0]["timestamp"]

        # Parse the timestamp and calculate the minutes ago
        timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        time_diff = now - timestamp_obj
        minutes_ago = int(time_diff.total_seconds() / 60)

        # Format the string "X minutes ago..."
        time_str = f"{minutes_ago} minutes ago..."

        # Combine the time string and description
        combined_text = f"{time_str} {descp}"

        # Pass the combined text to the /api/text-to-speech API
        url_tts = "https://hack-the-valley-09.charlws.workers.dev/api/text-to-speech"
        data_tts = {
            "text": combined_text
        }
        response_tts = requests.post(url_tts, json=data_tts)

        if response_tts.status_code == 200:
            # The response contains the audio file, store it in a variable
            audio_file = response_tts.content

            # Save the audio file to a local file (output_audio.mp3)
            audio_file_path = "output_audio.mp3"
            with open(audio_file_path, "wb") as f:
                f.write(audio_file)

            # Set session state to show the audio player after receiving the file
            st.session_state["audio_file_path"] = audio_file_path
            st.session_state["show_audio"] = True  # Enable showing the audio
        else:
            print(f"Failed to retrieve audio. Status code: {response_tts.status_code}, Message: {response_tts.text}")

    else:
        print(f"Failed to get latest data. Status code: {response_latest.status_code}, Message: {response_latest.text}")

# Initialize session state for the audio player if it doesn't exist
if "show_audio" not in st.session_state:
    st.session_state["show_audio"] = False

if "audio_file_path" not in st.session_state:
    st.session_state["audio_file_path"] = None

# Dashboard Page
def dashboard():
    st.title(f"Welcome, {user_name}!")

    # Display the help button (unconditionally)
    if st.button("HELP - Environmental Context Assistance"):
        helpbtnCallback()  # Play the audio when clicked

    # Conditionally show the audio player below the title if the audio is ready
    if st.session_state["show_audio"] and st.session_state["audio_file_path"]:
        autoplay_audio(st.session_state["audio_file_path"])  # Play the generated audio file

    st.subheader("Your day so far:")
    st.write("""Here's a brief summary of what you've done today:""")
    for summary in summary_paragraphs:
        st.write(f"- {summary}")
    
    st.write("""Check out your today's highlight:""")
    for highlight in highlight_paragraphs:
        st.write(f"- {highlight}")

# Render the dashboard
dashboard()
