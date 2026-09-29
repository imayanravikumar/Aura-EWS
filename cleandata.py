import pandas as pd

# ==========================================
# 1. LOAD THE STRUCTURED DATA
# ==========================================

file_path = "structured_telemetry.csv"

df = pd.read_csv(file_path)

print("Data loaded successfully!")
print("Shape:", df.shape)


# ==========================================
# 2. BASIC INFORMATION
# ==========================================

print("\n==============================")
print("DATA INFORMATION")
print("==============================")

print(df.info())


# ==========================================
# 3. FIRST FEW ROWS
# ==========================================

print("\n==============================")
print("FIRST 10 ROWS")
print("==============================")

print(df.head(10))


# ==========================================
# 4. CHECK MISSING VALUES
# ==========================================

print("\n==============================")
print("MISSING VALUES")
print("==============================")

print(df.isnull().sum())


# ==========================================
# 5. CONVERT VALUE TO NUMERIC
# ==========================================

df["Value"] = pd.to_numeric(df["Value"], errors="coerce")


# ==========================================
# 6. CHECK -1 VALUES
# ==========================================

print("\n==============================")
print("NUMBER OF -1 VALUES")
print("==============================")

print((df["Value"] == -1).sum())


# ==========================================
# 7. REPLACE -1 WITH NaN
# ==========================================

df["Value"] = df["Value"].replace(-1, pd.NA)

print("\n-1 values converted to missing values.")


# ==========================================
# 8. LIST ALL PARAMETERS
# ==========================================

print("\n==============================")
print("PARAMETERS")
print("==============================")

parameters = df["Parameter"].value_counts()

print(parameters)


# ==========================================
# 9. NUMBER OF PATIENTS
# ==========================================

print("\n==============================")
print("PATIENT COUNT")
print("==============================")

print("Number of patients:", df["File"].nunique())


# ==========================================
# 10. RECORD COUNT BY PARAMETER
# ==========================================

print("\n==============================")
print("RECORDS PER PARAMETER")
print("==============================")

print(df["Parameter"].value_counts())


# ==========================================
# 11. SAVE CLEANED DATA
# ==========================================

output_file = "cleaned_telemetry.csv"

df.to_csv(output_file, index=False)

print("\n==============================")
print("CLEANING COMPLETED")
print("==============================")

print("Saved as:", output_file)
print("Final shape:", df.shape)
