import pandas as pd
import numpy as np
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')

# 1. Quickly retrain the model to ensure it is in memory
print("Initializing Early Warning System...")
df_features = pd.read_csv("time_series_features.csv")
target = "In-hospital_death"
X = df_features.drop(columns=['RecordID', target])
y = df_features[target]

weight_ratio = len(y[y == 0]) / len(y[y == 1])
model = xgb.XGBClassifier(
    n_estimators=200, learning_rate=0.05,
    scale_pos_weight=weight_ratio, missing=np.nan, random_state=42
)
model.fit(X, y)
expected_cols = list(X.columns)

# 2. Load the raw timeline data
df_raw = pd.read_csv("final_ml_dataset.csv")

# 3. Select a specific high-risk patient to monitor
# We will grab the first patient in the dataset who actually deteriorated
high_risk_patients = df_raw[df_raw['In-hospital_death'] == 1]['RecordID'].unique()
patient_id = high_risk_patients[0]  
patient_data = df_raw[df_raw['RecordID'] == patient_id]

print(f"\n==================================================")
print(f"LIVE MONITOR SIMULATION | PATIENT ID: {patient_id}")
print(f"==================================================")

clinical_cols = [c for c in df_raw.columns if c not in [
    'RecordID', 'TimeMinutes', 'File', 'SAPS-I', 'SOFA', 
    'Length_of_stay', 'Survival', 'In-hospital_death'
]]
agg_funcs = ['min', 'max', 'mean', 'std']
agg_dict = {col: agg_funcs for col in clinical_cols}

# 4. Simulate time passing in 4-hour increments
for hour in range(4, 52, 4):
    current_time_mins = hour * 60
    
    # Filter telemetry to only include data available up to this specific hour
    snapshot = patient_data[patient_data['TimeMinutes'] <= current_time_mins]
    
    if snapshot.empty:
        print(f"Hour {hour:02d} | Waiting for telemetry...")
        continue
        
    # Dynamically compute the 372 statistical features for this exact moment in time
    snapshot_features = snapshot.groupby('RecordID').agg(agg_dict)
    snapshot_features.columns = [f"{col[0]}_{col[1]}" for col in snapshot_features.columns]
    
    # Ensure the columns perfectly match what XGBoost was trained on
    snapshot_features = snapshot_features.reindex(columns=expected_cols)
    
    # Generate the live risk prediction
    risk_prob = model.predict_proba(snapshot_features)[0][1]
    
    # Apply our 20% clinical threshold
    alert = "🚨 CRITICAL RISK" if risk_prob >= 0.20 else "✅ STABLE"
    
    print(f"Hour {hour:02d} | Obs: {len(snapshot):03d} | Deterioration Risk: {risk_prob*100:04.1f}% | Status: {alert}")

print("==================================================")
