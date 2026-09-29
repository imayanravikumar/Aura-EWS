import pandas as pd

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("patient_timeline_freshness.csv")

print("Loaded:", df.shape)


# ==========================================
# 2. SORT BY PATIENT AND TIME
# ==========================================

df = df.sort_values(
    ["File", "TimeMinutes"]
).reset_index(drop=True)


# ==========================================
# 3. PARAMETERS FOR TREND ANALYSIS
# ==========================================

trend_parameters = [
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
    "Lactate",
    "PaO2",
    "PaCO2",
    "pH",
    "Creatinine",
    "Glucose",
    "WBC"
]


# ==========================================
# 4. CREATE CHANGE FEATURES
# ==========================================

for parameter in trend_parameters:

    if parameter not in df.columns:
        continue

    # Change from previous measurement
    df[parameter + "_Change"] = (
        df.groupby("File")[parameter]
        .diff()
    )


# ==========================================
# 5. CREATE SHORT-TERM RATE OF CHANGE
# ==========================================

for parameter in trend_parameters:

    if parameter not in df.columns:
        continue

    previous_value = (
        df.groupby("File")[parameter]
        .shift(1)
    )

    previous_time = (
        df.groupby("File")["TimeMinutes"]
        .shift(1)
    )

    time_difference = (
        df["TimeMinutes"] - previous_time
    )

    df[parameter + "_Rate"] = (
        (df[parameter] - previous_value)
        / time_difference
    )


# ==========================================
# 6. DISPLAY IMPORTANT FEATURES
# ==========================================

columns_to_show = [
    "File",
    "TimeMinutes",
    "HR",
    "HR_Change",
    "HR_Rate",
    "NIMAP",
    "NIMAP_Change",
    "GCS",
    "GCS_Change",
    "Temp",
    "Temp_Change",
    "RespRate",
    "RespRate_Change"
]

print("\n==============================")
print("CONDITION FEATURES")
print("==============================")

print(df[columns_to_show].head(30))


# ==========================================
# 7. SAVE
# ==========================================

output_file = "condition_features.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n==============================")
print("COMPLETED")
print("==============================")

print("Saved as:", output_file)
print("Final shape:", df.shape)
