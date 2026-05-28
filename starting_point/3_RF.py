# %%

# Defining train and test sets
X_train = pd.read_parquet("https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/2_preprocessing/X_train.parquet")
X_test  = pd.read_parquet("https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/2_preprocessing/X_test.parquet")

X_train = X_train.drop(columns=["prop_type", "trans_date"])
X_test  =  X_test.drop(columns=["prop_type", "trans_date"])

y_train = pd.read_parquet('https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/2_preprocessing/y_train.parquet')["price_sqm"]
y_test  = pd.read_parquet('https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/2_preprocessing/y_test.parquet')["price_sqm"]
# %%

from sklearn.ensemble import RandomForestRegressor

# create RandomForestRegressor instance with selected hyperparameters
rf = RandomForestRegressor(
    n_estimators=50,
    max_features="sqrt",
    min_samples_leaf=10,
    oob_score=True # for calculating total oob error for the RF
)

# %%
rf.fit(X_train, y_train)


# %%
print(f"OOB Score : {rf.oob_score_}")

# %% 
from sklearn.metrics import mean_squared_error

# Predictions on train set
y_pred_test = rf.predict(X_test)

# Print the error
print(f"Test - MSE: {mean_squared_error(y_test, y_pred_test)}")


# %%
# Split features / target
X_train = pd.read_parquet("https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/2_preprocessing/X_train.parquet")
X_test  = pd.read_parquet("https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/2_preprocessing/X_test.parquet")
y_train = pd.read_parquet("https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/2_preprocessing/y_train.parquet")["price_sqm"]
y_test  = pd.read_parquet("https://minio.lab.sspcloud.fr/projet-funathon/2026/project1/data/2_preprocessing/y_test.parquet")["price_sqm"] 


# %%
param_grid = {
    "regressor__RF__n_estimators": [80],
    "regressor__RF__max_features": ["sqrt"],
    "regressor__RF__min_samples_leaf": [40, 50, 75],
    "regressor__RF__max_depth" : [8, 13],
}

# %%
from sklearn.model_selection import GridSearchCV

# Grid search
grid_search = GridSearchCV(
    estimator=model, # it is the TransformedTargetRegressor created in the preprocessing part
    param_grid=param_grid,
    cv=4,  # number of folds
    scoring="r2", # 'r2' or 'neg_root_mean_squared_error' or 'neg_mean_absolute_error'
    n_jobs=-1,
    verbose=2
)

# Train
grid_search.fit(X_train, y_train)
# %%
print(f"Best params : {grid_search.best_params_}")

# %%
rf_model_final = grid_search.best_estimator_
print(type(rf_model_final))

rf_model_final.fit(X_train, y_train)
# %%
y_pred_test = rf_model_final.predict(X_test)
# %%
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
mae  = mean_absolute_error(y_test, y_pred_test)
r2   = r2_score(y_test, y_pred_test)

print(f"Test - RMSE : {rmse:.2f}")
print(f"Test - MAE  : {mae:.2f}")
print(f"Test - R²   : {r2:.4f}")
# %%
