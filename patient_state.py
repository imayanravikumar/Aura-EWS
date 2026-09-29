import pandas as pd

# ==========================================
# 1. LOAD CONDITION FEATURES
# ==========================================

df = pd.read_csv("condition_features.csv")

print("Loaded:", df.shape)


# ==========================================
# 2. HELPER FUNCTION
# ==========================================

def safe_column(name):
    return name if name in df.columns else None


# ==========================================
# 3. HEART RATE INDICATORS
# ==========================================

if "HR" in df.columns:

    df["HR_Low"] = (df["HR"] < 50).astype(int)

    df["HR_High"] = (df["HR"] > 100).astype(int)


# ==========================================
# 4. RESPIRATORY RATE INDICATORS
# ==========================================

if "RespRate" in df.columns:

    df["RespRate_Low"] = (
        df["RespRate"] < 12
    ).astype(int)

    df["RespRate_High"] = (
        df["RespRate"] > 20
    ).astype(int)


# ==========================================
# 5. TEMPERATURE INDICATORS
# ==========================================

if "Temp" in df.columns:

    df["Temp_Low"] = (
        df["Temp"] < 36
    ).astype(int)

    df["Temp_High"] = (
        df["Temp"] > 38
    ).astype(int)


# ==========================================
# 6. GCS CHANGE
# ==========================================

if "GCS_Change" in df.columns:

    df["GCS_Drop"] = (
        df["GCS_Change"] < 0
    ).astype(int)


# ==========================================
# 7. BLOOD PRESSURE / MAP
# ==========================================

if "MAP" in df.columns:

    df["MAP_Low"] = (
        df["MAP"] < 65
    ).astype(int)


if "NIMAP" in df.columns:

    df["NIMAP_Low"] = (
        df["NIMAP"] < 65
    ).astype(int)


# ==========================================
# 8. OXYGENATION
# ==========================================

if "SaO2" in df.columns:

    df["SaO2_Low"] = (
        df["SaO2"] < 92
    ).astype(int)


# ==========================================
# 9. RESPIRATORY SUPPORT
# ==========================================

if "MechVent" in df.columns:

    df["Mechanical_Ventilation"] = (
        df["MechVent"] > 0
    ).astype(int)


# ==========================================
# 10. LACTATE
# ==========================================

if "Lactate" in df.columns:

    df["Lactate_High"] = (
        df["Lactate"] > 2
    ).astype(int)


# ==========================================
# 11. CREATININE
# ==========================================

if "Creatinine" in df.columns:

    df["Creatinine_Change"] = (
        df.groupby("File")["Creatinine"]
        .diff()
    )


# ==========================================
# 12. COUNT CURRENT FLAGS
# ==========================================

flag_columns = [
    "HR_Low",
    "HR_High",
    "RespRate_Low",
    "RespRate_High",
    "Temp_Low",
    "Temp_High",
    "GCS_Drop",
    "MAP_Low",
    "NIMAP_Low",
    "SaO2_Low",
    "Mechanical_Ventilation",
    "Lactate_High"
]

existing_flags = [
    column for column in flag_columns
    if column in df.columns
]

df["Abnormal_Flag_Count"] = (
    df[existing_flags]
    .sum(axis=1)
)


# ==========================================
# 13. DISPLAY
# ==========================================

display_columns = [
    "File",
    "TimeMinutes",
    "HR",
    "RespRate",
    "Temp",
    "GCS",
    "MAP",
    "SaO2",
    "Lactate",
    "Abnormal_Flag_Count"
]

display_columns = [
    column for column in display_columns
    if column in df.columns
]

print("\n==============================")
print("PATIENT STATE")
print("==============================")

print(
    df[display_columns].head(30)
)


# ==========================================
# 14. SAVE
# ==========================================

output_file = "patient_state.csv"

df.to_csv(
    output_file,
    index=False
)

print("\n==============================")
print("COMPLETED")
print("==============================")

print("Saved as:", output_file)
print("Final shape:", df.shape)




