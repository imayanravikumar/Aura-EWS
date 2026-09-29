import pandas as pd
import zipfile
import re

# 1. Load patient states
df_states = pd.read_csv("patient_state.csv")

# Extract the 6-digit RecordID from the filename (e.g., 'train/set-a/137750.txt' -> 137750)
df_states["RecordID"] = df_states["File"].apply(
    lambda x: int(re.search(r'\d+', str(x)).group())
)

# 2. Load Outcomes
zip_path = "Dataset 2.zip"
with zipfile.ZipFile(zip_path, "r") as z:
    with z.open("train/Outcomes-train.txt") as f:
        df_outcomes = pd.read_csv(f)

# 3. Merge the datasets
# We use an inner join so we only keep patients that exist in both files
df_final = pd.merge(df_states, df_outcomes, on="RecordID", how="inner")

print("==============================")
print("FINAL MERGED DATASET")
print("==============================")
print(f"Total rows (timeline observations): {len(df_final)}")
print(f"Unique patients: {df_final['RecordID'].nunique()}")

# Look at the first few rows for a specific patient to verify the merge
sample_patient = df_final["RecordID"].iloc[0]
print(f"\nSample timeline for patient {sample_patient}:")
cols_to_show = ["RecordID", "TimeMinutes", "In-hospital_death"] 
# Add a couple of your state columns like 'HeartRate_mean' if you know their exact names
print(df_final[cols_to_show].head())

# 4. Save the ML-ready dataset
df_final.to_csv("final_ml_dataset.csv", index=False)
print("\nSaved as: final_ml_dataset.csv")
