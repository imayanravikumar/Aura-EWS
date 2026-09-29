import pandas as pd

df = pd.read_csv("patient_state.csv")

print("==============================")
print("PATIENT DATA CHECK")
print("==============================")

processed_patients = set(df["File"].unique())

print(
    "Patients in patient_state.csv:",
    len(processed_patients)
)

rows_per_patient = df.groupby("File").size()

single_row_patients = rows_per_patient[
    rows_per_patient == 1
]

print(
    "\nPatients with only 1 row:",
    len(single_row_patients)
)

print("\nPatients with <= 5 rows:")

print(
    rows_per_patient[
        rows_per_patient <= 5
    ].sort_values()
)

summary = df.groupby("File").agg(
    Start_Time=("TimeMinutes", "min"),
    End_Time=("TimeMinutes", "max"),
    Number_of_Observations=("TimeMinutes", "count")
)

summary["Duration_Minutes"] = (
    summary["End_Time"] -
    summary["Start_Time"]
)

print("\n==============================")
print("TIMELINE SUMMARY")
print("==============================")

print(summary.head(20))

summary.to_csv(
    "patient_timeline_summary.csv"
)

print("\nSaved as:")
print("patient_timeline_summary.csv")
