import streamlit as st
from streamlit_lottie import st_lottie
import json


st.set_page_config(page_title="Raj's Superstore", page_icon="🌀", layout="centered")


# gui.icon("🌀")

# Make sure session state is preserved
for key in st.session_state:
    st.session_state[key] = st.session_state[key]

st.title("Welcome to the Raj's Superstore analysis app!")
st.sidebar.info("Choose a page!")
st.markdown(
    """
This is a simple app to show the features of streamlit.
It is using snowflake as the datasource 

### Get started!

👈 Select a page in the sidebar!
    """
)


def load_lottiefile(filepath: str):
    with open("lottiefile.json", "r") as f:
        data = json.load(f)
        st_lottie(data, height=400, width=400)


with st.container():
    st.write("---")
    r1_c1, r2_c2 = st.columns(2)
    with r1_c1:
        st.header(" What I do ")
        st.write("##")
        st.write("""
                On my youtube chennel I am creating tutorials for:
                 - Snowflake
                 - Domo
                 - dbt
                 """
                )

    with r2_c2:
        load_lottiefile("lottiefile.json")  # replace link to local lottie file

