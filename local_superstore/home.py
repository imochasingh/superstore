import streamlit as st

st.set_page_config(page_title="Usage Insights app", page_icon="🌀", layout="centered")


# gui.icon("🌀")

# Make sure session state is preserved
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

st.title("Welcome to the Usage Insights app!")
st.sidebar.info("Choose a page!")
st.markdown(
    """
This is a simple app to show the features of streamlit.
It is using snowflake as the datasource 

### Get started!

👈 Select a page in the sidebar!
    """
)
