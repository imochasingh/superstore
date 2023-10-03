import streamlit as st
import snowflake.connector
import matplotlib.pyplot as plt
import pandas as pd
# import tomli
from collections import Counter
import plotly.express as px
import sql
from PIL import Image

st.set_page_config(
    page_title="Superstore Dashboard",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


#------------- THIS IS WORKING FINE FOR NAV BAR BUT FOR NOW COMMNETING OUT AS NEED TO FIX SOMETHING 
# import hydralit_components as hc
# # specify the primary menu definition
# menu_data = [
#         {'icon': "far fa-copy", 'label':"Left End"},
#         {'id':'Copy','icon':"🐙",'label':"Copy"},
#         {'icon': "far fa-chart-bar", 'label':"Chart"},#no tooltip message
#         {'icon': "far fa-address-book", 'label':"Book"},
#         {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
#         {'icon': "far fa-clone", 'label':"Component"},
#         {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
#         {'icon': "far fa-copy", 'label':"Right End"},
# ]
# # we can override any part of the primary colors of the menu
# #over_theme = {'txc_inactive': '#FFFFFF','menu_background':'red','txc_active':'yellow','option_active':'blue'}
# over_theme = {'txc_inactive': '#FFFFFF'}
# menu_id = hc.nav_bar(menu_definition=menu_data,home_name='Home',override_theme=over_theme)
#get the id of the menu item clicked
# st.info(f"{menu_id=}")





# from streamlit_extras.app_logo import add_logo

# def logo():
#     add_logo("img/bgimg.png", height=300)

# logo()

 

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''

    imageurl ="https://img.freepik.com/free-vector/gradient-purple-striped-background_23-2149583760.jpg"
    # https://img.freepik.com/free-vector/background-concept-with-technology-particles_23-2148294347.jpg?w=1060&t=st=1695289318~exp=1695289918~hmac=1d777cd2b9d662f15befb87eaa1dd8ef4bedec91a9be28464e6878eb17a0e749
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url({imageurl});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
 
    
set_bg_hack_url()

def space(num_lines: int = 1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

# Function to read Snowflake connection details from TOML file
# def read_snowflake_config():
#     try:
#         with open('snowflake_config.toml', 'rb') as config_file:
#             config = tomli.load(config_file)
#         return config['snowflake']
#     except FileNotFoundError:
#         st.error("Snowflake configuration file not found. Please create a 'snowflake_config.toml' file with your credentials.")

# Function to create a Snowflake connection and cursor
def create_connection():
    conn = snowflake.connector.connect(
        user='poc',
        password="Poc@3214",
        account= 'byzfefs-pd02178',
        warehouse='COMPUTE_WH',
        database='STREAM_SUPERSTORE_PKG',
        schema='SHARED_DATA'
    )
    cur = conn.cursor()
    return conn, cur


 
conn, cur = create_connection()

company, other = st.columns(2)
with company:
    st.header(":atom_symbol: Raj's superstore")
with other:
    st.write("")

#  --------- filters 

def filterCountry():
    cur.execute(sql.countryFilter)
    # countnryFilterData = cur.fetchall()
    countnryFilterData = [row[0] for row in cur.fetchall()]
    return countnryFilterData






# Use st.sidebar to add filters in the sidebar
st.sidebar.header("Filters")
from datetime import date
default_start_date = date(2010, 1, 1)

selected_countries = st.sidebar.multiselect("Select Country", ["All"] + filterCountry())
start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date")

# Format the selected dates to match your SQL date format
formatted_start_date = start_date.strftime("%Y-%m-%d")
formatted_end_date = end_date.strftime("%Y-%m-%d")


def fetchScore(selected_countries):
    if not selected_countries or (len(selected_countries) == 1 and 'All' in selected_countries):
        scoreSql=sql.scoreSql
    else:        
        # Dynamically build the IN clause
        selected_country_str = ', '.join([f"'{country}'" for country in selected_countries])
        scoreSql = sql.scoreSql + f"WHERE country IN ({selected_country_str})"
    cur.execute(scoreSql)
    r_score = cur.fetchone()
    return r_score


if not selected_countries or (len(selected_countries)==1 and 'All' in selected_countries):    
    conditionSql = f"where orderdate::date between '{start_date}' and '{end_date}'"
else:
    selected_country_str = ', '.join([f"'{country}'" for country in selected_countries])
    conditionSql = f" where country in ({selected_country_str}) and orderdate::date between '{start_date}' and '{end_date}'"

cateforySales = f"""
SELECT CATEGORY , SUM(SALES) AS TOTAL_SALES FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE 
{conditionSql}
GROUP BY CATEGORY  order by TOTAL_SALES ASC
    """


 
# Function to fetch data from Snowflake using the provided SQL query
def fetchCategorySales():    
    # fetchCategorySalesSql= sql.cateforySales + conditionSql    
    cur.execute(cateforySales)
    data = cur.fetchall()
    # conn.close()
    return data

abc = fetchCategorySales()
import pygwalker as pyg 
# st.write(type(abc))

adf = pd.DataFrame(abc)
 
 
vis_spec = """<PASTE_COPIED_CODE_HERE>"""
pyg_html = pyg.walk(adf, spec=vis_spec, return_html=True)
# components.html(pyg_html, height=1000, scrolling=True)



def fetchSubCategorySales():
    # con,cur= create_connection()
    cur.execute(sql.subCategorySales)
    fetchSubCategorySalesData = cur.fetchall()
    # conn.close()
    return fetchSubCategorySalesData


r1c0,r1c1, r1c2, r1c3,r1c5 = st.columns(5)



with r1c0:
    font_color = "violet" 
    st.write(
        f'<div style="text-align: center; color: ">'
        f'<div style="font-weight: bold; font-size: 24px; color:{font_color} ;">{fetchScore(selected_countries)[0]}</div>'
        '<div>Total Customer</div>'
        '</div>',
        unsafe_allow_html=True
    )
with r1c1:
    font_color = "violet" 
    st.write(
        f'<div style="text-align: center;">'
        f'<div style="font-weight: bold; font-size: 24px; color: {font_color};">{fetchScore(selected_countries)[1]}</div>'
        '<div>Total Orders</div>'
        '</div>',
        unsafe_allow_html=True
    )

with r1c2:       
      font_color = "violet" 
      dollar_emoji = "+"
      st.write(
            f'<div style="text-align: center;">'
            f'<div style="font-weight: bold; font-size: 24px; color: {font_color};">  {dollar_emoji} {fetchScore(selected_countries)[2]}</div>'
            '<div>Total Quantity</div>'
            '</div>',
            unsafe_allow_html=True
        )


with r1c3:
   font_color = "violet" 
   dollar_emoji = "💰"
   st.write(
    f'<div style="text-align: center;">'
    f'<div style="font-weight: bold; font-size: 24px; color: {font_color};">  {dollar_emoji} {fetchScore(selected_countries)[3]}</div>'
    '<div>Total Sales</div>'
    '</div>',
    unsafe_allow_html=True
)


# with r1c4:

#    font_color = "violet" 
#    dollar_emoji = "💰"
#    st.write(
#     f'<div style="text-align: center;">'
#     f'<div style="font-weight: bold; font-size: 24px; color: {font_color};">  {dollar_emoji} {fetchScore()[4]}</div>'
#     '<div>Total Profit</div>'
#     '</div>',
#     unsafe_allow_html=True
# )


with r1c5:

   font_color = "violet" 
   dollar_emoji = "💰"
   st.write(
    f'<div style="text-align: center;">'
    f'<div style="font-weight: bold; font-size: 24px; color: {font_color};">  {dollar_emoji} {fetchScore(selected_countries)[6]}</div>'
    '<div>Total Profit</div>'
    '</div>',
    unsafe_allow_html=True
)



st.write("---")


 
# Execute the query and convert it into a Pandas data frame


# Function to display the results in tabular format
# def displayTable(data):
#     if not data:
#         st.write("No data available.")
#     else:
#         # space(4)
#         # Create a DataFrame from the fetched data
#         df = pd.DataFrame(data, columns=["CATEGORY", "TOTAL_SALES"])
#         df["TOTAL_SALES"] = "$ " + df["TOTAL_SALES"].astype(str)
#         st.table(df)


def displayPieChart(data):
    # Check if there is no data
    if not data:
        st.write("No data available.")
    else:
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(data, columns=["CATEGORY", "TOTAL_SALES"])
        fig = px.pie(df, labels="CATEGORY", values="TOTAL_SALES", names="CATEGORY", height=300,width=500, color_discrete_sequence=px.colors.sequential.Plasma)
        # Display the pie chart using Streamlit
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background color
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper (plot border) color
            title="Sales by Category",
            xaxis_title="CATEGORY",
            yaxis_title="SALES",
            xaxis=dict(tickangle=45),
            showlegend=True  # Hide the legend    
              , margin=dict(l=0, r=0, t=80, b=50)
           , legend=dict(
                orientation='h',  # Set the legend orientation to horizontal
                yanchor='bottom',  # Anchor the legend to the bottom
                y=5.02,  # Adjust the y position to move it below the pie chart
                xanchor='center',  # Center the legend horizontally
                x=0.5  # Center the legend horizontally
                , bgcolor='#B9770E' #'#d5aae4'
            )        
        )
        st.plotly_chart(fig)

# Function to display the bar chart with multiple colored bars and values on the bars using Plotly
def displayBarChart(fetchSubCategorySalesData):
    if not fetchSubCategorySalesData:
        st.write("No data available.")
    else:
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(fetchSubCategorySalesData, columns=["SUB_CATEGORY", "TOTAL_SALES"])

        # Generate a list of unique skills
        unique_skills = df["SUB_CATEGORY"].unique()

        fig = px.bar(df, x="SUB_CATEGORY", y="TOTAL_SALES",
                    hover_data=['TOTAL_SALES', 'SUB_CATEGORY'], color='TOTAL_SALES',
                    labels={'pop':'Sales'}, height=300)

        # Customize the layout
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background color
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper (plot border) color
            title="Sub Category Sales",
            xaxis_title="SUB-CATEGORY",
            yaxis_title="SALES",
            xaxis=dict(tickangle=45),
            showlegend=False  # Hide the legend            
        )
        # Display the bar chart using Plotly
        st.plotly_chart(fig)
 




