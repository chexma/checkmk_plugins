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
{
    "Alias": "tier-1-storage",
    "AllServers": [
        "FDD5406C-1664-467B-AACC-889775A2C32E"
    ],
    "BusType": 10,
    "Caption": "tier-1-storage",
    "CompressionSupported": false,
    "DeduplicationSupported": false,
    "DiskIndex": 6,
    "DiskStatus": 1,
    "DvaPoolDiskId": null,
    "ExtendedCaption": "tier-1-storage on SSV1",
    "FreeSpace": {
        "Value": 4177408
    },
    "HardwareEncryptionSupported": false,
    "HostId": "FDD5406C-1664-467B-AACC-889775A2C32E",
    "Id": "{574d760e-75f5-46f6-9534-f820a19f6893}",
    "InUse": true,
    "InquiryData": {
        "Product": "VMware Virtual S",
        "Revision": "1.0 ",
        "Serial": "UNKNOWN",
        "Vendor": "VMware, "
    },
    "Internal": false,
    "IsBootDisk": false,
    "IsDataCoreDisk": false,
    "IsSolidState": false,
    "Partitioned": true,
    "PerformanceData": {
        "AverageQueueLength": 0,
        "CollectionTime": "/Date(-62135596800000)/",
        "MaxReadTime": 0,
        "MaxReadWriteTime": 0,
        "MaxWriteTime": 0,
        "NullCounterMap": 0,
        "PercentIdleTime": 0,
        "TotalBytesRead": 0,
        "TotalBytesTransferred": 0,
        "TotalBytesWritten": 0,
        "TotalOperations": 0,
        "TotalOperationsTime": 0,
        "TotalPendingCommands": 0,
        "TotalReads": 0,
        "TotalReadsTime": 0,
        "TotalWrites": 0,
        "TotalWritesTime": 0
    },
    "PoolMemberId": "2310a495-eeef-4d21-a714-0a43636eda6f",
    "PresenceStatus": 1,
    "Protected": false,
    "ScsiPath": {
        "Bus": 0,
        "LUN": 0,
        "Port": 0,
        "Target": 2
    },
    "SectorSize": {
        "Value": 512
    },
    "SequenceNumber": 163313,
    "SharedPhysicalDiskId": null,
    "Size": {
        "Value": 1073741824
    },
    "SmartStatus": 0,
    "Status": "On-line",
    "StatusLevel": 0,
    "SystemName": "\\\\?\\PhysicalDrive6",
    "Type": 4,
    "UniqueIdentifier": null,
    "Usage": "In pool \"Disk pool 1\""
}"""

from cmk_addons.plugins.datacore_rest.lib import (
    parse_datacore_rest,
    discover_datacore_rest,
    calculate_percentages,
    convert_timestamp_to_epoch,
)

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
    Metric,
    render,
    get_value_store,
    get_rate,
    check_levels,
)


def check_datacore_rest_physicaldisks(item: str, params, section) -> CheckResult:
    """Check state of DataCore physical disks (Backend)"""

    data = section.get(item)
    if data is None:
        return

    perfdata = bool("PerformanceData" in data)

    # Status

    if data["Status"] != "On-line":
        message = "Physical disk is not online"
        yield Result(state=State.CRIT, summary=message)
    else:
        message = "Online"
        yield Result(state=State.OK, summary=message)

    # presence_status = data['PresenceStatus']

    ########
    # Info #
    ########

    size = data["Size"]["Value"]
    # InitializationPercentage = data['InitializationPercentage']
    sector_size = data["SectorSize"]
    # data['MaxReadWriteTime']
    # data['PercentAllocated']

    details = f"Sector Size: {sector_size})"
    message = f"size:  {render.bytes(size)}"

    yield Result(state=State.OK, summary=message, details=details)

    if perfdata:

        raw_performance_counters = [
            "TotalReads",
            "TotalWrites",
            "TotalBytesRead",
            "TotalBytesWritten",
            "TotalWritesTime",
            "TotalReadsTime",
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
                    counter,
                    current_collection_time_in_epoch,
                    data["PerformanceData"][counter],
                    raise_overflow=True,
                )
            )

        message = f"Read IO/s: {rate['TotalReads']}, Write IO/s: {rate['TotalWrites']}"
        yield Result(state=State.OK, summary=message)

        # Read / Write Ratio
        percent_read, percent_write = calculate_percentages(
            rate["TotalReads"], rate["TotalWrites"]
        )
        message = f"Read / Write Ratio: {round(percent_read)}/{round(percent_write)}%"
        yield Result(state=State.OK, summary=message)

        # Average Latency

        #  From the above, the Average Time per Write = ∆ TotalWriteTime / ∆ TotalWrites.
        #  $AverageTimeperWrite = $PhysicalDisk1PerformanceReading.TotalWritesTime / $PhysicalDisk1PerformanceReading.TotalWrites

        if rate["TotalReads"] > 0:
            average_read_latency = round(
                (rate["TotalReadsTime"] / rate["TotalReads"]), 2
            )
        else:
            average_read_latency = 0
        if rate["TotalWrites"] > 0:
            average_write_latency = round(
                (rate["TotalWritesTime"] / rate["TotalWrites"]), 2
            )
        else:
            average_write_latency = 0

        upper_read_latency_levels = params["upper_write_latency_levels"]
        yield from (
            check_levels(
                average_read_latency,
                levels_upper=upper_read_latency_levels,
                label="avg. read latency",
                notice_only=False,
            )
        )

        upper_write_latency_levels = params["upper_write_latency_levels"]
        yield from (
            check_levels(
                average_write_latency,
                levels_upper=upper_write_latency_levels,
                label="avg. write latency",
                notice_only=False,
            )
        )

        # yield all metrics
        performance_metrics = [
            ("disk_read_ios", rate["TotalReads"]),
            ("disk_write_ios", rate["TotalWrites"]),
            ("disk_read_throughput", rate["TotalBytesRead"]),
            ("disk_write_throughput", rate["TotalBytesWritten"]),
            ("read_latency", average_read_latency / 1000),
            ("write_latency", average_write_latency / 1000),
        ]

        for description, metric in performance_metrics:
            yield Metric(description, metric)


agent_section_datacore_rest_physicaldisks = AgentSection(
    name="datacore_rest_physicaldisks",
    parse_function=parse_datacore_rest,
    parsed_section_name="datacore_rest_physicaldisks",
)

check_plugin_datacore_rest_physicaldisks = CheckPlugin(
    name="datacore_rest_physicaldisks",
    service_name="SANsymphony Physical Disk %s",
    sections=["datacore_rest_physicaldisks"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_physicaldisks,
    check_ruleset_name="datacore_rest_physicaldisks",
    check_default_parameters={
        "upper_read_latency_levels": ("no_levels", None),
        "upper_write_latency_levels": ("no_levels", None),
    },
)
