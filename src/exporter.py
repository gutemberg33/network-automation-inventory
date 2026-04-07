import csv
import json
import os


def export_json(data, filename="output/data.json"):
    """Export all collected device data to a single JSON file."""
    parent = os.path.dirname(os.path.abspath(filename))
    if parent:
        os.makedirs(parent, exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def _write_csv_rows(path, rows):
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_csv(data, output_dir="output"):
    """Export collected device data to separate CSV files per device and section."""
    os.makedirs(output_dir, exist_ok=True)

    for device, sections in data.items():
        safe_device = str(device).replace(os.sep, "_").replace("/", "_")
        for section, records in sections.items():
            if isinstance(records, list):
                out_path = os.path.join(output_dir, f"{safe_device}_{section}.csv")
                _write_csv_rows(out_path, records)
