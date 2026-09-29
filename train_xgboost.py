import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb

# 1. Load Data
df = pd.read_csv("time_series_features.csv")
target = "In-hospital_death"
X = df.drop(columns=['RecordID', target])
y = df[target]

# 2. Train/Test Split
# Notice there is NO SimpleImputer here. 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Calculate Class Imbalance Weight
# This mathematically forces XGBoost to care more about the 89 deteriorating patients
weight_ratio = len(y_train[y_train == 0]) / len(y_train[y_train == 1])

# 4. Train the Model
print("Training XGBoost...")
model = xgb.XGBClassifier(
    n_estimators=200,
    learning_rate=0.05,
    scale_pos_weight=weight_ratio,
    missing=np.nan, # Tells XGBoost to treat missing values as a distinct pattern
    random_state=42,
    eval_metric='auc'
)
model.fit(X_train, y_train)

# 5. Predict Probabilities (Not just flat 0 or 1)
y_prob = model.predict_proba(X_test)[:, 1]

# 6. Apply a Custom Clinical Threshold
# We don't wait for 50% certainty to check on a patient. 
# We flag them if the model is even 20% sure they are deteriorating.
CUSTOM_THRESHOLD = 0.20
y_pred_custom = (y_prob >= CUSTOM_THRESHOLD).astype(int)

print("\n==============================")
print("XGBOOST MODEL PERFORMANCE")
print(f"Probability Threshold: {CUSTOM_THRESHOLD}")
print("==============================")
print(classification_report(y_test, y_pred_custom))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
