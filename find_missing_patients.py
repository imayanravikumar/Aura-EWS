import pandas as pd
import zipfile
import os

# ==========================================
# 1. LOAD PROCESSED DATA
# ==========================================

df = pd.read_csv("patient_state.csv")

processed_files = set(df["File"].unique())

print("Processed patients:", len(processed_files))


# ==========================================
# 2. READ ORIGINAL ZIP
# ==========================================

zip_path = "Dataset 2.zip"

with zipfile.ZipFile(zip_path, "r") as z:

    all_txt_files = [
        name
        for name in z.namelist()
        if name.endswith(".txt")
    ]


print("TXT files in ZIP:", len(all_txt_files))


# ==========================================
# 3. FIND FILES NOT IN PROCESSED DATA
# ==========================================

original_files = set(all_txt_files)

missing_files = original_files - processed_files


# ==========================================
# 4. DISPLAY
# ==========================================

print("\n==============================")
print("MISSING FILES")
print("==============================")

print("Missing files:", len(missing_files))

for file in sorted(missing_files):
    print(file)
