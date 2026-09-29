import pandas as pd

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("cleaned_telemetry.csv")

print("Data loaded!")
print("Shape:", df.shape)


# ==========================================
# CONVERT VALUE TO NUMERIC
# ==========================================

df["Value"] = pd.to_numeric(df["Value"], errors="coerce")


# ==========================================
# CREATE MISSING INDICATOR
# ==========================================

df["Missing"] = df["Value"].isna().astype(int)


# ==========================================
# MISSING DATA BY PARAMETER
# ==========================================

missing_by_parameter = (
    df.groupby("Parameter")["Missing"]
    .agg(
        Missing_Count="sum",
        Total_Count="count"
    )
)

missing_by_parameter["Missing_Percentage"] = (
    missing_by_parameter["Missing_Count"]
    / missing_by_parameter["Total_Count"]
    * 100
)

missing_by_parameter = missing_by_parameter.sort_values(
    "Missing_Percentage",
    ascending=False
)


print("\n==============================")
print("MISSING DATA BY PARAMETER")
print("==============================")

print(missing_by_parameter)


# ==========================================
# SAVE REPORT
# ==========================================

missing_by_parameter.to_csv(
    "missing_data_report.csv"
)

print("\nSaved:")
print("missing_data_report.csv")
