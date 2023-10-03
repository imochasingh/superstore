import snowflake.connector

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