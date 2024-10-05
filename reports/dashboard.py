import streamlit as st

# Mock user data (would come from an API)
user_name = "Alexander"
summary_paragraphs = [
    "Today, you had an early meeting with the marketing team where you discussed the new product launch strategy.",
    "You then grabbed lunch with Sarah at your favorite cafe downtown.",
    "In the afternoon, you met with your development team to finalize the app features and had a productive brainstorming session."
]

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
