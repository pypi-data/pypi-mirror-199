"""
sprof exceptions.
"""


class SPFException(Exception):
    """Base exception for sprof."""


class SPFInitError(SPFException, RuntimeError):
    """Raised with something is wrong the project setup."""