def segment():
    # con,cur= create_connection()
    cur.execute(sql.segmentSql)
    segmentData = cur.fetchall()
    # conn.close()
    return segmentData
def segmentPieChart(data):
    # Check if there is no data
    if not data:
        st.write("No data available.")
    else:
        # Create a DataFrame from the fetched data
        df = pd.DataFrame(data, columns=["SEGMENT", "SALES"])        
        # Calculate the total sales
        total_sales = df["SALES"].sum()        
        # Calculate the percentage of sales for each segment
        df["SALES_PERCENTAGE"] = (df["SALES"] / total_sales) * 100        
        fig = px.pie(df, labels="SEGMENT", values="SALES_PERCENTAGE", names="SEGMENT",height=300, width=500, color_discrete_sequence=px.colors.sequential.Plasma)        
        # Display the pie chart using Streamlit
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background color
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper (plot border) color
            title="Customer Segment Sales",
            xaxis_title="SEGMENT",
            yaxis_title="SALES_PERCENTAGE (%)",
            xaxis=dict(tickangle=45),
            showlegend=True  # Hide the legend
            , margin=dict(l=50, r=70, t=80, b=50)
           , legend=dict(
                orientation='h',  # Set the legend orientation to horizontal
                yanchor='bottom',  # Anchor the legend to the bottom
                y=5.02,  # Adjust the y position to move it below the pie chart
                xanchor='center',  # Center the legend horizontally
                x=0.5  # Center the legend horizontally
                , bgcolor='#B9770E'
           )
        )
        
        st.plotly_chart(fig)

