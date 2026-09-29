import pandas as pd

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

df = pd.read_csv("cleaned_telemetry.csv")

print("Data loaded!")
print("Total records:", len(df))


# ==========================================
# 2. NUMBER OF PATIENTS
# ==========================================

total_patients = df["File"].nunique()

print("\n==============================")
print("PATIENT INFORMATION")
print("==============================")

print("Total patients:", total_patients)


# ==========================================
# 3. COUNT PATIENTS HAVING EACH PARAMETER
# ==========================================

patients_with_parameter = (
    df.groupby("Parameter")["File"]
    .nunique()
)


# ==========================================
# 4. CALCULATE MISSING PATIENTS
# ==========================================

missing_analysis = pd.DataFrame({
    "Patients_With_Data": patients_with_parameter
})

missing_analysis["Missing_Patients"] = (
    total_patients
    - missing_analysis["Patients_With_Data"]
)

missing_analysis["Missing_Percentage"] = (
    missing_analysis["Missing_Patients"]
    / total_patients
    * 100
)


# ==========================================
# 5. SORT BY MISSING PERCENTAGE
# ==========================================

missing_analysis = missing_analysis.sort_values(
    "Missing_Percentage",
    ascending=False
)


# ==========================================
# 6. DISPLAY RESULTS
# ==========================================

print("\n==============================")
print("MISSING DATA BY PATIENT")
print("==============================")

print(missing_analysis)


# ==========================================
# 7. SAVE REPORT
# ==========================================

missing_analysis.to_csv(
    "missing_data_report_v2.csv"
)

print("\n==============================")
print("ANALYSIS COMPLETED")
print("==============================")

print("Saved as:")
print("missing_data_report_v2.csv")
