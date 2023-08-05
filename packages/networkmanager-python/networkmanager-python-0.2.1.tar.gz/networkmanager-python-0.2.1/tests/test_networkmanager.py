"""Tests the NetworkManager object."""

import unittest
from unittest.mock import patch

from networkmanager.messages import hotspot_connection, wifi_connection
from networkmanager.networkmanager import NetworkManager
from networkmanager.settings_models import HotspotConnectionSettings, WiFiConnectionSettings


class TestNetworkManager(unittest.TestCase):
    """Tests NetworkManager object"""

    def setUp(self) -> None:
        self.nm = NetworkManager()

    @patch("dbus.SystemBus")
    def test_add_wifi_connection(self, _) -> None:
        """Tests adding wifi connection"""
        settings = WiFiConnectionSettings(
            ssid="MyWiFi",
            psk="changethispassword",
            interface="wlan0",
        )

        with patch.object(self.nm, "_add_connection") as add_conn_mock:
            connection = wifi_connection(settings)
            self.nm.add_wifi_connection(settings)
            add_conn_mock.assert_called_once_with(connection)

    @patch("dbus.SystemBus")
    def test_add_hotspot_connection(self, _) -> None:
        """Tests adding hotspot connection"""
        settings = HotspotConnectionSettings(
            ssid="test_hotspot",
            psk="password",
            interface="wlan0",
            channel=6,
            ip_address="192.168.10.1",
            netmask=24,
        )

        with patch.object(self.nm, "_add_connection") as add_conn_mock:
            connection = hotspot_connection(settings)
            self.nm.add_hotspot_connection(settings)
            add_conn_mock.assert_called_once_with(connection)


if __name__ == "__main__":
    unittest.main()
