import gspread
import pandas as pd

# Authenticate Google Sheets API
gc = gspread.service_account(filename=r"C:\Users\Ribisha\Downloads\graphic-pathway-442116-k4-b04a13ed1ede.json")

# Open Google Sheet by its key
worksheet = gc.open_by_key("1lb1WBiZzKCgm0SZMPvt0lCeFkPHqz8MrE-EMz-Sy58w")

# Access the specific worksheet/tab named "Datasheet1"
data = worksheet.worksheet("Datasheet1")

# Fetch all values and convert to DataFrame
values = data.get_all_values()
df = pd.DataFrame(values[1:], columns=values[0])  # First row as column names

# Convert columns to correct data types
df["Day"] = pd.to_datetime(df["Day"], dayfirst=True, errors="coerce")
df["T GMV"] = pd.to_numeric(df["T GMV"], errors="coerce")

# Define new date range
new_dates = pd.date_range(start="2025-01-01", end="2025-02-28", freq='D')

# Store new data
new_rows = []

# Iterate over unique Brand-Channel combinations
for (brand, channel), group in df.groupby(["Brand", "Channel"]):
    last_t_gmv = float(group["T GMV"].values[0])  # Ensure it's numeric

    prev_month = None
    for new_date in new_dates:
        if prev_month is None or new_date.month != prev_month:
            last_t_gmv *= 1.05  # Increase by 5% at the start of the month

        new_rows.append({
            "Brand": brand,
            "Channel": channel,
            "Day": new_date.strftime("%d-%m-%Y"),  # Ensure the date format is dd-mm-yyyy
            "T GMV": round(last_t_gmv, 2)
        })

        prev_month = new_date.month

# Create new DataFrame and append to the original
df_new = pd.DataFrame(new_rows)
df_final = pd.concat([df, df_new], ignore_index=True).sort_values(by=["Brand", "Channel", "Day"])
df_final.reset_index(drop=True, inplace=True)

# Convert 'Day' to datetime for filtering
df_final["Day"] = pd.to_datetime(df_final["Day"], format="%d-%m-%Y", errors="coerce")

# Define date range in datetime format
start_date = pd.to_datetime("2025-01-01")
end_date = pd.to_datetime("2025-02-28")

# Filter data for the given date range
filtered_df = df_final[(df_final["Day"] >= start_date) & (df_final["Day"] <= end_date)]

# Ensure 'Day' column is formatted as dd-mm-yyyy before saving
filtered_df.loc[:, "Day"] = filtered_df["Day"].dt.strftime("%d-%m-%Y")


# Display the filtered DataFrame
print(filtered_df)

# Save to CSV with the correct format for the 'Day' column
filtered_df.to_csv(r"C:\Users\Ribisha\Downloads\filtered_data.csv", index=False)














