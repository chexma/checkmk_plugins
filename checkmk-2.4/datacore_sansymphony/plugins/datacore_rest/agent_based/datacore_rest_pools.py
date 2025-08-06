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
    FILESYSTEM_DEFAULT_LEVELS,
    MAGIC_FACTOR_DEFAULT_PARAMS,
)


def check_datacore_rest_pools(item: str, params, section) -> CheckResult:
    """Check state of DataCore Pools"""

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

    if int(data["PerformanceData"]["BytesOverSubscribed"]) > 0:
        message = (
            f"Pool is oversubscribed with "
            f"{render.bytes(data["PerformanceData"]["BytesOverSubscribed"])}"
        )
        yield Result(state=State.CRIT, summary=message)

    ########
    # Info #
    ########

    sector_size = int(data["SectorSize"]["Value"])
    sector_size_unit = "B" if sector_size == 512 else "K"

    pool_members = []
    for member in data["PoolMembers"]:
        pool_members.append(f"{member["Caption"]}")

    details = (
        f"Max. Nr. of tiers: {data['MaxTierNumber']}\n"
        f"Tier Reservation: {data['TierReservedPct']}%\n"
        f"Nr. of physical disks: {len(data['PoolMembers'])} \n"
        f"Physical Disks: {",".join(pool_members)} \n"
        f"Sector Size: {sector_size}{sector_size_unit}"
    )

    yield Result(state=State.OK, notice="test", details=details)

    ####################
    # Performance Data #
    ####################

    if perfdata:

        # Pool Usage
        pool_size = data["Size"]["Value"]
        pool_free = data["FreeSpace"]["Value"]
        pool_allocated = pool_size - pool_free

        warn, crit = params["levels"]

        yield from check_levels(
            100.0 * pool_allocated / pool_size,
            levels_upper=(warn, crit),
            metric_name="fs_used_percent",
            render_func=render.percent,
            boundaries=(0.0, 100.0),
            label="Used",
        )

        yield Metric("fs_size", pool_size, boundaries=(0, None))
        yield Metric("fs_free", pool_free, boundaries=(0, None))
        yield Metric("fs_used", pool_allocated, boundaries=(0, None))

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
                    counter,
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
    check_default_parameters={
        **FILESYSTEM_DEFAULT_LEVELS,
        **MAGIC_FACTOR_DEFAULT_PARAMS,
    },
    check_ruleset_name="sansymphony_pool",
)
