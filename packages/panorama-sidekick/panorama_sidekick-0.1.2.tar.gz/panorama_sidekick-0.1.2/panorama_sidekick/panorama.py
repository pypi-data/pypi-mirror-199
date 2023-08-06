"""Implementation for the Panorama class."""

from typing import Union

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Panorama:
    """Palo Alto Panorama object."""

    def __init__(
        self,
        hostname: str,
        api_key: str,
        timeout: int = 30,
        verify: Union[bool, str] = False,
    ) -> None:
        self.hostname = hostname
        self.api_key = api_key
        self.timeout = timeout
        self.verify = verify

    def get(self, uri: str) -> str:
        """Run HTTP GET API calls.

        Args:
            uri (str): API resource

        Returns:
            str: XML output.
        """
        url = f"https://{self.hostname}/api" + uri
        headers = {"X-PAN-KEY": self.api_key}
        response = requests.get(
            url, headers=headers, timeout=self.timeout, verify=self.verify
        )
        response.raise_for_status()
        return response.text

    def operational_command(self, cmd: str) -> str:
        """Run operational commands.

        Args:
            cmd (str): XML string of the command.

        Returns:
            str: XML output of the API call.
        """
        uri = f"/?type=op&cmd={cmd}"
        return self.get(uri)
