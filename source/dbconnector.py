import sqlite3
import polars as pl
import pandas as pd

def get_data_polars(dbname: str, query: str) -> pl.dataframe:
    '''
    Method returns polars dataframe (sql query to sqlite)
    :param dbname: sqlite db
    :param query: sql query
    :return: pl.dataframe
    '''
    conn = sqlite3.connect(dbname)
    return pl.read_database(query=query, connection=conn)

def get_data_pandas(dbname: str, query: str) -> pl.dataframe:
    '''
    Method returns polars dataframe (sql query to sqlite)
    :param dbname: sqlite db
    :param query: sql query
    :return: pl.dataframe
    '''
    conn = sqlite3.connect(dbname)
    return pd.read_sql(sql=query, con=conn)