import argparse  # standard library for CLI argument parsing

def get_args():
    """Parse and return command line arguments."""
    parser = argparse.ArgumentParser(
        description="Network Automation Inventory Tool"  # shown in --help output
    )
    parser.add_argument(
        "--inventory",
        default="inventory/devices.yaml",  # fallback if no argument provided
        help="path to devices YAML file"   # shown in --help output
    )
    return parser.parse_args()  # returns args.inventory, args.format, etc.