import json
import pandas as pd
import os

def export_json(data, filename="output/data.json"):
    os.makedirs("output", exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def export_csv(data, filename_prefix="output"):
    os.makedirs("output", exist_ok=True)

    for device, sections in data.items():
        for section, records in sections.items():
            if isinstance(records, list):
                df = pd.DataFrame(records)
                df.to_csv(f"{filename_prefix}/{device}_{section}.csv", index=False)