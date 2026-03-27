import os
import json
import pytest
from src.exporter import export_json, export_csv

# mock data mimicking TextFSM parsed output
MOCK_DATA = {
    "192.168.1.1": {
        "interfaces": [
            {"intf": "GigabitEthernet0", "ipaddr": "192.168.1.1", "status": "up", "proto": "up"}
        ],
        "routes": [
            {"network": "0.0.0.0", "mask": "0.0.0.0", "nexthop": "192.168.1.254", "protocol": "S"}
        ]
    }
}

def test_export_json_creates_file():
    """JSON file should be created in output directory."""
    export_json(MOCK_DATA, filename="output/test_data.json")
    assert os.path.exists("output/test_data.json")

def test_export_json_content():
    """JSON file should contain correct data."""
    export_json(MOCK_DATA, filename="output/test_data.json")
    with open("output/test_data.json") as f:
        data = json.load(f)
    assert "192.168.1.1" in data

def test_export_csv_creates_files():
    """CSV files should be created per device per section."""
    export_csv(MOCK_DATA)
    assert os.path.exists("output/192.168.1.1_interfaces.csv")
    assert os.path.exists("output/192.168.1.1_routes.csv")