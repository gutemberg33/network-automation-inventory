import sys

from src.parser import get_args


def test_default_inventory(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["network-inventory"])
    args = get_args()
    assert args.inventory == "inventory/devices.yaml"
    assert args.output_dir == "output"
    assert args.commands is None
    assert args.verbose is False


def test_custom_flags(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "network-inventory",
            "--inventory",
            "inv.yaml",
            "--output-dir",
            "out",
            "--commands",
            "cmd.yaml",
            "-v",
        ],
    )
    args = get_args()
    assert args.inventory == "inv.yaml"
    assert args.output_dir == "out"
    assert args.commands == "cmd.yaml"
    assert args.verbose is True
