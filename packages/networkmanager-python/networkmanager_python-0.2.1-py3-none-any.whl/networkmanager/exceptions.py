"""Custom NetworkManager exceptions"""


class NetworkManagerBaseException(Exception):
    """Base NetworkManager exception"""


class NetworkManagerConnectionNotFound(NetworkManagerBaseException):
    """Raised when connection was not found"""


class NetworkManagerDeviceNotConnected(NetworkManagerBaseException):
    """Raised when device has no connection and user try to disconnect on that device"""
