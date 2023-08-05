# SPDX-FileCopyrightText: 2023 Jakub Kozłowicz
#
# SPDX-License-Identifier: MIT

"""Tests exceptions for NetworkManager package"""

import unittest

from networkmanager.exceptions import (
    NetworkManagerConnectionNotFound,
    NetworkManagerDeviceNotConnected,
)


class TestNetworkManagerExceptions(unittest.TestCase):
    """Tests exceptions for package"""

    def test_network_manager_connection_not_found(self) -> None:
        """Tests connection not found exception"""
        with self.assertRaises(NetworkManagerConnectionNotFound):
            raise NetworkManagerConnectionNotFound("Connection not found")

    def test_network_manager_device_not_connected(self) -> None:
        """Tests device not found exception"""
        with self.assertRaises(NetworkManagerDeviceNotConnected):
            raise NetworkManagerDeviceNotConnected("Device not connected")


if __name__ == "__main__":
    unittest.main()
