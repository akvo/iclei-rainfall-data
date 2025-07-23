import os
import re
import pandas as pd

# Define the paths to the source file and destination directory
SOURCE_FILE = "./source/RAINFALL_DAILY_NDCQ-2024-07-128.txt"
DESTINATION_DIR = "./results/"

# Ensure the destination directory exists
os.makedirs(DESTINATION_DIR, exist_ok=True)


# Function to clean and format the station name
def clean_station_name(station_name):
    return (
        station_name.strip()
        .lower()
        .replace(" ", "_")
        .replace("(", "")
        .replace(")", "")
    )


# Read the file line by line and process it
with open(SOURCE_FILE, "r") as file:
    station_name = None
    headers = []
    data = []
    capture_data = False

    for line in file:
        # Check for station name
        station_match = re.match(r"STATION\s*:\s*([A-Z\s]+)", line)
        if station_match:
            # Save the previous station data if exists
            if station_name and headers and data:
                df = pd.DataFrame(data, columns=headers)
                xlsx_filename = f"{clean_station_name(station_name)}.xlsx"
                destination_path = os.path.join(DESTINATION_DIR, xlsx_filename)
                df.to_excel(destination_path, index=False)
                print(f"Created new file: {destination_path}")

            # Start new station section
            station_name = station_match.group(1)
            headers = []
            data = []
            capture_data = False

        # Check for header line (after the first line of dashes)
        if re.match(r"-{2,}", line):
            if not headers:
                # Next line should be headers
                headers = next(file).split()
            else:
                # Now start capturing data
                capture_data = True
            continue

        # Capture data lines
        if capture_data:
            row = line.split()
            if row:
                data.append(row)

    # Save the last station data
    if station_name and headers and data:
        df = pd.DataFrame(data, columns=headers)
        xlsx_filename = f"{clean_station_name(station_name)}.xlsx"
        destination_path = os.path.join(DESTINATION_DIR, xlsx_filename)
        df.to_excel(destination_path, index=False)
        print(f"Created new file: {destination_path}")

if not station_name:
    print("No 'STATION' found in the file.")
