-- STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE definition

create or replace TABLE STREAM_SUPERSTORE_PKG.SHARED_DATA.SUPERSTORE (
	ROW_ID NUMBER(38,0),
	ORDERID VARCHAR(16777216),
	ORDERDATE DATE,
	SHIPDATE DATE,
	SHIPMODE VARCHAR(16777216),
	CUSTOMERID VARCHAR(16777216),
	CUSTOMERNAME VARCHAR(16777216),
	SEGMENT VARCHAR(16777216),
	POSTALCODE FLOAT,
	CITY VARCHAR(16777216),
	STATE VARCHAR(16777216),
	COUNTRY VARCHAR(16777216),
	REGION VARCHAR(16777216),
	MARKET VARCHAR(16777216),
	PRODUCTID VARCHAR(16777216),
	CATEGORY VARCHAR(16777216),
	SUB_CATEGORY VARCHAR(16777216),
	PRODUCTNAME VARCHAR(16777216),
	SALES FLOAT,
	QUANTITY NUMBER(38,0),
	DISCOUNT FLOAT,
	PROFIT FLOAT,
	SHIPPINGCOST FLOAT,
	ORDERPRIORITY VARCHAR(16777216)
);