import argparse


def get_args():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        description="Network Automation Inventory Tool",
    )
    parser.add_argument(
        "--inventory",
        default="inventory/devices.yaml",
        help="Path to devices YAML file",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for JSON and CSV exports",
    )
    parser.add_argument(
        "--commands",
        default=None,
        help="Optional YAML file mapping section names to show commands",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    return parser.parse_args()
