import streamlit as st

dashboard = st.Page("app/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)
history = st.Page("app/history.py", title="History", icon=":material/history:")
alerts = st.Page("app/alerts.py", title="Alerts", icon=":material/warning:")
trace = st.Page("app/trace.py", title="Trace", icon=":material/map:")
chatbot = st.Page("app/chatbot.py", title="Chatbot", icon=":material/robot:")

pg = st.navigation(
    {
        "Snaipshot": [dashboard, history, alerts, trace, chatbot],
    }
)

pg.run()