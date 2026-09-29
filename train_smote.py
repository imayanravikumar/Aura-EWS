import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE

# 1. Load Data
df = pd.read_csv("time_series_features.csv")

target = "In-hospital_death"
X = df.drop(columns=['RecordID', target])
y = df[target]

# 2. Impute Missing Values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# 3. Train/Test Split (Crucial: Split BEFORE SMOTE to prevent data leakage)
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Apply SMOTE only to the training data
print("Applying SMOTE to balance the training data...")
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print(f"Original training target statistics: {y_train.value_counts().to_dict()}")
print(f"SMOTE training target statistics: {y_train_smote.value_counts().to_dict()}")

# 5. Train the Model on the balanced data
print("\nTraining Random Forest...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_smote, y_train_smote)

# 6. Evaluate on the untouched testing data
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n==============================")
print("SMOTE MODEL PERFORMANCE")
print("==============================")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")
