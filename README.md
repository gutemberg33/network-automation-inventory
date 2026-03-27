# Network Automation Inventory Tool

Automates SSH collection of interface and routing data from network devices.
Parses output using TextFSM and exports to JSON and CSV.

## Features
- SSH into multiple devices via Netmiko
- Parses `show ip interface brief` and `show ip route` with TextFSM
- Exports structured data to JSON and CSV
- CLI support for custom inventory files

## Project Structure
```
network-automation-inventory/
├── src/
│   ├── ssh_handler.py      # SSH connection logic
│   └── exporter.py         # JSON and CSV export functions
├── inventory/
│   └── devices.yaml        # device list (not committed)
├── output/                 # exported data lands here
├── main.py
├── requirements.txt
└── README.md
```

## Setup
```bash
# clone the repo
git clone https://github.com/yourname/network-automation-inventory.git
cd network-automation-inventory

# create and activate virtual environment
python -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

# set TextFSM template path
export NET_TEXTFSM=$(python -c "import ntc_templates; print(ntc_templates.__path__[0])")/templates
```

## Inventory File

Create `inventory/devices.yaml` (not committed — see .gitignore):
```yaml
- host: 192.168.1.1
  username: admin
  password: cisco
  device_type: cisco_ios
```

## Usage
```bash
# run with default inventory
python main.py

# run with custom inventory file
python main.py --inventory inventory/lab_devices.yaml
```

## Output

Results are saved to the `output/` folder:
- `output/data.json` — full structured data
- `output/data.csv` — flat CSV for spreadsheet use

## Dependencies
- [Netmiko](https://github.com/ktbyers/netmiko)
- [ntc-templates](https://github.com/networktocode/ntc-templates)
- PyYAML