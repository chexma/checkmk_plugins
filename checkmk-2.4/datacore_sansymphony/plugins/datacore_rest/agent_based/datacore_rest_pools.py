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
    "Alias": "HB51",
    "AutoTieringEnabled": true,
    "Caption": "HB51",
    "ChunkSize": {
        "Value": 134217728
    },
    "DeduplicationState": 0,
    "Description": "SAN Storage Fujitsu NetApp HB51",
    "EncryptionKeyPresent": false,
    "ExtendedCaption": "SSV1-HB51 on ssv1",
    "FreeSpace": {
        "Value": 10949884903424
    },
    "HasEncryption": false,
    "Id": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF:{4d235c44-e5c6-11ed-b80b-98f2b3e70bc1}",
    "InSharedMode": false,
    "Internal": false,
    "IsAuthorized": true,
    "MaxTierNumber": 1,
    "PerformanceData": {
        "BytesAllocated": 168729937707008,
        "BytesAllocatedPercentage": 65,
        "BytesAvailable": 10949884903424,
        "BytesAvailablePercentage": 4,
        "BytesInReclamation": 0,
        "BytesInReclamationPercentage": 0,
        "BytesOverSubscribed": 0,
        "BytesReserved": 84200820572160,
        "BytesReservedPercentage": 31,
        "BytesTotal": 263880643182592,
        "CollectionTime": "/Date(1717881200383)/",
        "DeduplicationPoolFreeSpace": 0,
        "DeduplicationPoolPercentFreeSpace": 0,
        "DeduplicationPoolTotalSpace": 0,
        "DeduplicationPoolUsedSpace": 0,
        "EstimatedDepletionTime": 18446744073709551615,
        "ExpectedDeduplicationPoolUsedSpace": 0,
        "MaxPoolBytes": 1108127332171776,
        "MaxReadTime": 15,
        "MaxReadWriteTime": 15,
        "MaxWriteTime": 15,
        "NullCounterMap": 0,
        "PercentAllocated": 96,
        "PercentAvailable": 4,
        "TotalBytesMigrated": 2606508277760,
        "TotalBytesRead": 25050970373120,
        "TotalBytesTransferred": 44758827710976,
        "TotalBytesWritten": 19707857337856,
        "TotalOperations": 515946348,
        "TotalOperationsTime": 178717277,
        "TotalReadTime": 72907350,
        "TotalReads": 167400110,
        "TotalWriteTime": 105809927,
        "TotalWrites": 348547254
    },
    "PoolMembers": [
        {
            "Caption": "sv1-hb51-vol04",
            "DiskInRecoveryId": "",
            "DiskPoolId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF:{4d235c44-e5c6-11ed-b80b-98f2b3e70bc1}",
            "DiskTier": 1,
            "ExtendedCaption": "Pool disk ssv1-hb51-vol04 on ssv1",
            "Id": "5399554d-4af5-4f92-a056-c64fb1ce5098",
            "Internal": false,
            "IsMirrored": false,
            "MemberState": 0,
            "PhysicalDiskIds": [
                "{0b014904-9a06-4856-944c-51c78b55ee19}"
            ],
            "ReservedChunkCount": 1,
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 584093,
            "Size": {
                "Value": 65970697666560
            },
            "Status": "On-line",
            "StatusLevel": 0
        },
        {
            "Caption": "ssv1-hb51-vol03",
            "DiskInRecoveryId": "",
            "DiskPoolId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF:{4d235c44-e5c6-11ed-b80b-98f2b3e70bc1}",
            "DiskTier": 1,
            "ExtendedCaption": "Pool disk ssv1-hb51-vol03 on ssv1",
            "Id": "14d3e03f-20f2-448d-aad6-4502f66ef706",
            "Internal": false,
            "IsMirrored": false,
            "MemberState": 0,
            "PhysicalDiskIds": [
                "{9160d4fa-1e12-48e0-857f-0568aef7ea98}"
            ],
            "ReservedChunkCount": 1,
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 584091,
            "Size": {
                "Value": 65970697666560
            },
            "Status": "On-line",
            "StatusLevel": 0
        },
        {
            "Caption": "ssv1-hb51-vol02",
            "DiskInRecoveryId": "",
            "DiskPoolId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF:{4d235c44-e5c6-11ed-b80b-98f2b3e70bc1}",
            "DiskTier": 1,
            "ExtendedCaption": "Pool disk ssv1-hb51-vol02 on ssv1",
            "Id": "e60d31b0-e8d3-4cff-b448-181f261fff42",
            "Internal": false,
            "IsMirrored": false,
            "MemberState": 0,
            "PhysicalDiskIds": [
                "{f69c4f3a-9ee8-44cf-9652-0f86b7f8fac1}"
            ],
            "ReservedChunkCount": 1,
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 584089,
            "Size": {
                "Value": 65970697666560
            },
            "Status": "On-line",
            "StatusLevel": 0
        },
        {
            "Caption": "ssv1-hb51-vol01",
            "DiskInRecoveryId": "",
            "DiskPoolId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF:{4d235c44-e5c6-11ed-b80b-98f2b3e70bc1}",
            "DiskTier": 1,
            "ExtendedCaption": "Pool disk ssv1-hb51-vol01 on ssv1",
            "Id": "b3b2466d-42ce-4f0c-afb5-5dfd8a577525",
            "Internal": false,
            "IsMirrored": false,
            "MemberState": 0,
            "PhysicalDiskIds": [
                "{debe8152-474c-4c2b-aa35-126e3f94351f}"
            ],
            "ReservedChunkCount": 1,
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 584087,
            "Size": {
                "Value": 65970697666560
            },
            "Status": "On-line",
            "StatusLevel": 0
        }
    ],
    "PoolMode": 1,
    "PoolStatus": 0,
    "PresenceStatus": 1,
    "SMPAApproved": false,
    "SectorSize": {
        "Value": 512
    },
    "SequenceNumber": 38232392,
    "ServerId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
    "ServerMembers": [
        {
            "HasEncryption": false,
            "IsAuthorized": true,
            "PoolStatus": 0,
            "PresenceStatus": 1,
            "ServerId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "SupportsEncryption": true
        }
    ],
    "SharedPoolId": null,
    "Size": {
        "Value": 263880643182592
    },
    "Status": "Running",
    "StatusLevel": 0,
    "SupportsEncryption": true,
    "TierReservedPct": 0,
    "Type": 0
