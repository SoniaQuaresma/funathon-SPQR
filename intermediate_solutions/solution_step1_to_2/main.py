# %%
import pandas as pd
from sklearn.compose import make_column_selector as selector
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.model_selection import cross_validate, train_test_split, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, r2_score
from sklearn.dummy import DummyRegressor
import time

from plotnine import (
    ggplot, aes, geom_bar, geom_point, facet_grid,
    labs, theme, element_text, position_dodge
)
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
data_all.loc[data_all["dnbniv"]==0, "dnivrel"] = 0
data_all.loc[data_all["dnbniv"]>0, "dnivrel"] = data_all["dniv"] / data_all["dnbniv"]

# Selecting the only cols we want to use

# %%
# Sample some data
features_list = [
    ["depcom", "x", "y", "dteloc", "dnbppr", "dnbcha", "dsupdc"],
    ['anneemut', 'dteloc', 'jannath', 'ccodep', 'depcom', 'x', 'y','distance_ltm', 'dnbniv', 'dnbbai', 'dnbdou',
       'dnblav', 'dnbwc', 'dnbppr', 'dnbsam', 'dnbcha', 'dnbcu8', 'dnbcu9',
       'dnbsea', 'dnbann', 'dnbpdc', 'dsupdc', 'dniv', 'nb_terrasses',
       'nb_greniers', 'nb_caves', 'nb_autresdep'], 
    ['anneemut', 'dteloc', 'jannath', 'ccodep', 'depcom', 'x', 'y','distance_ltm', 'dnbniv', 'dnbbai', 'dnbdou',
       'dnblav', 'dnbwc', 'dnbppr', 'dnbsam', 'dnbcha', 'dnbcu8', 'dnbcu9',
       'dnbsea', 'dnbann', 'dnbpdc', 'dsupdc', 'dniv', 'nb_terrasses',
       'nb_greniers', 'nb_caves', 'nb_autresdep', 'dnivrel']
] 
target = "price_sqm"
data_75 = data_all[data_all['ccodep'] == '75'].dropna()
# %%
max_target = data_75[target].quantile(0.9)
min_target = data_75[target].quantile(0.1)
data_preproc = data_75[(data_75[target] <= max_target) & (data_75[target] >= min_target)]

# %%
# Encoding issue - differentiate between numeric and other
cols_cat = selector(dtype_exclude="number")
cols_num = selector(dtype_include="number")

# %%
X = data_preproc[features_list[1]]
y = data_preproc[target] # depcom (question encoding ?), dteloc (boolean apt), dnbppr, dnbcha, dsupdc
X.hist(bins=10)
# Features are not troncated
# %%
X.hist(log=True)
# %%
y.hist(bins=10)  # skewed to 0 bcs prices
# %%
y.plot(kind='hist', logx=True, logy=True)  # sharp decrease for assets above 1Me

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
# Impact of tails of price_sqm on model performance
## Option 1 - remove extreme values
# 1a - thresholds 0.1/0.9
max_target = data_75[target].quantile(0.9)
min_target = data_75[target].quantile(0.1)
data_preproc = data_75[(data_75[target] <= max_target) & (data_75[target] >= min_target)]

# 1b - thresholds 0.2/0.8
# max_target = data_75[target].quantile(0.8)
# min_target = data_75[target].quantile(0.2)
# data_preproc = data_75[(data_75[target] <= max_target) & (data_75[target] >= min_target)]
# %%
#| label: nb_features_accuracy
# Impact of nb of features on accuracy :  

scoring = {
    'r2': 'r2',
    'mape': 'neg_mean_absolute_percentage_error'
}

for feature in features_list:
    X = data_preproc[feature]
    y = data_preproc[target] # depcom (question encoding ?), dteloc (boolean apt), dnbppr, dnbcha, dsupdc

    start = time.time()
    cv_results = cross_validate(estimator=model_hist, X=X, y=y, scoring=scoring, return_train_score=True, cv=5)
    elapsed_time = time.time() - start
    
    print(
        f"Data set : \n"
        f"   - {X.shape[1]} col ({list(X.columns)})\n"
        f"   - n_ops : {X.shape[0]} \n"
        f"Training score is : \n"
        f"   - with R² : {cv_results['train_r2'].mean():.3f} +- {cv_results['train_r2'].std():.3f} \n"
        f"   - with MAPE : {-cv_results['train_mape'].mean():.3f} +- {cv_results['train_mape'].std():.3f} \n"
        f"Mean cross validation accuracy is : \n"
        f"   - with R² : {cv_results['test_r2'].mean():.3f} +- {cv_results['test_r2'].std():.3f} \n"
        f"   - with MAPE : {-cv_results['test_mape'].mean():.3f} +- {cv_results['test_mape'].std():.3f} \n"
        f" with an elapsed time of {elapsed_time:.3f}s"
    )

