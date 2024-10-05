import streamlit as st
import requests

r = requests.get("https://f9c0-138-51-73-220.ngrok-free.app/api/summary").json()

# Mock user data (would come from an API)
user_name = "Alexander"
summary_paragraphs = [p for p in r["summary"].split("\n") if p.strip()]

# Dashboard Page
def dashboard():
    # Welcome the user with a title
    st.title(f"Welcome, {user_name}!")

    # Summary of the user's day so far
    st.subheader("Your day so far:")
    st.write("""
        Here's a brief summary of what you've done today:
    """)

    # Display the paragraph summary from the array
    for summary in summary_paragraphs:
        st.write(f"- {summary}")

# Call the dashboard function to render the page
dashboard()