"""

from cmk_addons.plugins.datacore_rest.lib import (
    parse_datacore_rest,
    discover_datacore_rest,
    convert_timestamp_to_epoch,
    calculate_percentages,
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
    render,
    get_value_store,
    get_rate,
)

from cmk.agent_based.v1 import check_levels

from cmk.plugins.lib.df import (
    check_filesystem_levels,
    FILESYSTEM_DEFAULT_LEVELS,
    MAGIC_FACTOR_DEFAULT_PARAMS,
)


def check_datacore_rest_pools(
    item: str, params: Mapping[str, Any], section: Mapping[str, Any]
) -> CheckResult:
    """Check state of DataCore Pools."""

    value_store = get_value_store()
    data = section.get(item)

    if data is None:
        return

    perfdata = bool("PerformanceData" in data)

    ##########
    # Status #
    ##########

    if not data["Status"] == "Running":
        message = f"Pool status: {data['Status']}"
        yield Result(state=State.CRIT, summary=message)
    else:
        message = f"Pool status: {data['Status']}"
        yield Result(state=State.OK, summary=message)

    ####################
    # Oversubscription #
    ####################

    if int(data["PerformanceData"]["BytesOverSubscribed"]) > 0:
        oversubscribed_bytes = data["PerformanceData"]["BytesOverSubscribed"]
        message = f"Pool is oversubscribed with {render.bytes(oversubscribed_bytes)}"

        # Get oversubscription state from parameters (default: CRIT)
        oversubscription_state = params.get("oversubscription_state", "crit")
        if oversubscription_state == "ignore":
            yield Result(state=State.OK, summary=message)
        elif oversubscription_state == "warn":
            yield Result(state=State.WARN, summary=message)
        else:  # "crit" (default)
            yield Result(state=State.CRIT, summary=message)

    ########
    # Info #
    ########

    sector_size = int(data["SectorSize"]["Value"])
    sector_size_unit = "B" if sector_size == 512 else "K"

    pool_members = []
    for member in data["PoolMembers"]:
        pool_members.append(member["Caption"])

    details = (
        f"Max. Nr. of tiers: {data['MaxTierNumber']}\n"
        f"Tier Reservation: {data['TierReservedPct']}%\n"
        f"Nr. of physical disks: {len(data['PoolMembers'])} \n"
        f"Physical Disks: {",".join(pool_members)} \n"
        f"Sector Size: {sector_size}{sector_size_unit}"
    )

    yield Result(state=State.OK, notice="Pool configuration details available", details=details)

    ####################
    # Performance Data #
    ####################

    if perfdata:

        raw_performance_counters = [
            "TotalReads",
            "TotalWrites",
            "TotalBytesRead",
            "TotalBytesWritten",
            "TotalWriteTime",
            "TotalReadTime",
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

        # Read / Write Ratio

        percent_read, percent_write = calculate_percentages(
            rate["TotalReads"], rate["TotalWrites"]
        )
        message = f"Read/Write Ratio: {int(round(percent_read, 0))}/{int(round(percent_write, 0))}%"
        yield Result(state=State.OK, summary=message)

        # Average Latency
        #
        #  From the above, the Average Time per Write = ∆ TotalWriteTime / ∆ TotalWrites.
        #  $AverageTimeperWrite = $PhysicalDisk1PerformanceReading.TotalWritesTime / $PhysicalDisk1PerformanceReading.TotalWrites

        # Only divide if new data was written
        if rate["TotalReads"] > 0:
            average_read_latency = round(
                (rate["TotalReadTime"] / rate["TotalReads"]), 2
            )
        else:
            average_read_latency = 0

        if rate["TotalWrites"] > 0:
            average_write_latency = round(
                (rate["TotalWriteTime"] / rate["TotalWrites"]), 2
            )
        else:
            average_write_latency = 0

        message = f"avg. read latency: {average_read_latency}, avg. write latency: {average_write_latency}"
        yield Result(state=State.OK, summary=message)

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


agent_section_datacore_rest_pools = AgentSection(
    name="datacore_rest_pools",
    parse_function=parse_datacore_rest,
    parsed_section_name="datacore_rest_pools",
)


check_plugin_datacore_rest_pools = CheckPlugin(
    name="datacore_rest_pools",
    service_name="SANsymphony Pool %s",
    sections=["datacore_rest_pools"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_pools,
    check_ruleset_name="datacore_rest_pools",
    check_default_parameters={
        "oversubscription_state": "crit",  # Default: CRIT for oversubscription
    },
)

#################
# Pool Capacity #
#################

def check_datacore_rest_pool_capacity(
    item: str, params: Mapping[str, Any], section: Mapping[str, Any]
) -> CheckResult:
    data = section.get(item)

    if data is None:
        return

    perfdata = bool("PerformanceData" in data)

    if perfdata:
        # Pool Usage - treat as filesystem
        pool_size = data["Size"]["Value"]
        pool_free = data["FreeSpace"]["Value"]
        pool_allocated = pool_size - pool_free

        # Convert bytes to MB for CheckMK filesystem check
        size_mb = pool_size / 1024.0**2
        free_mb = pool_free / 1024.0**2
        used_mb = pool_allocated / 1024.0**2

        # Normalize parameters: SimpleLevels returns ('fixed', (warn, crit)) or similar
        # but check_filesystem_levels expects just (warn, crit) or more complex dict
        normalized_params = dict(params)

        # Handle SimpleLevels format for 'levels' parameter
        if "levels" in normalized_params:
            levels = normalized_params["levels"]
            if isinstance(levels, tuple) and len(levels) == 2:
                # Check if it's SimpleLevels format: ('fixed', (warn, crit))
                if isinstance(levels[0], str) and levels[0] in ('fixed', 'predictive', 'no_levels'):
                    if levels[0] == 'fixed' and isinstance(levels[1], tuple):
                        normalized_params["levels"] = levels[1]
                    elif levels[0] == 'no_levels':
                        normalized_params.pop("levels", None)

        # Handle SimpleLevels format for 'levels_low' parameter (magic factor)
        if "levels_low" in normalized_params:
            levels_low = normalized_params["levels_low"]
            if isinstance(levels_low, tuple) and len(levels_low) == 2:
                if isinstance(levels_low[0], str) and levels_low[0] == 'fixed':
                    normalized_params["levels_low"] = levels_low[1]
                elif levels_low[0] == 'no_levels':
                    normalized_params.pop("levels_low", None)

        # Handle trend_perfdata SimpleLevels format
        if "trend_perfdata" in normalized_params:
            trend_perfdata = normalized_params["trend_perfdata"]
            if isinstance(trend_perfdata, tuple) and len(trend_perfdata) == 2:
                if isinstance(trend_perfdata[0], str) and trend_perfdata[0] == 'fixed':
                    normalized_params["trend_perfdata"] = trend_perfdata[1]
                elif trend_perfdata[0] == 'no_levels':
                    normalized_params.pop("trend_perfdata", None)

        # Use CheckMK's filesystem checking with magic factor support
        yield from check_filesystem_levels(
            filesystem_size=size_mb,
            allocatable_filesystem_size=size_mb,
            free_space=free_mb,
            used_space=used_mb,
            params=normalized_params,
        )

###

check_plugin_datacore_rest_pool_capacity = CheckPlugin(
    name="datacore_rest_pool_capacity",
    service_name="SANsymphony Pool capacity %s",
    sections=["datacore_rest_pools"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_pool_capacity,
    check_ruleset_name="datacore_rest_pool_capacity",
    check_default_parameters={
        **FILESYSTEM_DEFAULT_LEVELS,
        **MAGIC_FACTOR_DEFAULT_PARAMS,
    },
)
