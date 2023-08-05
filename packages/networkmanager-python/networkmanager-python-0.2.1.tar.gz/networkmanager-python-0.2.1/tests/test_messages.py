# SPDX-FileCopyrightText: 2023 Jakub Kozłowicz
#
# SPDX-License-Identifier: MIT

"""Tests building messages for NetworkManager package."""

import unittest
import uuid

from dbus import Dictionary

from networkmanager.messages import hotspot_connection, wifi_connection
from networkmanager.settings_models import HotspotConnectionSettings, WiFiConnectionSettings


class TestBuildMessages(unittest.TestCase):
    """Tests building messages for connections."""

    def test_wifi_connection(self) -> None:
        """Tests message for wifi connection."""
        guid: str = str(uuid.uuid4).upper()

        wifi_settings = WiFiConnectionSettings(
            ssid="test_wifi",
            psk="password",
            interface="wlan0",
        )

        expected = Dictionary(
            {
                "connection": Dictionary(
                    {
                        "type": "802-11-wireless",
                        "uuid": guid,
                        "id": wifi_settings.ssid,
                        "autoconnect": True,
                        "interface-name": wifi_settings.interface,
                    }
                ),
                "802-11-wireless": Dictionary(
                    {
                        "ssid": bytearray(wifi_settings.ssid.encode("utf-8")),
                        "mode": "infrastructure",
                        "security": "802-11-wireles-security",
                    }
                ),
                "802-11-wireless-security": Dictionary(
                    {
                        "key-mgmt": "wpa-psk",
                        "auth-alg": "open",
                        "psk": wifi_settings.psk,
                    }
                ),
                "ipv4": Dictionary({"method": "auto"}),
                "ipv6": Dictionary({"method": "auto"}),
            }
        )

        self.assertEqual(wifi_connection(wifi_settings, guid), expected)

    def test_hotspot_connection(self) -> None:
        """Tests message for hotspot connection."""
        guid: str = str(uuid.uuid4).upper()

        hotspot_settings = HotspotConnectionSettings(
            ssid="test_hotspot",
            psk="password",
            interface="wlan0",
            channel=6,
            ip_address="192.168.10.1",
            netmask=24,
        )

        expected = Dictionary(
            {
                "connection": Dictionary(
                    {
                        "type": "802-11-wireless",
                        "uuid": guid,
                        "id": hotspot_settings.ssid,
                        "autoconnect": False,
                        "interface-name": hotspot_settings.interface,
                    }
                ),
                "802-11-wireless": Dictionary(
                    {
                        "ssid": bytearray(hotspot_settings.ssid.encode("utf-8")),
                        "mode": "ap",
                        "band": "bg",
                        "channel": 6,
                        "security": "802-11-wireles-security",
                    }
                ),
                "802-11-wireless-security": Dictionary(
                    {
                        "key-mgmt": "wpa-psk",
                        "proto": ["rsn"],
                        "group": ["ccmp"],
                        "pairwise": ["ccmp"],
                        "psk": hotspot_settings.psk,
                    }
                ),
                "ipv4": Dictionary(
                    {
                        "method": "shared",
                        "address-data": [
                            Dictionary(
                                {
                                    "address": hotspot_settings.ip_address,
                                    "prefix": 24,
                                }
                            )
                        ],
                    }
                ),
                "ipv6": Dictionary({"method": "ignore"}),
            }
        )

        self.assertEqual(hotspot_connection(hotspot_settings, guid), expected)


if __name__ == "__main__":
    unittest.main()