# -======================




# ============================

# chart_data1 = pd.DataFrame(segment(),columns="SEGMENT")
# st.bar_chart(chart_data1)

# ------------- top 10 product 

def topProduct():
    cur.execute(sql.top10Product)
    topProducts = cur.fetchall()
    return topProducts

def top10ProductsBarH(data):
    if not data:
        st.write("No data available")
    else:
        df = pd.DataFrame(data, columns = ["PRODUCTNAME","TOTAL_SOLD"])
        fig = px.bar(df, y="PRODUCTNAME", x="TOTAL_SOLD", color="TOTAL_SOLD", orientation="h", hover_name="PRODUCTNAME", height=300, width=500)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background color
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper (plot border) color
            title="Top 10 Product",
            xaxis_title="Total Sold",
            yaxis_title="Product Name",
            xaxis=dict(tickangle=45),
            showlegend=True  # Hide the legend
            # , margin=dict(l=50, r=70, t=80, b=50)
            , yaxis={'categoryorder':'total ascending'}
            , legend=dict(
                orientation='h',  # Set the legend orientation to horizontal
                yanchor='bottom',  # Anchor the legend to the bottom
                y=5.02,  # Adjust the y position to move it below the pie chart
                xanchor='center',  # Center the legend horizontally
                x=0.5  # Center the legend horizontally
                , bgcolor='#B9770E'
           )
        )
    st.plotly_chart(fig)

