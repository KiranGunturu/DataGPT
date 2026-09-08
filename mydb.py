import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

def get_engine(database="retail", server="localhost\\MSSQLSERVER03"):
    odbc = quote_plus(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;TrustServerCertificate=yes;"
    )
    return create_engine(f"mssql+pyodbc:///?odbc_connect={odbc}")


# build the engine once and reuse it — don't reconnect on every call
_engine = get_engine()


def run_query(query, params=None):
    """Run a SQL query and return the result as a DataFrame."""
    with _engine.connect() as conn:
        df = pd.read_sql(text(query), conn, params=params)
    return df

def get_schema(table_name):
    query = f'''
    select 
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE
    from INFORMATION_SCHEMA.COLUMNS
    where TABLE_SCHEMA = 'dbo'
    and TABLE_NAME = '{table_name}'
    order by ORDINAL_POSITION;
    '''
    schema = run_query(query)
    return schema

# result = get_schema('orders')
# print(result)