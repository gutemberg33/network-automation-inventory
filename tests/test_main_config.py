"""Tests for inventory/commands loading helpers in src.main."""

from src.main import load_commands, load_inventory


def test_load_inventory_list(tmp_path):
    inv = tmp_path / "inv.yaml"
    inv.write_text(
        "- host: 1.1.1.1\n  username: u\n  password: p\n  device_type: cisco_ios\n",
        encoding="utf-8",
    )
    rows = load_inventory(inv)
    assert rows == [
        {
            "host": "1.1.1.1",
            "username": "u",
            "password": "p",
            "device_type": "cisco_ios",
        }
    ]


def test_load_inventory_devices_key(tmp_path):
    inv = tmp_path / "inv.yaml"
    inv.write_text(
        "devices:\n"
        "  - host: 2.2.2.2\n"
        "    username: u\n"
        "    password: p\n"
        "    device_type: cisco_ios\n",
        encoding="utf-8",
    )
    rows = load_inventory(inv)
    assert len(rows) == 1
    assert rows[0]["host"] == "2.2.2.2"


def test_load_commands_default():
    assert "interfaces" in load_commands(None)


def test_load_commands_file(tmp_path):
    p = tmp_path / "cmd.yaml"
    p.write_text(
        "commands:\n  a: show version\n  b: show clock\n",
        encoding="utf-8",
    )
    cmds = load_commands(p)
    assert cmds == {"a": "show version", "b": "show clock"}
