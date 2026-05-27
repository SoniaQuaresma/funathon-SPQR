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

# %% 

import pandas as pd

trans = trans[trans["prop_loc_dep"].isin(["75", "77", "78", "91", "92", "93", "94", "95"])]
trans.head()

# %%
trans["price_sqm"] = trans["price"] / trans["farea"]
trans.head()


# %%
import numpy as np
import matplotlib.pyplot as plt

y = trans["price_sqm"]
p = np.percentile(y, 99.5)

fig, axes = plt.subplots(4, 1, figsize=(12, 12))

for ax, (data, label) in zip(axes, [(y, "Y"), (y[y <= p], "Y filtered"), (np.log(y), "log(Y)"), (np.log(y[y <= p]), "log(Y) filtered")]):
    ax.hist(data, bins="auto", edgecolor="white", color="#334887", alpha=0.5)
    ax.set_title(label)
    ax.set_xlabel("Price per square meter")
    ax.set_ylabel("Number of transactions")

plt.tight_layout()
plt.show()


# %%
fig, axes = plt.subplots(1, 2, figsize=(10, 5))

for ax, (data, label) in zip(axes, [(y[y <= 2000], "Y below 2000€ per sqm"), (y[y <= 500], "Y below 500€ per sqm")]):
    ax.hist(data, bins="auto", edgecolor="white", color="#334887", alpha=0.95)
    ax.set_title(label)
    ax.set_xlabel("Price per square meter")
    ax.set_ylabel("Number of transactions")

plt.tight_layout()
plt.show()
# %%
