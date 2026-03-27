import yaml                                      # to load devices from YAML file
import argparse                                  # to handle command line arguments
from src.ssh_handler import connect_device       # handles SSH connection to each device
from src.exporter import export_json, export_csv # functions to save output to files

# define CLI arguments
parser = argparse.ArgumentParser(description="Network Automation Inventory Tool")
parser.add_argument("--inventory", default="inventory/devices.yaml", help="path to devices YAML file")
args = parser.parse_args()

# load devices from YAML inventory file (path from CLI or default)
with open(args.inventory) as f:
    devices = yaml.safe_load(f)

# commands to run on each device
commands = {
    "interfaces": "show ip interface brief",     # get interface status and IPs
    "routes": "show ip route"                    # get routing table
}

raw_data = {}  # will hold all collected data, keyed by device IP/hostname

for device in devices:
    conn = connect_device(device)  # open SSH connection to the device
    if not conn:
        continue                   # skip this device if connection failed

    device_data = {}  # holds this device's command outputs

    for key, cmd in commands.items():
        # send command and parse output into structured data using TextFSM templates
        output = conn.send_command(cmd, use_textfsm=True)
        device_data[key] = output  # store result under "interfaces" or "routes"

    raw_data[device["host"]] = device_data  # add this device's data to the main dict
    conn.disconnect()                        # close SSH connection cleanly

print(raw_data)          # print collected data to terminal for quick inspection
export_json(raw_data)    # save full output as a .json file
export_csv(raw_data)     # save output as a .csv file