import logging

from netmiko import ConnectHandler
from netmiko.exceptions import (
    ConnectionException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)

log = logging.getLogger(__name__)


def connect_device(device):
    """Open an SSH connection to a device and return the connection object."""
    host = device.get("host", "?")
    try:
        return ConnectHandler(**device)
    except (NetmikoTimeoutException, NetmikoAuthenticationException, ConnectionException, OSError) as e:
        log.warning("Connection failed: %s - %s", host, e)
        return None
