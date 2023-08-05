# SPDX-FileCopyrightText: 2023 Jakub Kozłowicz
#
# SPDX-License-Identifier: MIT

"""Builds messages for the NetworkManager D-Bus communication"""

import uuid

import dbus

from .settings_models import HotspotConnectionSettings, WiFiConnectionSettings


def wifi_connection(
    settings: WiFiConnectionSettings, guid: str = str(uuid.uuid4()).upper()
) -> dbus.Dictionary:
    """Builds wifi connection message for NetworkManager communication."""
    return dbus.Dictionary(
        {
            "connection": dbus.Dictionary(
                {
                    "type": "802-11-wireless",
                    "uuid": guid,
                    "id": settings.ssid,
                    "autoconnect": True,
                    "interface-name": settings.interface,
                }
            ),
            "802-11-wireless": dbus.Dictionary(
                {
                    "ssid": dbus.ByteArray(settings.ssid.encode("utf-8")),
                    "mode": "infrastructure",
                    "security": "802-11-wireles-security",
                }
            ),
            "802-11-wireless-security": dbus.Dictionary(
                {
                    "key-mgmt": "wpa-psk",
                    "auth-alg": "open",
                    "psk": settings.psk,
                }
            ),
            "ipv4": dbus.Dictionary({"method": "auto"}),
            "ipv6": dbus.Dictionary({"method": "auto"}),
        }
    )


def hotspot_connection(
    settings: HotspotConnectionSettings, guid: str = str(uuid.uuid4()).upper()
) -> dbus.Dictionary:
    """Builds hotspot connection message for NetworkManager communication."""
    return dbus.Dictionary(
        {
            "connection": dbus.Dictionary(
                {
                    "type": "802-11-wireless",
                    "uuid": guid,
                    "id": settings.ssid,
                    "autoconnect": False,
                    "interface-name": settings.interface,
                }
            ),
            "802-11-wireless": dbus.Dictionary(
                {
                    "ssid": dbus.ByteArray(settings.ssid.encode("utf-8")),
                    "mode": "ap",
                    "band": "bg",
                    "channel": dbus.UInt32(settings.channel),
                    "security": "802-11-wireles-security",
                }
            ),
            "802-11-wireless-security": dbus.Dictionary(
                {
                    "key-mgmt": "wpa-psk",
                    "proto": dbus.Array(["rsn"]),
                    "group": dbus.Array(["ccmp"]),
                    "pairwise": dbus.Array(["ccmp"]),
                    "psk": settings.psk,
                }
            ),
            "ipv4": dbus.Dictionary(
                {
                    "method": "shared",
                    "address-data": dbus.Array(
                        [
                            dbus.Dictionary(
                                {
                                    "address": settings.ip_address,
                                    "prefix": dbus.UInt32(settings.netmask),
                                }
                            )
                        ],
                        signature=dbus.Signature("a{sv}"),
                    ),
                }
            ),
            "ipv6": dbus.Dictionary({"method": "ignore"}),
        }
    )
