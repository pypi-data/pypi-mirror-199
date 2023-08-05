# SPDX-FileCopyrightText: 2023 Jakub Kozłowicz
#
# SPDX-License-Identifier: MIT

"""NetworkManager setting models"""

from pydantic import BaseModel


class WiFiConnectionSettings(BaseModel):
    """Settings for the wifi connection."""

    ssid: str
    psk: str
    interface: str


class HotspotConnectionSettings(BaseModel):
    """Settings for the hotspot connection."""

    ssid: str
    psk: str
    interface: str
    channel: int
    ip_address: str
    netmask: int