# ------------- END OF TOP 10 PRODUCTS


#----------- sales by orderrdate trend 




def orderSales():
    cur.execute(sql.salesOrderTrend)
    orderSalesData = cur.fetchall()
    if not orderSalesData:
        st.write("No data available")
    else:
        # df = pd.DataFrame(orderSalesData, columns=["ORDERDATE", "TOTAL_SALES"])
        # fig = px.line(df, x="ORDERDATE", y="TOTAL_SALES", title="Sales Trend Over Time",hover_data=["TOTAL_SALES", "ORDERDATE"] )
        # fig.update_xaxes(title_text="Order Date")
        # fig.update_yaxes(title_text="Sales")
        dates, sales = zip(*orderSalesData)
        
        df = pd.DataFrame({"Date": dates, "Sales": sales})
        
        # Sort the DataFrame by date if it's not already sorted
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values(by="Date")
        
        fig = px.line(
            df,
            x="Date",
            y="Sales",
            # color = "Sales",
            markers=True,
            color_discrete_sequence=["#f0f922"],
            # title="Sales Trend Over Time",
            hover_data=["Date", "Sales"]  # Specify columns for tooltips
            ,height=300
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background color
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper (plot border) color
            title="Sales Trend Over Time",
            xaxis_title="TOTAL SALES",
            yaxis_title="Total Orders",
            xaxis=dict(tickangle=45),
            height=400
        )
    st.plotly_chart(fig)




# --------------- TOP 10 PROFITABLE PRODUCT 

# def marketsales():
#     cur.execute(sql.marketsales)
#     marketSalesResult = cur.fetchall()
#     return marketSalesResult

def market():
    cur.execute(sql.marketsales)
    marketSalesResult = cur.fetchall()
    if not marketSalesResult:
        st.write("No data available")
    else:
        df = pd.DataFrame(marketSalesResult, columns = ["MARKET","TOTAL_SALES"])
        fig = px.bar(df, 
                     y="MARKET", 
                     x="TOTAL_SALES",
                       color="TOTAL_SALES", 
                    #  orientation="h", 
                     hover_name="MARKET", 
                     height=300,
                       width=500)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background color
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper (plot border) color
            title="Top 10 Profitable Product",
            xaxis_title="TOTAL SALES",
            yaxis_title="MARKET",
            xaxis=dict(tickangle=45),
            showlegend=True  # Hide the legend
            # , margin=dict(l=50, r=70, t=80, b=50)
            , yaxis={'categoryorder':'total ascending'}
            , legend=dict(
                # orientation='v',  # Set the legend orientation to horizontal
                yanchor='bottom',  # Anchor the legend to the bottom
                y=5.02,  # Adjust the y position to move it below the pie chart
                xanchor='center',  # Center the legend horizontally
                x=0.5  # Center the legend horizontally
                , bgcolor='#B9770E'
           )
        )
    st.plotly_chart(fig)

