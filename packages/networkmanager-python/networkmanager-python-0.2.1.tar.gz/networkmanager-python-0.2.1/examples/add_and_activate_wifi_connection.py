"""Example for adding hotspot connection and activating it"""

from networkmanager.exceptions import NetworkManagerConnectionNotFound
from networkmanager.networkmanager import NetworkManager
from networkmanager.settings_models import WiFiConnectionSettings


def main() -> None:
    """Main example entrypoint."""
    manager = NetworkManager()
    settings = WiFiConnectionSettings(
        ssid="MyWiFi",
        psk="changethispassword",
        interface="wlan0",
    )

    connection = manager.find_existing_connection_by_ssid(settings.ssid)
    if not connection:
        manager.add_wifi_connection(settings)

    interface = manager.find_interface_by_name("wlan0")
    connection = manager.find_existing_connection_by_ssid(settings.ssid)
    if not connection:
        raise NetworkManagerConnectionNotFound(
            "Connection not found. Add it first, before trying to activate"
        )

    manager.activate_connection_on_interface(connection, interface)


if __name__ == "__main__":
    main()
