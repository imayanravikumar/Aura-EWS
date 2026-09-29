import zipfile
import csv
import pandas as pd

# ==============================
# 1. ZIP FILE LOCATION
# ==============================

zip_path = "Dataset 2.zip"


# ==============================
# 2. READ ZIP FILE
# ==============================

all_records = []

with zipfile.ZipFile(zip_path, "r") as z:

    # Find all patient text/CSV files
    files = [
        f for f in z.namelist()
        if f.lower().endswith(".txt") or f.lower().endswith(".csv")
    ]

    print("Files found:", len(files))

    # Process ALL files
    for count, filename in enumerate(files, start=1):

        with z.open(filename) as file:

            reader = csv.reader(
                line.decode("utf-8", errors="ignore")
                for line in file
            )

            # Skip header
            next(reader, None)

            # Read every row
            for row in reader:

                # Make sure row has Time, Parameter, Value
                if len(row) != 3:
                    continue

                time = row[0].strip()
                parameter = row[1].strip()
                value = row[2].strip()

                all_records.append({
                    "Time": time,
                    "Parameter": parameter,
                    "Value": value,
                    "File": filename
                })

        # Show progress every 100 files
        if count % 100 == 0:
            print("Processed:", count, "files")


# ==============================
# 3. CREATE DATAFRAME
# ==============================

df = pd.DataFrame(all_records)


# ==============================
# 4. DISPLAY RESULTS
# ==============================

print("\n==============================")
print("PARSING COMPLETED")
print("==============================")

print("Total patient files:", df["File"].nunique())
print("Total records:", len(df))

print("\nFirst 20 records:")
print(df.head(20))

print("\nData shape:")
print(df.shape)


# ==============================
# 5. SAVE STRUCTURED DATA
# ==============================

output_file = "structured_telemetry.csv"

df.to_csv(output_file, index=False)

print("\nSaved successfully as:")
print(output_file)
