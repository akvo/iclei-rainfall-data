import re
import pandas as pd

SOURCE_FILE = "./source/RAINFALL_DAILY_NDCQ-2024-07-128.txt"

# Read the file
with open(SOURCE_FILE, encoding="utf-8") as f:
    lines = f.readlines()

data = []
CURRENT_STATION = None
CURRENT_DISTRICT = None
DATA_SECTION = False

for line in lines:
    # detect new station & district
    if line.startswith("STATION"):
        # extract station name
        station_match = re.search(r"STATION\s*:\s*(.*?),", line)
        if station_match:
            raw_station = station_match.group(1).strip()
            cleaned_station = re.sub(r"\[.*?\]", "", raw_station).strip()
            cleaned_station = re.sub(r"\s+", " ", cleaned_station)
            cleaned_station = cleaned_station.replace("[", "").strip()
            CURRENT_STATION = cleaned_station

        # extract district name
        district_match = re.search(r"DISTRICT\s*:\s*(.*?),", line)
        if district_match:
            CURRENT_DISTRICT = district_match.group(1).strip()

        DATA_SECTION = False
        continue

    # detect table header
    if re.match(r"^\s*YEAR\s+MN", line):
        DATA_SECTION = True
        continue

    if not DATA_SECTION:
        continue
    if re.match(r"^\s*-{5,}", line) or line.strip() == "":
        continue

    tokens = line.split()
    if len(tokens) < 2:
        continue
    if not tokens[0].isdigit() or not tokens[1].isdigit():
        continue

    year = int(tokens[0])
    month = int(tokens[1])

    for day_offset, val in enumerate(tokens[2:], start=1):
        try:
            rainfall = float(val)
        except ValueError:
            continue
        data.append(
            [
                CURRENT_STATION,
                CURRENT_DISTRICT,
                year,
                month,
                day_offset,
                rainfall,
            ]
        )

df = pd.DataFrame(
    data,
    columns=["Station Name", "District", "Year", "Month", "Date", "Rainfall"],
)

df.to_csv("rainfall_tabular.csv", index=False)

print("All stations & districts saved to rainfall_tabular.csv")
