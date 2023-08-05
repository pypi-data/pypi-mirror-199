# SPDX-FileCopyrightText: 2023 Jakub Kozłowicz
#
# SPDX-License-Identifier: MIT

"""NetworkManager Python API using D-Bus communication"""

import logging
import time
from typing import Generator, Optional, Union

import dbus

from .exceptions import NetworkManagerDeviceNotConnected
from .messages import hotspot_connection, wifi_connection
from .settings_models import HotspotConnectionSettings, WiFiConnectionSettings


logger = logging.getLogger(__name__)


class NetworkManager:
    """NetworkManager object"""

    _BUS_NETWORKMANAGER_NAME = "org.freedesktop.NetworkManager"
    _BUS_NETWORKMANAGER_PATH = "/org/freedesktop/NetworkManager"

    def __init__(self) -> None:
        self._bus: Union[dbus.SystemBus, None] = None

    def _add_connection(self, connection: dbus.Dictionary) -> None:
        """Add configured connection."""
        if not self._bus:
            self._bus = dbus.SystemBus()

        proxy = self._bus.get_object(
            self._BUS_NETWORKMANAGER_NAME, f"{self._BUS_NETWORKMANAGER_PATH}/Settings"
        )
        nm_settings = dbus.Interface(proxy, f"{self._BUS_NETWORKMANAGER_NAME}.Settings")
        nm_settings.AddConnection(connection)

    def add_wifi_connection(self, settings: WiFiConnectionSettings) -> None:
        """
        Add WiFi connection to NetworkManager system connections.

        :param settings: Setting for the WiFi connection
        :type settings: WiFiConnectionSettings
        """
        connection = wifi_connection(settings)
        self._add_connection(connection)
        logger.info("Added WIFI connection %s", settings.ssid)

    def add_hotspot_connection(self, settings: HotspotConnectionSettings) -> None:
        """
        Add Hotspot connection to NetworkManager system connections.

        :param settings: Setting for the Hotspot connection
        :type settings: HotspotConnectionSettings
        """
        connection = hotspot_connection(settings)
        self._add_connection(connection)
        logger.info("Added Hotspot connection %s", settings.ssid)

    def find_existing_connection_by_ssid(self, ssid: str) -> Optional[str]:
        """Finds if there is any saved connection with given ssid."""
        if not self._bus:
            self._bus = dbus.SystemBus()

        proxy = self._bus.get_object(
            self._BUS_NETWORKMANAGER_NAME, f"{self._BUS_NETWORKMANAGER_PATH}/Settings"
        )
        nm_settings = dbus.Interface(proxy, f"{self._BUS_NETWORKMANAGER_NAME}.Settings")

        connection_path = None
        for path in nm_settings.ListConnections():
            proxy = self._bus.get_object(self._BUS_NETWORKMANAGER_NAME, path)
            settings_connection = dbus.Interface(
                proxy, f"{self._BUS_NETWORKMANAGER_NAME}.Settings.Connection"
            )
            config = settings_connection.GetSettings()
            # Connection settings always are saved with the SSID of the
            # network they are meant.
            if config["connection"]["id"] == ssid:
                connection_path = path
                break

        return connection_path

    def find_interface_by_name(self, interface: str) -> str:
        """Finds interface by the given name"""
        if not self._bus:
            self._bus = dbus.SystemBus()

        proxy = self._bus.get_object(self._BUS_NETWORKMANAGER_NAME, self._BUS_NETWORKMANAGER_PATH)
        nmi = dbus.Interface(proxy, self._BUS_NETWORKMANAGER_NAME)
        return nmi.GetDeviceByIpIface(interface)

    def activate_connection_on_interface(self, connection_path: str, interface_path: str) -> None:
        """Activate given connection on desired interface."""
        if not self._bus:
            self._bus = dbus.SystemBus()

        proxy = self._bus.get_object(self._BUS_NETWORKMANAGER_NAME, self._BUS_NETWORKMANAGER_PATH)
        manager = dbus.Interface(proxy, self._BUS_NETWORKMANAGER_NAME)

        acpath = manager.ActivateConnection(connection_path, interface_path, "/")
        proxy = self._bus.get_object(self._BUS_NETWORKMANAGER_NAME, acpath)
        active_props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")

        # Wait for the hotspot to start up
        start = time.time()
        while time.time() < start + 10:
            state = active_props.Get(f"{self._BUS_NETWORKMANAGER_NAME}.Connection.Active", "State")
            if state == 2:  # NM_ACTIVE_CONNECTION_STATE_ACTIVATED
                logger.info("Connection %s activated", connection_path)
                return

            time.sleep(1)

        logger.error(
            "Failed to activate connection %s on interface %s", connection_path, interface_path
        )

    def deactivate_connection_on_interface(self, interface_path: str) -> None:
        """Deactivate any connection on given interface."""
        if not self._bus:
            self._bus = dbus.SystemBus()

        proxy = self._bus.get_object(self._BUS_NETWORKMANAGER_NAME, interface_path)
        interface = dbus.Interface(proxy, f"{self._BUS_NETWORKMANAGER_NAME}.Device")
        interface_props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")

        # Make sure the device is connected before we try to disconnect it
        state = interface_props.Get(f"{self._BUS_NETWORKMANAGER_NAME}.Device", "State")
        if state <= 3:
            raise NetworkManagerDeviceNotConnected(f"Device {interface_path} is not connected")

        interface.Disconnect()

    def wifi_interfaces(self) -> Generator[dbus.Interface, None, None]:
        """Yields wifi devices in active state."""
        if not self._bus:
            self._bus = dbus.SystemBus()

        nm_proxy = self._bus.get_object(
            self._BUS_NETWORKMANAGER_NAME, self._BUS_NETWORKMANAGER_PATH
        )
        manager = dbus.Interface(nm_proxy, self._BUS_NETWORKMANAGER_NAME)

        # Get all network devices
        devices = manager.GetDevices()
        for device in devices:
            interface_proxy = self._bus.get_object(self._BUS_NETWORKMANAGER_NAME, device)
            interface_props = dbus.Interface(interface_proxy, "org.freedesktop.DBus.Properties")

            # Make sure the device is enabled before we try to use it
            state = interface_props.Get(f"{self._BUS_NETWORKMANAGER_NAME}.Device", "State")
            if state <= 20:  # NM_DEVICE_STATE_UNAVAILABLE
                continue

            # Get device's type; we only want wifi devices
            interface_type = interface_props.Get(
                f"{self._BUS_NETWORKMANAGER_NAME}.Device", "DeviceType"
            )
            if interface_type == 2:  # WiFi
                # Get a proxy for the wifi interface
                yield dbus.Interface(
                    interface_proxy, f"{self._BUS_NETWORKMANAGER_NAME}.Device.Wireless"
                )

    def request_scan(self, interface: dbus.Interface) -> None:
        """Requests scan on Wifi interface and block execution waiting for end."""
        opt = dbus.Dictionary({})
        interface.RequestScan(opt)
        # Not efficient, but should work. In later versions should handle signals
        time.sleep(1)

    def get_all_ap_from_wifi_interface(
        self, interface: dbus.Interface
    ) -> Generator[str, None, None]:
        """Gets all access points from wifi interface."""
        if not self._bus:
            self._bus = dbus.SystemBus()

        # Get all APs the card can see
        access_points = interface.GetAllAccessPoints()
        for path in access_points:
            ap_proxy = self._bus.get_object(self._BUS_NETWORKMANAGER_NAME, path)
            ap_interface_props = dbus.Interface(ap_proxy, "org.freedesktop.DBus.Properties")
            ssid = ap_interface_props.Get(f"{self._BUS_NETWORKMANAGER_NAME}.AccessPoint", "Ssid")
            ssid = "".join([chr(char) for char in ssid])
            yield ssid
