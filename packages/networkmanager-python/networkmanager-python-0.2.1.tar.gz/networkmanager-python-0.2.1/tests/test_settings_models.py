# SPDX-FileCopyrightText: 2023 Jakub Kozłowicz
#
# SPDX-License-Identifier: MIT

"""Tests settings models for NetworkManager API."""

import unittest

from networkmanager.settings_models import HotspotConnectionSettings, WiFiConnectionSettings


class SettingsModelsTestCase(unittest.TestCase):
    """Tests for settings models"""

    def test_hotspot_model(self) -> None:
        """Test wifi model"""
        ref = {
            "ssid": "network-name",
            "psk": "network-psk",
            "interface": "eth0",
            "channel": 1,
            "ip_address": "192.168.1.8",
            "netmask": 24,
        }
        settings = HotspotConnectionSettings(
            ssid="network-name",
            psk="network-psk",
            interface="eth0",
            channel=1,
            ip_address="192.168.1.8",
            netmask=24,
        )
        self.assertDictEqual(ref, settings.dict())

    def test_wifi_model(self) -> None:
        """Test wifi model"""
        ref = {
            "ssid": "network-name",
            "psk": "network-psk",
            "interface": "eth0",
        }
        settings = WiFiConnectionSettings(
            ssid="network-name",
            psk="network-psk",
            interface="eth0",
        )
        self.assertDictEqual(ref, settings.dict())


if __name__ == "__main__":
    unittest.main()
