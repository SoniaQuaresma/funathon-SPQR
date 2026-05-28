# %%
import mlflow
import os

mlflow_server = os.getenv("MLFLOW_TRACKING_URI") 
mlflow.set_tracking_uri(mlflow_server)
mlflow.set_experiment("run_rf")


# %%
with mlflow.start_run(run_name="run_rf"):
    ...  # all logging calls go here

# %%
mlflow.set_tags({
    "model_type": "RandomForestRegressor",
    "task": "regression",
    "data_path": "https://minio.lab.sspcloud.fr/...",
    "target_col": y.name,
    "framework": "scikit-learn"
})

mlflow.log_params({
    "test_size": 0.2,
    "max_depth": 5,
    "min_samples_split": 2,
    "random_state": RANDOM_STATE,
    "n_train": len(X_train),
    "n_test": len(X_test),
    "n_features": X.shape[1],
    "target_mean": round(float(y.mean()), 4),
    "target_std": round(float(y.std()), 4),
    "oob_score": True,
    "n_jobs": -1
})

mlflow.log_figure(oob_error_ntrees, "convergence_ntrees_oob_error.png")

mlflow.log_params(grid_search.best_params_)

from sklearn.metrics import root_mean_squared_error, r2_score, mean_absolute_error

y_pred = rf_model_final.predict(X_test)
residuals = y_test - y_pred

metrics = {
    "neg_root_mean_squared_error": root_mean_squared_error(y_test, y_pred),
    "neg_mean_absolute_error": mean_absolute_error(y_test, y_pred),
    "r2": r2_score(y_test, y_pred),
}

mlflow.log_metrics(metrics)

mlflow.log_figure(
    residuals_distribution(residuals, metrics["r2"]),
    "residuals_distrib.png"
)

mlflow.log_figure(QQplot(y_test, y_pred), "qqplot.png")
mlflow.log_figure(target_distribution(y_test), "y_test_distrib.png")
mlflow.log_figure(target_distribution(y_pred), "y_pred_distrib.png")
mlflow.log_figure(
    importance_plot(
        calculate_importance(X_test, y_test, RANDOM_STATE, rf_model_final, "r2")
    ),
    "importance.png"
)

import mlflow.sklearn
from mlflow.models.signature import infer_signature

signature = infer_signature(X_train, rf_model_final.predict(X_train))

mlflow.sklearn.log_model(
    sk_model=rf_model_final,
    name="RF",
    signature=signature,
    input_example=X_train.head(5),
    registered_model_name="rf-run",
)

print(f"Run ID : {mlflow.active_run().info.run_id}")
# %%
