allResult = """select ROW_ID,
ORDERID,
ORDERDATE,
SHIPDATE,
SHIPMODE,
CUSTOMERID,
CUSTOMERNAME,
SEGMENT,
POSTALCODE,
CITY,
STATE,
COUNTRY,
REGION,
MARKET,
PRODUCTID,
CATEGORY,
SUB_CATEGORY,
PRODUCTNAME,
SALES,
QUANTITY,
DISCOUNT,
PROFIT,
SHIPPINGCOST,
ORDERPRIORITY from STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE"""


countryFilter = """
  SELECT 
distinct country
FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE 
    """


cateforySales = """
  SELECT 
CATEGORY , SUM(SALES) AS TOTAL_SALES
FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE 
GROUP BY CATEGORY  order by TOTAL_SALES ASC
    """

 

subCategorySales = """
  SELECT 
SUB_CATEGORY AS SUB_CATEGORY , SUM(SALES) AS TOTAL_SALES1
FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE 
GROUP BY SUB_CATEGORY  order by TOTAL_SALES1 ASC
    """


totalOrders = """ SELECT count(ORDERID) TOTAL_ORDERS
 FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE """

totalSales = """ SELECT sum(SALES) TOTAL_SALES
FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE """

scoreSql ="""
SELECT 
count(DISTINCT CUSTOMERID) AS total_customer,
count(ORDERID) AS total_orders,sum(quantity) as total_quantity,
sum(sales) as total_sales,
sum(profit) as total_profit ,
sum(case when sign(profit) = -1 then profit else 0 end ) as nagative_profit,
sum(case when sign(profit) 
!= -1 then profit else 0 end ) as positive_profit
FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE """ 


segmentSql ="""SELECT 
SEGMENT , sum(sales) sales
FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE
GROUP BY 1
"""

top10Product =""" SELECT 
PRODUCTNAME , count(*) total_sold
FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE
GROUP BY 1  order by total_sold desc limit 5"""

salesOrderTrend ="""SELECT 
 orderdate AS od , sum(sales) AS total_sales
FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE where year(orderdate)=2015
GROUP BY 1"""

salesByLocation="""SELECT   country, state, city, sum(sales) total_saels FROM STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE 
GROUP BY 1,2,3
"""

top10ProfitableProduct="""  elect distinct PRODUCTNAME,  to_decimal(profit/quantity,9) as PROFIT_PER_QUANTITY
 FROM superstore_app.code_schema.superstore_view 
 order by 2 desc limit 10 """

marketsales ="""select MARKET, sum(sales) as TOTAL_SALES
 FROM superstore_app.code_schema.superstore_view 
group by 1"""


regioncountrysql=""""SELECT REGION,  SUM(SALES) AS TOTAL_SALES
 FROM SUPERSTORE_APP.CODE_SCHEMA.SUPERSTORE_VIEW 
GROUP BY REGION"""


countrYearSales="""SELECT 
COUNTRY , region, year(ORDERDATE) orderYear, count(ORDERID) AS totalorder,  sum(SALES) as totalsales
FROM 
SUPERSTORE_APP.CODE_SCHEMA.SUPERSTORE_VIEW 
GROUP BY country ,region,  YEAR(ORDERDATE) order by 3"""