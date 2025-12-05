#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Andre Eckstein <andre.eckstein@bechtle.com>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

"""
Output:

{
    "ActiveOperation": 0,
    "Caption": "myvirtualdisk1 @ 6/2/2024 6:49:10 PM UTC",
    "CompressionEnabled": false,
    "DestinationLogicalDiskId": "4222f406-18de-42fb-aea3-b2ae7d77b679",
    "ExtendedCaption": "myvirtualdisk1 @ 6/2/2024 6:49:10 PM UTC on SSV1",
    "Failure": 0,
    "Id": "V.{7F77F087-202D-11EF-B804-000C2992E794}-00000001--V.{7F77F087-202D-11EF-B804-000C2992E794}-00000003",
    "Internal": false,
    "SequenceNumber": 67462,
    "SourceLogicalDiskId": "032c6b1a-f697-44c0-8d90-cb3698d59bf8",
    "State": 1,
    "TimeStamp": "/Date(1717354164003+0200)/",
    "Type": 0
}
"""

from cmk_addons.plugins.datacore_rest.lib import (
    parse_datacore_rest_single,
    discover_datacore_rest_single,
    convert_epoch_to_readable,
    convert_timestamp_to_epoch,
)

from typing import Any

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
    Metric,
)

agent_section_datacore_rest_snapshots = AgentSection(
    name="datacore_rest_snapshots",
    parse_function=parse_datacore_rest_single,
    parsed_section_name="datacore_rest_snapshots",
)


def check_datacore_rest_snapshots(section: list[Any]) -> CheckResult:
    """Check state of DataCore Snapshots."""

    # The section is a list containing a single list of snapshots: [[snap1, snap2, ...]]
    # Flatten it to get the actual snapshots
    snapshots = section[0] if section and isinstance(section[0], list) else section

    nr_of_snapshots = len(snapshots)

    if nr_of_snapshots == 0:
        message = "No Snapshots present"
        yield Metric("snapshots", 0)
        yield Result(state=State.OK, summary=message)
        return

    snapshot_list = []

    for snapshot in snapshots:
        name = snapshot["Caption"]
        timestamp = snapshot["TimeStamp"]
        snapshot_list.append((convert_timestamp_to_epoch(timestamp), name))

    # Turn around and sort by oldest age
    sorted_snapshots = sorted(snapshot_list, key=lambda x: x[0], reverse=True)
    top_ten_entries = sorted_snapshots[:10]

    details = ""
    for date, message in top_ten_entries:
        details += f"{convert_epoch_to_readable(date)} {message} \n"

    latest_entry = (
        f"{convert_epoch_to_readable(top_ten_entries[0][0])}: "
        f"{top_ten_entries[0][1][:80]}"
    )

    message = f"Snapshots: {nr_of_snapshots}, Latest: {latest_entry}"

    yield Result(state=State.OK, summary=message)


check_plugin_datacore_rest_snapshots = CheckPlugin(
    name="datacore_rest_snapshots",
    service_name="SANsymphony Snapshots",
    sections=["datacore_rest_snapshots"],
    discovery_function=discover_datacore_rest_single,
    check_function=check_datacore_rest_snapshots,
)
