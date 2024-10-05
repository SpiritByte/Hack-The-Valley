import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page("app/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)
history = st.Page("app/history.py", title="History", icon=":material/history:")
trace = st.Page("app/trace.py", title="Trace", icon=":material/map:")
chatbot = st.Page("app/chatbot.py", title="Chatbot", icon=":material/robot:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Snaipshot": [dashboard, history, trace, chatbot, logout_page],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()