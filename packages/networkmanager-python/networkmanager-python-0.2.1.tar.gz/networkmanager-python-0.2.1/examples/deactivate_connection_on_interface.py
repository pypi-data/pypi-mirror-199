"""Example for deactivating connection on given interface"""

from networkmanager.networkmanager import NetworkManager


def main() -> None:
    """Main example entrypoint."""
    manager = NetworkManager()
    interface = manager.find_interface_by_name("wlan0")
    manager.deactivate_connection_on_interface(interface)


if __name__ == "__main__":
    main()
