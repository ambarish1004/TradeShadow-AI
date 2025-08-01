import json
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta

json_path = "captures/ocr_data.json"

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

# Filter valid RSI entries
timestamps = []
rsi_values = []

for entry in data:
    try:
        ts = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
        if entry.get("rsi") is not None:
            timestamps.append(ts)
            rsi_values.append(entry["rsi"])
    except:
        continue

if not rsi_values:
    print("⚠️ No valid RSI data found.")
    exit()

# 📊 Plotting
plt.figure(figsize=(10, 5))
plt.plot(timestamps, rsi_values, marker='o', linestyle='-', color='blue')
plt.axhline(70, color='red', linestyle='--', label="Overbought (70)")
plt.axhline(30, color='green', linestyle='--', label="Oversold (30)")
plt.title("📈 RSI Trend Over Time")
plt.xlabel("Time")
plt.ylabel("RSI Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.grid(True)
plt.show()
