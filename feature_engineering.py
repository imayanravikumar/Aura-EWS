import pandas as pd

# 1. Load the merged dataset
df = pd.read_csv("final_ml_dataset.csv")

# 2. Identify the clinical columns (ignore IDs, time, and outcomes)
exclude_cols = [
    'RecordID', 'TimeMinutes', 'File', 'SAPS-I', 
    'SOFA', 'Length_of_stay', 'Survival', 'In-hospital_death'
]
clinical_cols = [col for col in df.columns if col not in exclude_cols]

# 3. Aggregate the 48-hour time-series data
print("Aggregating 48-hour trends for each patient...")
agg_funcs = ['min', 'max', 'mean', 'std']

# Create a mapping of {column_name: ['min', 'max', 'mean', 'std']}
agg_dict = {col: agg_funcs for col in clinical_cols}

# Group by patient and apply the statistical functions
df_features = df.groupby('RecordID').agg(agg_dict)

# 4. Flatten the MultiIndex columns (e.g., 'HeartRate', 'min' -> 'HeartRate_min')
df_features.columns = [f"{col[0]}_{col[1]}" for col in df_features.columns]

# 5. Bring back the target outcome
# Since the outcome is static per patient, we just take the first instance
df_outcomes = df.groupby('RecordID')['In-hospital_death'].first()

# Merge the new statistical features with the outcome label
df_final = df_features.join(df_outcomes).reset_index()

print("\n==============================")
print("NEW FEATURE DATASET")
print("==============================")
print(f"Total patients: {len(df_final)}")
print(f"Number of computed features per patient: {len(df_final.columns) - 2}") 
print("\nSample columns:")
print(df_final.columns.tolist()[:10])

# 6. Save the dataset
df_final.to_csv("time_series_features.csv", index=False)
print("\nSaved as: time_series_features.csv")
