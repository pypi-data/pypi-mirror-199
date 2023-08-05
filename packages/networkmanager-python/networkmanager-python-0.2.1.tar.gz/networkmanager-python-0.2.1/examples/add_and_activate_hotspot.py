"""Example for adding hotspot connection and activating it"""

from networkmanager.exceptions import NetworkManagerConnectionNotFound
from networkmanager.networkmanager import NetworkManager
from networkmanager.settings_models import HotspotConnectionSettings


def main() -> None:
    """Main example entrypoint."""
    manager = NetworkManager()
    settings = HotspotConnectionSettings(
        ssid="MyWiFi",
        psk="changethispassword",
        interface="wlan0",
        channel=1,
        ip_address="192.168.8.1",
        netmask=24,
    )

    connection = manager.find_existing_connection_by_ssid(settings.ssid)
    if not connection:
        manager.add_hotspot_connection(settings)

    interface = manager.find_interface_by_name("wlan0")
    connection = manager.find_existing_connection_by_ssid(settings.ssid)
    if not connection:
        raise NetworkManagerConnectionNotFound(
            "Connection not found. Add it first, before trying to activate"
        )

    manager.activate_connection_on_interface(connection, interface)


if __name__ == "__main__":
    main()
