# %%
y_pred_test = rf_model_final.predict(X_test)

y_pred_test

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
import matplotlib.pyplot as plt


def predicted_actual_plot(y_test, y_pred_test, model_name):
    fig, ax = plt.subplots(figsize=(7, 7))

    ax.scatter(y_test, y_pred_test, alpha=0.3, s=5, label="Predictions")

    lims = [min(y_test.min(), y_pred_test.min()),
            max(y_test.max(), y_pred_test.max())]
    ax.plot(lims, lims, "r--", linewidth=1.5, label="Perfect prediction")

    ax.set_xlabel("Actual values (log)")
    ax.set_ylabel("Predicted values (log)")
    ax.set_title(f"Comparison of predicted values vs. actual values on the test set\n({model_name})")
    ax.legend()
    plt.xscale('log')
    plt.yscale('log')
    return fig


predicted_actual_plot(y_test, y_pred_test, "Random Forest")
# %%
def build_feature_dict(loc_x, loc_y, fare_a, prop_type, feature_dict=None):
    """Return a feature dict ready for the model.

    If `feature_dict` is provided, it is returned unchanged.
    Otherwise, a default dict is built from the required arguments.
    Args:
        loc_x, loc_y : floats
    """
    if feature_dict is not None:
        return feature_dict

    _prop_type_map = {1: "House", 2: "Flat"}
    prop_type_str = _prop_type_map.get(prop_type, str(prop_type))

    return {
        "farea": fare_a,
        "trans_date": "01/02/2023",
        "trans_year": 2023,
        "trans_month": 2,
        "prop_type": prop_type_str,
        "prop_year_harm_10": 1870,
        "prop_loc_x": loc_x,
        "prop_loc_y": loc_y,
        "has_cheating": 0,
        "has_elec": 2,
        "has_elevator": 2,
        "has_gas": 2,
        "has_mdrainage": 2,
        "has_rchute": 0,
        "has_water": 2,
        "n_floors": 6,
        "n_bath": 0,
        "n_eatr": 0,
        "n_kit8": 1,
        "n_kit9": 0,
        "n_ancrooms": 0,
        "n_attic": 1,
        "n_basmt": 1,
        "n_garage": 0,
        "n_pool": 0,
        "n_mrooms": 3,
        "n_otherannex": 0,
        "n_rooms": 4,
        "n_show": 1,
        "n_sink": 1,
        "n_slr": 2,
        "n_terrace": 1,
        "n_washr": 1,
        "n_wc": 1,
        "nth_floor": 3,
        "s_land_agri": 0,
        "s_land_artif": 0,
        "s_land_nat": 0,
        "stair": 2,
    }

    # %%
    prediction_examples = {
    "adresse1" : {"nom" : "88 avenue Verdier 92120 Montrouge", "fare_a" : 80, "loc_x": 2.244608, "loc_y": 48.8865792, "prop_type" : 2},
    "adresse2" : {"nom" : "3 rue Sadi Carnot 78120 Rambouillet", "fare_a" : 140, "loc_x": 1.8300153, "loc_y": 48.6431721, "prop_type" : 1},
    "adresse3" : {"nom" : "1 rue des arts 92700 Colombes", "fare_a" : 35, "loc_x": 2.2410483, "loc_y": 48.9109437, "prop_type" : 2},
    "adresse4" : {"nom" : "152 Rue de Sèvres 75015 Paris", "fare_a" : 93, "loc_x": 2.3146301, "loc_y": 48.8462097, "prop_type" : 2},
    "adresse5" : {"nom" : "3 rue Paul Doumer 93100 Montreuil", "fare_a" : 105, "loc_x": 2.45626, "loc_y": 48.861197, "prop_type" : 1},  
}
# %%
import pandas as pd

# Build a DataFrame with one row per address — batching is faster than
# calling predict() in a loop and ensures consistent column ordering.
rows = []
for key, infos in prediction_examples.items():
    features = build_feature_dict(
        loc_x=infos["loc_x"],
        loc_y=infos["loc_y"],
        fare_a=infos["fare_a"],
        prop_type=infos["prop_type"],
    )
    features["adresse"] = infos["nom"]
    features["id"] = key
    rows.append(features)

X_examples = pd.DataFrame(rows)

# Keep metadata aside; the model only sees the feature columns it was trained on.
meta_cols = ["id", "adresse"]
feature_cols = [c for c in X_examples.columns if c not in meta_cols]

# Predicted price per square meter
predicted_price_sqm = rf_model_final.predict(X_examples[feature_cols])

results = X_examples[meta_cols].copy()
results["price_per_sqm"] = predicted_price_sqm.round(0)
results["surface"]       = X_examples["farea"].values
results["total_price"]   = (results["price_per_sqm"] * results["surface"]).round(0)

for _, row in results.iterrows():
    print(
        f"For the property at {row['adresse']} "
        f"({row['surface']:.0f} sqm), the estimated price is "
        f"{row['price_per_sqm']:,.0f} €/sqm, "
        f"i.e. a total of about {row['total_price']:,.0f} €."
    )
# %%
