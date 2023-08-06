"""Implementation for the Firewall class."""

from dataclasses import dataclass


@dataclass
class Firewall:
    """Palo Alto Firewall object."""

    name: str
