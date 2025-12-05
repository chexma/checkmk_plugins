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

""" "
Output:

{
    "Alias": "MyHostGroup",
    "Caption": "MyHostGroup",
    "Description": "Meine erste Hostgruppe",
    "ExtendedCaption": "MyHostGroup",
    "Id": "{128f44a1-9c80-44d7-b0bd-def632e3f342}",
    "Internal": false,
    "PerformanceData": {
        "CollectionTime": "/Date(-62135596800000)/",
        "MaxOperationSize": 0,
        "MaxReadSize": 0,
        "MaxWriteSize": 0,
        "NullCounterMap": 0,
        "TotalBytesProvisioned": 0,
        "TotalBytesRead": 0,
        "TotalBytesTransferred": 0,
        "TotalBytesWritten": 0,
        "TotalOperations": 0,
        "TotalReads": 0,
        "TotalWrites": 0
    },
    "SequenceNumber": 46,
    "StorageDomainSettings": {
        "ChargeBackEnabled": false,
        "MaxDataTransferredPerSec": 0,
        "MaxIoOperationsPerSec": 0
    }
}
"""

from cmk_addons.plugins.datacore_rest.lib import (
    parse_datacore_rest,
    discover_datacore_rest,
)

from typing import Any
from collections.abc import Mapping

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
)


def check_datacore_rest_hostgroups(item: str, section: Mapping[str, Any]) -> CheckResult:
    """Check state of DataCore Hostgroups."""

    data = section.get(item)
    if data is None:
        return

    max_io_ops_per_sec = data["StorageDomainSettings"]["MaxIoOperationsPerSec"]
    MaxIoOperationsPerSec = (
        max_io_ops_per_sec if max_io_ops_per_sec > 0 else "not enforced"
    )

    max_data_transferred_per_sec = data["StorageDomainSettings"][
        "MaxDataTransferredPerSec"
    ]
    MaxDataTransferredPerSec = (
        max_data_transferred_per_sec
        if max_data_transferred_per_sec > 0
        else "not enforced"
    )

    message = f"{data['Alias']} - Max Operations per Sec: {MaxIoOperationsPerSec}, Max Data Transferred Per Sec: {MaxDataTransferredPerSec}, ChargeBack enabled: {data["StorageDomainSettings"]['ChargeBackEnabled']}"

    yield Result(state=State(0), summary=message)


agent_section_datacore_rest_hostgroups = AgentSection(
    name="datacore_rest_hostgroups",
    parse_function=parse_datacore_rest,
    parsed_section_name="datacore_rest_hostgroups",
)


check_plugin_datacore_rest_hostgroups = CheckPlugin(
    name="datacore_rest_hostgroups",
    service_name="SANsymphony Hostgroup %s",
    sections=["datacore_rest_hostgroups"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_hostgroups,
)
