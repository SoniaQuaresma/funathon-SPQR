## Exercice 1: Understanding data inputs
# %%
import duckdb
import os

RANDOM_STATE = 202605

# Create a non-persistent connection (the database exists only while the connection is alive and disappears when it is closed)
con = duckdb.connect(database=":memory:")
# %%
trans = con.sql(
    """
        SELECT * FROM read_parquet('https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/1_input/transactions_EN.parquet')
    """).to_df()
# %%
trans.shape # (nb_rows, nb_columns)
trans.dtypes # type of each columns
trans.columns # list of columns
trans.index # index
trans.info() # full summary: types + non-null values + memory
trans.describe() # statistics (count, mean, std, min, max, quartiles)
trans.head(n=5) # first n rows
trans.isnull().sum() # nb of NaN per column
trans.notnull().all() # column with no NaN?