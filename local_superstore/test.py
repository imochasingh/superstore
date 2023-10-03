import numpy as np 
import pandas as pd
import streamlit as st

data = []

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

 

products = ['Product A', 'Product B', 'Product C', 'Product D']
sales = [5000, 7500, 3000, 6000]
product_sales_list = list(zip(products, sales))

r = product_sales_list.to_pandas()

st.bar_chart(r.set_index("SEGMENT")["sales"])

