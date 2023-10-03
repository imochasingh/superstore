import pygwalker as pyg
import pandas as pd
import streamlit.components.v1 as components
import streamlit as st
import conn 
import sql

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Raj's Superstore Analysis by Pygwalker ",
    page_icon="🌀",
    layout="wide"
)
 
# Add Title
st.title("Self Analysis")
st.write("wait for few seconds it will take some time to boot ")

def topProduct():
    conn.cur.execute(sql.allResult)
    topProducts = conn.cur.fetchall()
    return topProducts

df = pd.DataFrame(topProduct(), columns=["ROW_ID", "ORDERID","ORDERDATE","SHIPDATE","SHIPMODE","CUSTOMERID","CUSTOMERNAME","SEGMENT","POSTALCODE",
"CITY","STATE","COUNTRY","REGION","MARKET","PRODUCTID","CATEGORY","SUB_CATEGORY","PRODUCTNAME","SALES","QUANTITY","DISCOUNT","PROFIT","SHIPPINGCOST",
"ORDERPRIORITY"])

# st.dataframe(df)


# Paste the copied Pygwalker chart code here
vis_spec = """<PASTE_COPIED_CODE_HERE>"""
 
# Generate the HTML using Pygwalker
pyg_html = pyg.walk(df, spec=vis_spec, return_html=True)
 
# Embed the HTML into the Streamlit app
components.html(pyg_html, height=1000, scrolling=True)