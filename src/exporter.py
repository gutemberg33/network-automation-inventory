import json        # standard library for JSON serialization
import pandas as pd  # data manipulation library for creating and exporting CSVs
import os           # standard library for file system operations (creating directories)

def export_json(data, filename="output/data.json"):
    """Export all collected device data to a single JSON file."""

    # create output directory if it doesn't exist, no error if it already does
    os.makedirs("output", exist_ok=True)

    # write data to JSON file with 4-space indentation for readability
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def export_csv(data, filename_prefix="output"):
    """Export collected device data to separate CSV files per device and section."""

    # create output directory if it doesn't exist, no error if it already does
    os.makedirs("output", exist_ok=True)

    # loop through each device and its sections (interfaces, routes)
    for device, sections in data.items():
        for section, records in sections.items():

            # only export sections where TextFSM returned structured data (list of dicts)
            # skip sections where TextFSM failed and returned raw text (string)
            if isinstance(records, list):
                df = pd.DataFrame(records)  # convert list of dicts to a DataFrame

                # save to CSV named after device and section
                # example: output/192.168.1.1_interfaces.csv
                df.to_csv(f"{filename_prefix}/{device}_{section}.csv", index=False)