import logging
import os
import sys

import yaml

from src.exporter import export_csv, export_json
from src.parser import get_args
from src.ssh_handler import connect_device

DEFAULT_COMMANDS = {
    "interfaces": "show ip interface brief",
    "routes": "show ip route",
}


def load_inventory(path):
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "devices" in data:
        devs = data["devices"]
        return devs if isinstance(devs, list) else []
    raise ValueError(
        f"Inventory {path!r} must be a YAML list of devices or a mapping with a 'devices' key",
    )


def load_commands(path):
    if path is None:
        return dict(DEFAULT_COMMANDS)
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if isinstance(cfg, dict) and "commands" in cfg:
        cmds = cfg["commands"]
    else:
        cmds = cfg
    if not isinstance(cmds, dict):
        raise ValueError(
            f"Commands file {path!r} must be a mapping or contain a 'commands' mapping",
        )
    return cmds


def configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def main() -> int:
    args = get_args()
    configure_logging(args.verbose)
    log = logging.getLogger(__name__)

    try:
        devices = load_inventory(args.inventory)
    except OSError as e:
        log.error("Cannot read inventory: %s", e)
        return 1
    except ValueError as e:
        log.error("%s", e)
        return 1

    if not devices:
        log.warning("No devices in inventory; nothing to do.")
        return 0

    try:
        commands = load_commands(args.commands)
    except OSError as e:
        log.error("Cannot read commands file: %s", e)
        return 1
    except ValueError as e:
        log.error("%s", e)
        return 1

    os.makedirs(args.output_dir, exist_ok=True)

    raw_data = {}
    for device in devices:
        conn = connect_device(device)
        if not conn:
            continue

        device_data = {}
        host = device.get("host", "?")
        for key, cmd in commands.items():
            output = conn.send_command(cmd, use_textfsm=True)
            if isinstance(output, list):
                log.info("%s %s: parsed OK (%d entries)", host, cmd, len(output))
            else:
                log.warning(
                    "%s %s: raw text returned, no TextFSM template matched",
                    host,
                    cmd,
                )
            device_data[key] = output

        raw_data[host] = device_data
        conn.disconnect()

    log.debug("Collected data: %s", raw_data)

    json_path = os.path.join(args.output_dir, "data.json")
    export_json(raw_data, filename=json_path)
    export_csv(raw_data, output_dir=args.output_dir)
    log.info("Wrote %s and CSV files under %s/", json_path, args.output_dir)
    return 0


def cli_main() -> None:
    """Entry point for setuptools console_scripts (propagates exit status)."""
    sys.exit(main())


if __name__ == "__main__":
    cli_main()
