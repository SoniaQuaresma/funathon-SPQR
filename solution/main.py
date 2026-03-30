# %%
# ============================================
# STEP 1 — Preprocessing
#   - Outlier removal
#   - One-hot encoding
# ============================================
import pandas as pd
import duckdb
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer, TransformedTargetRegressor
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Create a non-persistent connection (the database exists only while the connection is alive and disappears when it is closed)
con = duckdb.connect(database=":memory:")

# You need to create a secret table with all the S3 credentials
con.execute(
    f"""
CREATE SECRET secret_s3 (
    TYPE S3,
    KEY_ID '{os.environ["AWS_ACCESS_KEY_ID"]}',
    SECRET '{os.environ["AWS_SECRET_ACCESS_KEY"]}',
    ENDPOINT '{os.environ["AWS_S3_ENDPOINT"]}',
    SESSION_TOKEN '{os.environ["AWS_SESSION_TOKEN"]}',
    REGION 'us-east-1',
    URL_STYLE 'path',
    SCOPE 's3://confpns/synthetic-transactions/'
);
"""
)

# We load all transactions made in France between 2010 and 2022
trans = con.sql(
    f"""
        SELECT * FROM read_parquet('s3://confpns/synthetic-transactions/rawdata/transactions/transactions_houses_final.parquet')
        UNION ALL
        SELECT * FROM read_parquet('s3://confpns/synthetic-transactions/rawdata/transactions/transactions_flats_final.parquet')
    """).to_df()

# Filtering to keep rows in Ile de France / Paris region
trans = trans[trans["ccodep"].isin(["75", "77", "78", "91", "92", "93", "94", "95"])]

# Target value
trans["valfonc_m2"] = trans["valeurfonc"] / trans["dsupdc"]

# Filtering
trans = trans[(trans["valfonc_m2"] < 200000) & (trans["valfonc_m2"] > 100)]


# Apply IQR methods for the outlier removal
def outlier_transform(y, lower=0.1, upper=0.9):
    """
    Transform Y target to log(Y) and remove outliers with IQR method

    Args :
        y : target
        lower: lower quantile for the IQR
        upper: upper quantile for the IQR
    """
    Q_lower = np.quantile(y, lower)
    Q_upper = np.quantile(y, upper)
    IQR = Q_upper - Q_lower

    mask = (y >= Q_lower - 1.5 * IQR) & (y <= Q_upper + 1.5 * IQR)
    return mask

mask = outlier_transform(trans["valfonc_m2"])
trans = trans[mask].reset_index(drop=True)

# Drop NAs for target and features
trans = trans.dropna(subset = "valfonc_m2")
trans = trans.dropna()

# Drop useless columns
df = trans.drop(columns=[
    'idmutation', "idnatmut", "libnatmut", 
    "valeurfonc", "ccodep", "depcom", "distance_ltm", "distance_ltm_corr"
])

# Mutating columns dteloc and jannath
df["dteloc"] = pd.Categorical(
    df["dteloc"],
    categories=["1", "2"],
    ordered=False
).rename_categories({"1": "House", "2": "Flat"})

df['jannath_10'] = (df['jannath'] // 10)*10
df['jannath_10'] = df['jannath_10'].where(df['jannath_10'] >= 1850, 1840)

# Dropping old column
df = df.drop(columns=["jannath"])


# Selection of integer columns
numeric_cols = X.select_dtypes(include="integer").columns.to_list()

def date_to_days(X: pd.Series, ref_date:pd.Timestamp):
    # converts a date to a difference to ref_date : 
    diff_dt = pd.to_datetime(X) - ref_date
    # Extract days part from datetime object
    diff_dt = diff_dt.dt.days
    # Transform it from a Pandas series to a Numpy nd array, used by scikit learn for input
    diff_dt = diff_dt.to_numpy().reshape(-1, 1)

    return diff_dt 
    
date_transformer = FunctionTransformer(
    date_to_days,
    kw_args={"ref_date": pd.Timestamp('2010-01-01 00:00')}
    )

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["dteloc", "jannath_10"]),  # one-hot encoder on feature
        ("dat", date_transformer, "datemut") # feature time since 01-01-2010
    ],
    remainder="passthrough"  # to keep features not transformed
) 


# %%
# ============================================
# STEP 3 — Train / test split, model fitting,
#          and performance evaluation
# ============================================

def log_transform(y):
    return np.log10(y)

def inverse_log_transform(y):
    return 10 ** y

y_transformer = FunctionTransformer(
    func = log_transform,
    inverse_func = inverse_log_transform)


rf_params = {
    "n_estimators": 100,
    "max_depth": 5,
    "max_features": "sqrt",
    "min_samples_split": 2,
    "min_samples_leaf": 10,
    "random_state": 202605,
    "oob_score": True,
    "n_jobs": -1,  # The number of jobs to run in parallel, -1 using all processors
}

rf_pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('random forests', RandomForestRegressor(**rf_params))
])

model = TransformedTargetRegressor(
    regressor=rf_pipeline,
    transformer=y_transformer
)

# Split features / target
X = df.drop(columns="valfonc_m2")  # X must contain only the features we'll learn from
y = df["valfonc_m2"]  # target must be a dataframe with 1 column

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=RANDOM_STATE
)

# Full modeling pipeline
model = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=200,
            random_state=RANDOM_STATE,
            n_jobs=-1
        )),
    ]
)

# Fit model
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
rmse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.3f}")
print(f"R² score: {r2:.3f}")
# %%
