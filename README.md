# Network Automation Inventory Tool

A Python tool that reads device credentials from a YAML file, connects over SSH with Netmiko, runs show commands, parses CLI output with TextFSM (`ntc-templates`), and exports structured results to JSON and CSV.

## Features

- SSH to multiple devices via Netmiko
- Parses `show ip interface brief` and `show ip route` with TextFSM (configurable)
- Exports structured data to JSON and CSV
- CLI options for inventory path, output directory, optional commands file, and verbose logging

## Project structure

```
network-automation-inventory/
├── src/
│   ├── main.py             # CLI entry and orchestration
│   ├── parser.py           # Argument parsing
│   ├── ssh_handler.py      # SSH connection logic
│   └── exporter.py         # JSON and CSV export
├── inventory/
│   ├── devices.example.yaml    # copy to devices.yaml (not committed)
│   └── commands.example.yaml   # optional custom command map
├── output/                 # default export directory (generated)
├── tests/
├── pyproject.toml          # package metadata and console script
├── requirements.txt
└── README.md
```

## Setup

```bash
git clone https://github.com/yourname/network-automation-inventory.git
cd network-automation-inventory
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Optional editable install (registers the `network-inventory` command):

```bash
pip install -e .
```

Set the TextFSM template path (required for parsing):

```bash
export NET_TEXTFSM=$(python -c "import ntc_templates; print(ntc_templates.__path__[0])")/templates
```

## Inventory file

Copy the example and edit credentials:

```bash
cp inventory/devices.example.yaml inventory/devices.yaml
```

Supported YAML shapes:

- A **list** of device dicts (each with `host`, `username`, `password`, `device_type`, etc.), or
- A **mapping** with a top-level `devices` key whose value is that list.

## Usage

From the repository root (so `src` is importable):

```bash
python -m src.main
```

With options:

```bash
python -m src.main --inventory inventory/lab.yaml --output-dir output --verbose
python -m src.main --commands inventory/commands.example.yaml
```

If you ran `pip install -e .`:

```bash
network-inventory --inventory inventory/devices.yaml
```

## Output

Under the output directory (default `output/`):

- `data.json` — full nested structure
- `<host>_<section>.csv` — one CSV per device and section when TextFSM returned a list of rows (for example `192.168.1.1_interfaces.csv`)

## Dependencies

- [Netmiko](https://github.com/ktbyers/netmiko)
- [ntc-templates](https://github.com/networktocode/ntc-templates)
- PyYAML

## Tests

```bash
pytest tests/ -v
```
