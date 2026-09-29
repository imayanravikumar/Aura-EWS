import pandas as pd

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

df = pd.read_csv("cleaned_telemetry.csv")

print("Data loaded:", df.shape)


# ==========================================
# 2. CONVERT VALUE TO NUMERIC
# ==========================================

df["Value"] = pd.to_numeric(
    df["Value"],
    errors="coerce"
)


# ==========================================
# 3. CONVERT TIME TO MINUTES
# ==========================================

def time_to_minutes(time_string):

    hours, minutes = time_string.split(":")

    return int(hours) * 60 + int(minutes)


df["TimeMinutes"] = df["Time"].apply(
    time_to_minutes
)


# ==========================================
# 4. SELECT IMPORTANT PARAMETERS
# ==========================================

important_parameters = [
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


df = df[
    df["Parameter"].isin(important_parameters)
]


# ==========================================
# 5. CREATE PATIENT-TIME TABLE
# ==========================================

timeline = df.pivot_table(
    index=["File", "TimeMinutes"],
    columns="Parameter",
    values="Value",
    aggfunc="last"
)


# ==========================================
# 6. RESET INDEX
# ==========================================

timeline = timeline.reset_index()


# ==========================================
# 7. SORT CHRONOLOGICALLY
# ==========================================

timeline = timeline.sort_values(
    ["File", "TimeMinutes"]
)


# ==========================================
# 8. DISPLAY RESULT
# ==========================================

print("\n==============================")
print("PATIENT TIMELINE")
print("==============================")

print(timeline.head(20))


print("\nShape:")
print(timeline.shape)


# ==========================================
# 9. SAVE
# ==========================================

timeline.to_csv(
    "patient_timeline.csv",
    index=False
)

print("\nSaved as:")
print("patient_timeline.csv")
