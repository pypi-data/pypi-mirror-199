"""Implementation for the DeviceGroup class."""

from dataclasses import dataclass
from typing import List

from panorama_sidekick.firewall import Firewall


@dataclass
class DeviceGroup:
    """Palo Alto Device Group object."""

    name: str
    firewalls: List[Firewall]
