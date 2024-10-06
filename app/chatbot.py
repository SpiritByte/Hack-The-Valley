import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

# Set your OpenAI API key
api_key = os.getenv("openai_key")
api_url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Memory data from API (your structured data)
memories = requests.get('https://htv-project.onrender.com/api/getrecords').json()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to interact with GPT
def chat_with_gpt(user_input):
    # Add memory context to the prompt
    memory_context = "\n".join([f"Timestamp: {m['timestamp']}, Caption: {m['caption']}" for m in memories])
    
    # Prepare the conversation with the memory context
    system_message = {
        "role": "system",
        "content": f"You have access to the following memories: {memory_context}. If the user ask you about a memory, or if you discover something relevant to the memory (e.g. in terms of timestamp, caption), return a response based on the memory. If not, you can respond based on the user input."
    }
    
    messages = [system_message] + st.session_state.chat_history + [{"role": "user", "content": user_input}]
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        return response_data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# UI setup
st.title("Snaipshot Chatbot")

# Display the chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(f"{chat['content']}")

# Input from the user
prompt = st.chat_input("Ask about a memory or anything else:")

if prompt:    
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    gpt_response = chat_with_gpt(prompt)
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    with st.chat_message("assistant"):
        st.markdown(gpt_response)

