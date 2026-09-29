import pandas as pd

# ==========================================
# 1. LOAD PATIENT TIMELINE
# ==========================================

df = pd.read_csv("patient_timeline.csv")

print("Loaded:", df.shape)


# ==========================================
# 2. PARAMETERS TO TRACK
# ==========================================

parameters = [
    "HR",
    "Temp",
    "GCS",
    "RespRate",
    "NIMAP",
    "NISysABP",
    "NIDiasABP",
    "MAP",
    "SysABP",
    "DiasABP",
    "SaO2",
    "FiO2",
    "MechVent",
    "Urine",
    "Lactate",
    "PaO2",
    "PaCO2",
    "pH",
    "Creatinine",
    "Glucose",
    "WBC"
]


# ==========================================
# 3. SORT DATA
# ==========================================

df = df.sort_values(
    ["File", "TimeMinutes"]
).reset_index(drop=True)


# ==========================================
# 4. CREATE VALUE + AGE FEATURES
# ==========================================

for parameter in parameters:

    if parameter not in df.columns:
        continue

    # Remember when the value was actually measured
    measured_time = df[parameter].notna()

    # Create measurement time
    measurement_time = df["TimeMinutes"].where(
        measured_time
    )

    # Carry the measurement time forward
    measurement_time = (
        measurement_time
        .groupby(df["File"])
        .ffill()
    )

    # Carry the value forward
    df[parameter] = (
        df.groupby("File")[parameter]
        .ffill()
    )

    # Calculate age of measurement in minutes
    df[parameter + "_Age"] = (
        df["TimeMinutes"] - measurement_time
    )


# ==========================================
# 5. DISPLAY RESULTS
# ==========================================

print("\n==============================")
print("TIME-AWARE DATA")
print("==============================")

columns_to_show = [
    "File",
    "TimeMinutes",
    "HR",
    "HR_Age",
    "Temp",
    "Temp_Age",
    "Creatinine",
    "Creatinine_Age"
]

print(
    df[columns_to_show].head(20)
)


# ==========================================
# 6. SAVE
# ==========================================

output_file = "patient_timeline_freshness.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n==============================")
print("COMPLETED")
print("==============================")

print("Saved as:", output_file)

print("Final shape:", df.shape)
