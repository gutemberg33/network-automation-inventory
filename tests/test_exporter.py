import json

from src.exporter import export_csv, export_json

MOCK_DATA = {
    "192.168.1.1": {
        "interfaces": [
            {
                "intf": "GigabitEthernet0",
                "ipaddr": "192.168.1.1",
                "status": "up",
                "proto": "up",
            }
        ],
        "routes": [
            {
                "network": "0.0.0.0",
                "mask": "0.0.0.0",
                "nexthop": "192.168.1.254",
                "protocol": "S",
            }
        ],
    }
}


def test_export_json_creates_file(tmp_path):
    out = tmp_path / "data.json"
    export_json(MOCK_DATA, filename=str(out))
    assert out.is_file()


def test_export_json_content(tmp_path):
    out = tmp_path / "data.json"
    export_json(MOCK_DATA, filename=str(out))
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "192.168.1.1" in data


def test_export_csv_creates_files(tmp_path):
    export_csv(MOCK_DATA, output_dir=str(tmp_path))
    assert (tmp_path / "192.168.1.1_interfaces.csv").is_file()
    assert (tmp_path / "192.168.1.1_routes.csv").is_file()
