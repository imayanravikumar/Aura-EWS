import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.impute import SimpleImputer

# 1. Load Data
df = pd.read_csv("final_ml_dataset.csv")

# 2. Isolate the final observation for each patient
# This prevents data leakage by ensuring 1 patient = 1 row in the training set
df_last_state = df.sort_values("TimeMinutes").groupby("RecordID").tail(1)

# 3. Define Features and Target
target = "In-hospital_death"
# Exclude metadata and future outcome columns from the training features
exclude_cols = ['RecordID', 'TimeMinutes', 'File', 'SAPS-I', 'SOFA', 'Length_of_stay', 'Survival', 'In-hospital_death']
features = [col for col in df.columns if col not in exclude_cols]

X = df_last_state[features]
y = df_last_state[target]

# 4. Handle Missing Values
# Medical data has gaps; we will impute missing values with the column mean for now
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# 5. Train/Test Split
# Stratify ensures the 80/20 split maintains the same survival/death ratio
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42, stratify=y
)

# 6. Train the Model
print("Training Random Forest Classifier...")
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)

# 7. Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
