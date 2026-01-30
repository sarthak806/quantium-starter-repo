import pandas as pd
import os

data_folder = "data"
all_data = []

for file in os.listdir(data_folder):
    if file.endswith(".csv"):
        file_path = os.path.join(data_folder, file)

        df = pd.read_csv(file_path)

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower()

        # Clean product column
        df["product"] = df["product"].str.strip().str.lower()

        # Keep only pink morsel rows
        df = df[df["product"] == "pink morsel"]

        # Remove $ sign from price and convert to float
        df["price"] = df["price"].str.replace("$", "", regex=False).astype(float)

        # Convert quantity to int
        df["quantity"] = df["quantity"].astype(int)

        # Create sales column
        df["sales"] = df["price"] * df["quantity"]

        # Keep only required columns
        df = df[["sales", "date", "region"]]

        all_data.append(df)

# Combine all CSV files
final_df = pd.concat(all_data, ignore_index=True)

# Save to CSV
final_df.to_csv("final_output.csv", index=False)

print("✅ final_output.csv created successfully")
