from netmiko import ConnectHandler

def connect_device(device):
    try:
        connection = ConnectHandler(**device)
        return connection
    except Exception as e:
        print(f"Connection failed: {device['host']} - {e}")
        return None