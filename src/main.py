import yaml
from src.ssh_handler import connect_device

# Load devices from YAML
with open("inventory/devices.yaml") as f:
    devices = yaml.safe_load(f)["devices"]

# Commands to run
commands = {
    "interfaces": "show ip interface brief",
    "routes": "show ip route"
}

# Store all results
raw_data = {}

# Loop through devices
for device in devices:
    conn = connect_device(device)
    if not conn:
        continue

    print(f"Connected to {device['host']}")

    device_data = {}

    # Run commands
    for key, cmd in commands.items():
        output = conn.send_command(cmd, use_textfsm=True)
        device_data[key] = output

    raw_data[device["host"]] = device_data

    conn.disconnect()

# Print collected data
print(raw_data)