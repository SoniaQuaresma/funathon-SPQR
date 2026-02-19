# %%
import pandas as pd
from sklearn.compose import make_column_selector as selector
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from sklearn.dummy import DummyRegressor
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
features_list = [
    ["depcom", "x", "y", "dteloc", "dnbppr", "dnbcha", "dsupdc"],
    ['anneemut', 'dteloc', 'jannath', 'ccodep', 'depcom', 'x', 'y','distance_ltm', 'dnbniv', 'dnbbai', 'dnbdou',
       'dnblav', 'dnbwc', 'dnbppr', 'dnbsam', 'dnbcha', 'dnbcu8', 'dnbcu9',
       'dnbsea', 'dnbann', 'dnbpdc', 'dsupdc', 'dniv', 'nb_terrasses',
       'nb_greniers', 'nb_caves', 'nb_autresdep']
] 
target = "price_sqm"
data_75 = data_all[data_all['ccodep'] == '75'].dropna()
# %%
max_target = data_75[target].quantile(0.9)
min_target = data_75[target].quantile(0.1)
data_preproc = data_75[(data_75[target] <= max_target) & (data_75[target] >= min_target)]

# %%
data_features = data_preproc[features_list[1]]
data_target = data_preproc[target] # depcom (question encoding ?), dteloc (boolean apt), dnbppr, dnbcha, dsupdc

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
model_hist = make_pipeline(preprocessor, HistGradientBoostingRegressor())
model_rf = make_pipeline(preprocessor, RandomForestRegressor())

models_list = [model_gb, model_hist, model_rf]
# %%
#

max_target = data_75[target].quantile(0.8)
min_target = data_75[target].quantile(0.2)
data_preproc = data_75[(data_75[target] <= max_target) & (data_75[target] >= min_target)]

# %%
for feature in features_list:
    data_features = data_preproc[feature]
    data_target = data_preproc[target] # depcom (question encoding ?), dteloc (boolean apt), dnbppr, dnbcha, dsupdc

    start = time.time()
    cv_results = cross_validate(model_gb, data_features, data_target)
    elapsed_time = time.time() - start
    scores = cv_results["test_score"]

    #
    print(
        f"Data set : \n"
        f"   - {data_features.shape[1]} col ({list(data_features.columns)})\n"
        f"   - n_ops : {data_features.shape[0]} \n"
        f"Mean cross validation accuracy is : "
        f"{scores.mean():.3f} +- {scores.std():.3f}"
        f" with an elapsed time of {elapsed_time:.3f}s"
    )
# %%
max_target = data_75[target].quantile(0.9)
min_target = data_75[target].quantile(0.1)
data_preproc = data_75[(data_75[target] <= max_target) & (data_75[target] >= min_target)]

for feature in features_list:
    data_features = data_preproc[feature]
    data_target = data_preproc[target] # depcom (question encoding ?), dteloc (boolean apt), dnbppr, dnbcha, dsupdc
    X_train, X_test, y_train, y_test = train_test_split(data_features, data_target)

    print(
        f"Data set : \n"
        f"   - {data_features.shape[1]} col ({list(data_features.columns)})\n"
        f"   - n_ops : {data_features.shape[0]} \n"
    )

    for model in models_list:
        start = time.time()
        model.fit(X_train, y_train)
        elapsed_time = time.time() - start
        y_pred = model.predict(X_test)
        mape = mean_absolute_percentage_error(y_test, y_pred)
        rtwo = r2_score(y_test, y_pred)

        print(
            f"= Model is : {model.steps[-1][1].__class__.__name__} \n"
            f"  Metrics are : \n"
            f"   - MAPE : {mape:.3f} \n"
            f"   - R2 : {rtwo:.3f} \n"
            f"  with an elapsed time of {elapsed_time:.3f}s"
        )

# %%

dummy_regr = DummyRegressor(strategy="mean")
dummy_regr.fit(data_features, data_target)
dummy_regr.score(data_features, data_target)
# %%