# ------------- END OF TOP 10 PRODUCTS


#-------------- region by country total sales 
def regioncountry():
    cur.execute(sql.regioncountrysql)
    regCountry = cur.fetchall()
    if not regCountry:
        st.write("No data available")
    else:
        df = pd.DataFrame(regCountry, columns = ["REGION","TOTAL_SALES"])
        fig = px.bar(df, 
                     y="REGION", 
                     x="TOTAL_SALES",
                       color="TOTAL_SALES", 
                    #  orientation="h", 
                     hover_name="REGION", 
                     height=300,
                       width=500)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background color
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper (plot border) color
            title="Top 10 Profitable Product",
            xaxis_title="TOTAL SALES",
            yaxis_title="MARKET",
            xaxis=dict(tickangle=45),
            showlegend=True  # Hide the legend
            # , margin=dict(l=50, r=70, t=80, b=50)
            , yaxis={'categoryorder':'total ascending'}
            , legend=dict(
                # orientation='v',  # Set the legend orientation to horizontal
                yanchor='bottom',  # Anchor the legend to the bottom
                y=5.02,  # Adjust the y position to move it below the pie chart
                xanchor='center',  # Center the legend horizontally
                x=0.5  # Center the legend horizontally
                , bgcolor='#B9770E'
           )
        )
    st.plotly_chart(fig)



def countryyearsales():
    cur.execute(sql.countrYearSales)
    cys = cur.fetchall()
    if not cys:
        st.write(" No data available")
    else:
        df = pd.DataFrame(cys, columns=["COUNTRY","REGION","ORDERYEAR","TOTALSALES", "TOTALORDER"])
        fig = px.scatter(df, x="TOTALSALES", y="TOTALORDER", animation_frame="ORDERYEAR", animation_group="COUNTRY",
            color="TOTALORDER", hover_name="COUNTRY",color_discrete_sequence=px.colors.sequential.Plasma,
           log_x=True, size_max=55, range_x=[20,5000], range_y=[0,90000]
           )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',  # Transparent background color
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper (plot border) color
            title="Region Country Year Order Sales",
            xaxis_title="TOTAL SALES",
            yaxis_title="Total Orders",
            xaxis=dict(tickangle=45),
            height=400,
            showlegend=True  # Hide the legend
            # , margin=dict(l=50, r=70, t=80, b=50)
            # , yaxis={'categoryorder':'total ascending'}
            , legend=dict(
                # orientation='v',  # Set the legend orientation to horizontal
                yanchor='bottom',  # Anchor the legend to the bottom
                y=-0.02,  # Adjust the y position to move it below the pie chart
                xanchor='center',  # Center the legend horizontally
                x=1.5 ,  # Center the legend horizontally
                bgcolor='#B9770E'
           )
        )
        st.plotly_chart(fig)
       





# Main Streamlit app

def main():
    # Define a variable to hold data
    data = fetchCategorySales()    
    # Create columns for the layout
    col1, col2, col3 = st.columns([1.8, 1.8, 3]) 
    # Place content within the columns
    with col1:
        displayPieChart(data)    
    with col2:
        segmentPieChart(segment())    
    with col3:
        displayBarChart(fetchSubCategorySales())
   
    # Add a horizontal line
    st.write("---")
    
    # Place content within the second row column
    top10product, mkt , rgc= st.columns(3)

    with top10product:
        top10ProductsBarH(topProduct())
    with mkt:
        market()

    cys, orders = st.columns(2)

    with cys:
        countryyearsales()
    with orders:
       orderSales()
    
 

if __name__ == "__main__":
    main()
