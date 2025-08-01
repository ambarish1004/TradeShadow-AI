import json
import csv
import os
from datetime import datetime, timedelta

json_path = "captures/ocr_data.json"
csv_path = "captures/ocr_data.csv"

def clean_old_entries(data):
    now = datetime.now()
    return [
        entry for entry in data
        if datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S") >= now - timedelta(hours=24)
    ]
    
if not os.path.exists(json_path):
    print("❌ JSON file not found.")
    exit()

with open(json_path, "r", encoding="utf-8") as f:
    data = clean_old_entries(json.load(f))  

# Filter only entries with RSI
data = [d for d in data if d.get("rsi") is not None]

with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Timestamp", "RSI", "Extracted_Text"])

    for entry in data:
        writer.writerow([entry["timestamp"], entry["rsi"], entry["text"].replace("\n", " ")])

print(f"✅ Exported to {csv_path}")
