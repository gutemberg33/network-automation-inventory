from netmiko import ConnectHandler  # netmiko library for SSH connections to network devices

def connect_device(device):
    """Open an SSH connection to a device and return the connection object."""
    try:
        # unpack device dict (host, username, password, device_type) into ConnectHandler
        connection = ConnectHandler(**device)
        return connection  # return active connection to be used in main.py

    except Exception as e:
        # if connection fails, print the error and return None so main.py can skip this device
        print(f"Connection failed: {device['host']} - {e}")
        return None