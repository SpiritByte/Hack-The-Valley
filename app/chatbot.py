import streamlit as st
import requests
import json

# Set your OpenAI API key
api_key = "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"
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

# Function to match user input with memories
def match_memory(query):
    for memory in memories:
        if query in memory['timestamp'] or query in memory['caption'] or query in memory['descp']:
            return f"On {memory['timestamp']}, this happened: {memory['descp']}"
    return None

# Function to interact with GPT
def chat_with_gpt(user_input):
    # Add memory context to the prompt
    memory_context = "\n".join([f"Timestamp: {m['timestamp']}, Caption: {m['caption']}, Description: {m['descp']}" for m in memories])
    
    # Prepare the conversation with the memory context
    system_message = {
        "role": "system",
        "content": f"You have access to the following memories: {memory_context}"
    }
    
    messages = [system_message] + st.session_state.chat_history + [{"role": "user", "content": user_input}]
    
    data = {
        "model": "gpt-3.5-turbo",
        "messages": messages
    }
    
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        print(response.json())
        return response_data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# UI setup
st.title("Memory-Enhanced Chatbot")

# Input from the user
user_input = st.text_input("Ask about a memory or anything else:")

if user_input:
    # Try to match with memory first
    memory_match = match_memory(user_input)
    
    if memory_match:
        st.session_state.chat_history.append({"role": "assistant", "content": memory_match})
    else:
        # Interact with GPT if no memory matches
        gpt_response = chat_with_gpt(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    
    st.session_state.chat_history.append({"role": "user", "content": user_input})

# Display the chat history
st.subheader("Chat History")
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.write(f"**You:** {chat['content']}")
    else:
        st.write(f"**Bot:** {chat['content']}")

# Reset button
if st.button("Reset Chat"):
    st.session_state.chat_history = []
