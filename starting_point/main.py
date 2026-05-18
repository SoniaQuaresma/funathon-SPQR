# %%
# ============================================
# STEP 1 — Generate synthetic regression data
# ============================================

# YOUR CODE HERE
from sklearn.datasets import make_regression
import pandas as pd

X, y = make_regression(n_samples=200, n_features=3, noise=15, random_state=42)

df = pd.DataFrame(X, columns=['X1', 'X2', 'X3'])
df['y'] = y
print(df.head(3))

# %%
# ============================================
# STEP 2 — Preprocessing
# ============================================

# YOUR CODE HERE


# %%
# ============================================
# STEP 3 — Train / test split, model fitting,
#          and performance evaluation
# ============================================

# YOUR CODE HERE

# %%
