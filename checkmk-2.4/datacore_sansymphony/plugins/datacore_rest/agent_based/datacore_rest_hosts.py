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
    "AluaSupport": true,
    "Caption": "esx4",
    "ClientPorts": [
        {
            "Alias": "esx4_1",
            "Caption": "esx4_1",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "esx4_1 on esx4",
            "HostId": "e69ea6aa78bd4b89b9b9ba9f251afa9a",
            "Id": "51-40-2E-C0-12-3F-59-A4",
            "Internal": false,
            "PortMode": 1,
            "PortName": "51-40-2E-C0-12-3F-59-A4",
            "PortType": 2,
            "SequenceNumber": 10529,
            "Status": "Present",
            "StatusLevel": 0
        },
        {
            "Alias": "esx4_2",
            "Caption": "esx4_2",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "esx4_2 on esx4",
            "HostId": "e69ea6aa78bd4b89b9b9ba9f251afa9a",
            "Id": "51-40-2E-C0-12-3F-59-A6",
            "Internal": false,
            "PortMode": 1,
            "PortName": "51-40-2E-C0-12-3F-59-A6",
            "PortType": 2,
            "SequenceNumber": 10530,
            "Status": "Present",
            "StatusLevel": 0
        }
    ],
    "Description": "BRZ - akf  ESX Host 4",
    "ExtendedCaption": "esx4",
    "HostGroupId": null,
    "HostName": "esx4",
    "Id": "e69ea6aa78bd4b89b9b9ba9f251afa9a",
    "Internal": false,
    "MappedServerIds": [
        "B9947E02-76BB-414D-B3C5-2A98FFD8A9D3",
        "9523A4EF-FD25-4B3F-AE67-6986A8C5B0ED"
    ],
    "MpioCapable": true,
    "PathPolicy": 0,
    "PerformanceData": {
        "CollectionTime": "/Date(-62135596800000)/",
        "Latency": 0,
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
    "PreferredServerString": "ssv2",
    "SequenceNumber": 9910,
    "ServerRelations": [
        {
            "Caption": "esx4 | ssv2",
            "ClientId": "e69ea6aa78bd4b89b9b9ba9f251afa9a",
            "ExtendedCaption": "esx4 | ssv2",
            "Id": "a33a1f52-5d7c-42a8-a186-43495d7a92d7",
            "Internal": false,
            "SequenceNumber": 8719,
            "ServerId": "9523A4EF-FD25-4B3F-AE67-6986A8C5B0ED"
        }
    ],
    "State": 2,
    "Status": "Connected",
    "StatusLevel": 0,
    "TelemetryData": {
        "DockerVersion": null,
        "KubernetesVersion": null,
        "NumberOfContainers": 0,
        "PersistentVolumes": null
    },
    "Type": 12
}
"""

from cmk_addons.plugins.datacore_rest.lib import (
    parse_datacore_rest,
    discover_datacore_rest,
    calculate_percentages,
    convert_timestamp_to_epoch,
)


from typing import Any
from collections.abc import Mapping

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
    Metric,
    get_value_store,
    get_rate,
)


def check_datacore_rest_hosts(item: str, section: Mapping[str, Any]) -> CheckResult:
    """Check state of DataCore Hosts."""

    data = section.get(item)

    if data is None:
        return

    perfdata = bool("PerformanceData" in data)

    hosts_status = data["Status"]
    host_ports = data["ClientPorts"]

    ##########
    # Status #
    ##########

    if hosts_status == "Connected":
        host_is_connected = True
        disconnected_ports = []
        # check if host is partially connected
        for port in host_ports:
            if (
                port["Status"] not in ["Present", "Connected"]
                or port["Connected"] is False
            ):
                disconnected_ports.append(port["Caption"])
        if len(disconnected_ports) > 0:
            message = f"Host is only partially connected, disconnected ports: {','.join(disconnected_ports)}"
            yield Result(state=State.WARN, summary=message)
        elif len(disconnected_ports) == 0:
            yield Result(state=State.OK, summary="Connected")
    else:
        host_is_connected = False
        message = "Host is disconnected"
        yield Result(state=State.CRIT, summary=message)

    ########
    # Info #
    ########

    #  "Id": "51-40-2E-C0-12-3F-59-A4",
    # "PortMode": 1,
    # "PortName": "51-40-2E-C0-12-3F-59-A4",
    # "PortType": 2,
    # "Status": "Present",
    # "StatusLevel": 0

    ####################
    # Performance Data #
    ####################

    if perfdata and host_is_connected:

        raw_performance_counters = [
            "TotalReads",
            "TotalWrites",
            "TotalBytesRead",
            "TotalBytesWritten",
            "Latency",
        ]

        # get a reference to the value_store:
        value_store = get_value_store()

        current_collection_time_in_epoch = convert_timestamp_to_epoch(
            data["PerformanceData"]["CollectionTime"]
        )

        rate = {}
        for counter in raw_performance_counters:
            rate[counter] = round(
                get_rate(
                    value_store,
                    f"{item}.{counter}",
                    current_collection_time_in_epoch,
                    data["PerformanceData"][counter],
                    raise_overflow=True,
                )
            )

        performance_metrics = [
            ("disk_read_ios", rate["TotalReads"]),
            ("disk_write_ios", rate["TotalWrites"]),
            ("disk_read_throughput", rate["TotalBytesRead"]),
            ("disk_write_throughput", rate["TotalBytesWritten"]),
            ("latency", rate["Latency"]),
        ]
        for description, metric in performance_metrics:
            yield Metric(description, metric)
        message = (
            f"Read IO/s: {rate['TotalReads']}/s, Write IO/s: {rate['TotalWrites']}/s"
        )
        yield Result(state=State.OK, summary=message)

        percent_read, percent_write = calculate_percentages(
            rate["TotalReads"], rate["TotalWrites"]
        )
        message = f"Read / Write Ratio: {round(percent_read)}/{round(percent_write)}%"
        yield Result(state=State.OK, summary=message)


agent_section_datacore_rest_hosts = AgentSection(
    name="datacore_rest_hosts",
    parse_function=parse_datacore_rest,
    parsed_section_name="datacore_rest_hosts",
)


check_plugin_datacore_rest_hosts = CheckPlugin(
    name="datacore_rest_hosts",
    service_name="SANsymphony Host %s",
    sections=["datacore_rest_hosts"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_hosts,
)
