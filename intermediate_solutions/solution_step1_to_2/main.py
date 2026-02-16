# %%
import pandas as pd
from sklearn.compose import make_column_selector as selector
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
import time
# %%
data = pd.read_parquet('s3://confpns/synthetic-transactions/rawdata/transactions/transactions_flats_final.parquet')
data_h = pd.read_parquet("s3://confpns/synthetic-transactions/rawdata/transactions/transactions_houses_final.parquet")

# %%
if data.columns.all() == data_h.columns.all():
    data_all = pd.concat([data, data_h])

# Setting data type of dteloc to a more meaningful category 
data_all["dteloc"] = pd.Categorical(
    data_all["dteloc"],
    categories=["1", "2"],
    ordered=False  # Set to True if the categories have a meaningful order
).rename_categories({"1": "House", "2": "Flat"})

data_all["price_sqm"] = data_all["valeurfonc"] / data_all["dsupdc"]
# Selecting the only cols we want to use

# %%
# Sample some data
data_small = data_all.sample(150000)
data_features = data_small[["depcom", "dteloc", "dnbppr", "dnbcha", "dsupdc"]]
data_target = data_small["valeurfonc"]
# depcom (question encoding ?), dteloc (boolean apt), dnbppr, dnbcha, dsupdc

# %%
# Encoding issue - differentiate between numeric and other
cols_cat = selector(dtype_exclude="number")
cols_num = selector(dtype_include="number")

# %%
data_features.hist(bins=10)
# Features are not troncated
# %%
data_features.hist(log=True)
# %%
data_target.hist(bins=10)  # skewed to 0 bcs prices
# %%
data_target.plot(kind='hist', logx=True, logy=True)  # sharp decrease for assets above 1Me

# %%
preprocessor = make_column_transformer(
    (OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), cols_cat),
    remainder="passthrough",
)
model_gb = make_pipeline(preprocessor, GradientBoostingRegressor())
model_rf = make_pipeline(preprocessor, RandomForestRegressor())
# %%
target = "price_sqm"
sample_size = 400000

# 
data_small = data_all.sample(sample_size)
data_features = data_small[["depcom", "dteloc", "dnbppr", "dnbcha", "dsupdc"]]
data_target = data_small["valeurfonc"]

#
start = time.time()
cv_results = cross_validate(model_gb, data_features, data_small[target])
elapsed_time = time.time() - start
scores = cv_results["test_score"]

#
print(
    f"Data set : \n"
    f"   - {data_features.shape[1]} col ({list(data_features.columns)})\n"
    f"   - n_ops : {data_features.shape[0]} \n"
    f"target is : {target} \n"
    f"Mean cross validation accuracy is : "
    f"{scores.mean():.3f} +- {scores.std():.3f}"
    f" with an elapsed time of {elapsed_time:.3f}s"
)
# %%
