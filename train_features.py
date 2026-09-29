import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.impute import SimpleImputer

# 1. Load the new feature-rich dataset
df = pd.read_csv("time_series_features.csv")

# 2. Define Features and Target
target = "In-hospital_death"
# Drop the ID and target to isolate just the 372 features
X = df.drop(columns=['RecordID', target])
y = df[target]

# 3. Handle Missing Values
# Because we generated so many features, many will be NaN (e.g., if a patient never had a specific lab test)
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# 4. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Train the Model
print("Training Random Forest on 372 Time-Series Features...")
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)

# 6. Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n==============================")
print("NEW MODEL PERFORMANCE")
print("==============================")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
