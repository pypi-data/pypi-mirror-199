"""Defines the commands for showing lists of things."""

import sys
import xml.etree.ElementTree as ET
from typing import List, Optional

import click

from panorama_sidekick.devicegroup import DeviceGroup
from panorama_sidekick.firewall import Firewall
from panorama_sidekick.panorama import Panorama


def parse_show_device_groups_command(panorama: Panorama) -> List[DeviceGroup]:
    cmd = "<show><devicegroups/></show>"
    show_devicegroups = panorama.operational_command(cmd)
    tree = ET.fromstring(show_devicegroups)
    device_group_entries = tree.findall(".//devicegroups/entry")
    device_groups = []
    for dg in device_group_entries:
        firewall_entries = dg.findall(".//devices/entry")
        firewalls = []
        for fw in firewall_entries:
            hostname = fw.findtext("hostname") or "Not-Found"
            firewalls.append(Firewall(hostname))
        device_group_name = dg.attrib["name"]
        device_groups.append(DeviceGroup(device_group_name, firewalls))
    return device_groups


def filter_by_device_group_name(
    name: str,
    device_groups: List[DeviceGroup],
) -> Optional[DeviceGroup]:
    for device_group in device_groups:
        if device_group.name == name:
            return device_group
    return None


@click.command()
@click.pass_obj
def device_groups(panorama: Panorama) -> None:
    """Print a list of device groups."""
    cmd = "<show><devicegroups/></show>"
    show_devicegroups = panorama.operational_command(cmd)
    tree = ET.fromstring(show_devicegroups)
    device_group_names = {
        dg.attrib["name"] for dg in tree.findall(".//devicegroups/entry")
    }
    device_group_names_formatted = "\n".join(sorted(device_group_names))
    click.echo(device_group_names_formatted)


@click.command()
@click.pass_obj
@click.option("-d", "--device-group", help="Filter firewalls by device-group.")
def firewalls(panorama: Panorama, device_group: str) -> None:
    """Print a list of firewalls."""
    device_groups = parse_show_device_groups_command(panorama)
    if device_group:
        for dg in device_groups:
            if device_group != dg.name:
                continue
            break
        else:
            sys.exit(0)
        firewall_names = {fw.name for fw in dg.firewalls}
    else:
        firewall_names = {fw.name for dg in device_groups for fw in dg.firewalls}
    firewall_names_formatted = "\n".join(sorted(firewall_names))
    click.echo(firewall_names_formatted)
