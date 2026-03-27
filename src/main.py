import yaml
from src.ssh_handler import connect_device

with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

for device in devices:
    conn = connect_device(device)
    if conn:
        print(f"Connected to {device['host']}")
        conn.disconnect()