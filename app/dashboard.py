import streamlit as st
import requests

summary = requests.get("https://htv-project.onrender.com/api/summary").json()["summary"]
summary_paragraphs = [p for p in summary.split("\n") if p.strip()]

highlight = requests.get("https://htv-project.onrender.com/api/highlight").json()["highlight"]
highlight_paragraphs = [p for p in highlight.split("\n") if p.strip()]

# Mock user data (would come from an API)
user_name = "Alexander"

# Dashboard Page
def dashboard():
    st.title(f"Welcome, {user_name}!")

    st.subheader("Your day so far:")
    st.write("""Here's a brief summary of what you've done today:""")

    for summary in summary_paragraphs:
        st.write(f"- {summary}")
    
    st.write("""Check out your today's highlight:""")
    for highlight in highlight_paragraphs:
        st.write(f"- {highlight}")

dashboard()
