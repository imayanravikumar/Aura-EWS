import pandas as pd

# Load cleaned data
df = pd.read_csv("cleaned_telemetry.csv")

print("Data loaded!")
print("Shape:", df.shape)


# ==========================================
# 1. COUNT OBSERVATIONS FOR EACH PARAMETER
# ==========================================

parameter_counts = df["Parameter"].value_counts()

print("\n==============================")
print("PARAMETER COUNTS")
print("==============================")

print(parameter_counts)


# ==========================================
# 2. NUMBER OF PATIENTS
# ==========================================

patient_count = df["File"].nunique()

print("\n==============================")
print("PATIENT COUNT")
print("==============================")

print(patient_count)


# ==========================================
# 3. PATIENTS WITH EACH PARAMETER
# ==========================================

patients_per_parameter = (
    df.groupby("Parameter")["File"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n==============================")
print("PATIENTS PER PARAMETER")
print("==============================")

print(patients_per_parameter)


# ==========================================
# 4. SAVE THE ANALYSIS
# ==========================================

patients_per_parameter.to_csv(
    "patients_per_parameter.csv"
)

print("\nAnalysis saved as:")
print("patients_per_parameter.csv")