# %%
# features and model 
#| label: features_plus_model_selection 
max_target = data_75[target].quantile(0.9)
min_target = data_75[target].quantile(0.1)
data_preproc = data_75[(data_75[target] <= max_target) & (data_75[target] >= min_target)]

for feature in features_list:
    X = data_preproc[feature]
    y = data_preproc[target] # depcom (question encoding ?), dteloc (boolean apt), dnbppr, dnbcha, dsupdc
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    print(
        f"Data set : \n"
        f"   - {X.shape[1]} col ({list(X.columns)})\n"
        f"   - n_ops : {X.shape[0]} \n"
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
#| label: hyperparams_tuning
dummy_regr = DummyRegressor(strategy="mean")
dummy_regr.fit(X, y)
dummy_regr.score(X, y)
# %%

max_target = data_75[target].quantile(0.9)
min_target = data_75[target].quantile(0.1)
data_preproc = data_75[(data_75[target] <= max_target) & (data_75[target] >= min_target)]

X = data_preproc[features_list[1]]
y = data_preproc[target]

# Hyper parameters tuning
param_grid =   {
    'histgradientboostingregressor__learning_rate': [0.1, 0.5, 0.8], 
    'histgradientboostingregressor__max_iter': [50, 100, 250],
    'histgradientboostingregressor__l2_regularization': [0, 0.01, 0.5],
    'histgradientboostingregressor__max_features': [0.65, 0.75, 0.85]
  }

gs = GridSearchCV(
    model_hist, 
    param_grid, 
    scoring={'neg_mape':'neg_mean_absolute_percentage_error', 'r2':'r2'},
    refit='neg_mape')

gs.fit(X,y)
print(
    f"Best estimator has params : {gs.best_params_} \n associated with a MAPE of {-gs.best_score_}"
)


# %%
#| label: hyperparams_plot
# Extract results
results = pd.DataFrame(gs.cv_results_)[["param_histgradientboostingregressor__learning_rate",
                     "param_histgradientboostingregressor__max_iter",
                     "param_histgradientboostingregressor__max_features",
                     "param_histgradientboostingregressor__l2_regularization",
                     "mean_test_neg_mape",
                     "mean_test_r2"]]
plot_data = results.rename(columns={
    "param_histgradientboostingregressor__learning_rate": "learning_rate",
    "param_histgradientboostingregressor__max_iter": "max_iter",
    "param_histgradientboostingregressor__max_features": "max_features",
    "param_histgradientboostingregressor__l2_regularization": "l2",
    "mean_test_neg_mape": "neg_mape", 
    "mean_test_r2": "r2"
}).dropna()
plot_data["mape"] = -plot_data["neg_mape"]*4  # Scale MAPE to align with R²
plot_data["learning_rate"] = plot_data["learning_rate"].astype(str)
plot_data["max_iter"] = plot_data["max_iter"].astype(str)
plot_data["max_features"] = plot_data["max_features"].astype(str)
plot_data["l2"] = plot_data["l2"].astype(str)

# Create the plot
(
    ggplot() +
    geom_bar(
        aes(x="max_iter", y="mape", fill="l2"),
        data=plot_data,
        stat="identity",
        position="dodge",
        alpha=0.7
    ) +
    geom_point(
        aes(x="max_iter", y="r2", color="l2"),
        data=plot_data,
        position=position_dodge(width=1),
        size=3,
        shape="o"
    ) +
    facet_grid("max_features ~ learning_rate", labeller="label_both") +
    labs(
        title="Hyperparameter Tuning: 4xMAPE (Bars) and R² (Points)",
        x="Max Iterations",
        y="Scaled Metrics (4xMAPE or R²)",
        fill="L2 Regularization",
        color="L2 Regularization",
        caption="Bars: 4xMAPE (%). Points: R²."
    ) +
    theme_matplotlib() +
    theme(
        plot_caption=element_text(hjust=0, size=10, margin={"t": 10}),
        figure_size=(12, 10),
        plot_margin=0.1
    )
)
# %%
