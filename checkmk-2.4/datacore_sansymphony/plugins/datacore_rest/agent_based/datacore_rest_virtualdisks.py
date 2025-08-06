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
Example Output
{
    "Alias": "test-1",
    "BackupHostId": null,
    "Caption": "test-1",
    "CompressionEnabled": true,
    "DeduplicationEnabled": true,
    "Description": null,
    "Disabled": false,
    "DiskLayout": {
        "Cylinders": 0,
        "Heads": 0,
        "SectorsPerTrack": 0
    },
    "DiskStatus": 0,
    "EncryptionEnabled": false,
    "ExtendedCaption": "test-1 from Server Group",
    "FirstHostId": "FDD5406C-1664-467B-AACC-889775A2C32E",
    "HostId": null,
    "Id": "65e604b87a7a42f0b346a4147c5421a4",
    "InquiryData": {
        "Product": "Virtual Disk",
        "Revision": "DCS",
        "Serial": "65e604b87a7a42f0b346a4147c5421a4",
        "Vendor": "DataCore"
    },
    "Internal": false,
    "IsRollbackVirtualDisk": false,
    "IsServed": false,
    "IsSnapshotVirtualDisk": false,
    "ManualRecovery": false,
    "MirrorTrunkMappingEnabled": false,
    "NVMe": false,
    "Offline": false,
    "OtherHostIds": [],
    "PerformanceData": {
        "BytesAllocated": 0,
        "BytesOutOfAffinity": 0,
        "BytesOutOfSettings": 0,
        "BytesTogglingEncryption": 0,
        "CacheReadHitBytes": 0,
        "CacheReadHits": 0,
        "CacheReadMissBytes": 0,
        "CacheReadMisses": 0,
        "CacheWriteHitBytes": 0,
        "CacheWriteHits": 0,
        "CacheWriteMissBytes": 0,
        "CacheWriteMisses": 0,
        "CollectionTime": "/Date(1717237778074)/",
        "ConsistencyCheckPercentage": 0,
        "InitializationPercentage": 0,
        "MaxReadWriteTime": 0,
        "NullCounterMap": 0,
        "PercentAllocated": 0,
        "PercentBytesOutOfAffinity": 0,
        "PercentBytesOutOfSettings": 0,
        "PercentTogglingEncryption": 100,
        "ReplicationBytesSent": 0,
        "ReplicationBytesToSend": 0,
        "ReplicationTimeDifference": 0,
        "ReplicationTimeLag": 0,
        "TestModeProgressPercentage": 0,
        "TotalBytesMigrated": 0,
        "TotalBytesRead": 0,
        "TotalBytesTransferred": 0,
        "TotalBytesWritten": 0,
        "TotalOperations": 0,
        "TotalOperationsTime": 0,
        "TotalReads": 0,
        "TotalWrites": 0
    },
    "PersistentReserveEnabled": true,
    "PoolIds": [
        "FDD5406C-1664-467B-AACC-889775A2C32E:{576349e9-1de8-11ef-b801-000c2992e794}"
    ],
    "PreferredServer": "FDD5406C-1664-467B-AACC-889775A2C32E",
    "RecoveryPriority": 2,
    "RemovableMedia": false,
    "ResiliencyEnabled": false,
    "RollbackId": "",
    "ScsiDeviceId": "YAMNkKNl9gS8S5iZn3lZng==",
    "ScsiDeviceIdString": "60030D90A365F604BC4B98999F79599E",
    "SecondHostId": null,
    "SectorSize": {
        "Value": 512
    },
    "SequenceNumber": 93444,
    "Size": {
        "Value": 134217728
    },
    "SnapshotId": "",
    "SnapshotPoolId": null,
    "StaleDataEnabled": false,
    "StaleDataWeight": 0,
    "Status": "Healthy",
    "StatusLevel": 0,
    "StorageProfileId": "A122B0E3-7D32-4783-BDE4-619049C936C9",
    "SubType": 0,
    "TPThresholdsEnabled": false,
    "Type": 0,
    "VirtualDiskGroupId": null,
    "VirtualDiskReplicationData": null,
    "VirtualDiskRollbackData": {
        "Caption": "test-1",
        "ContinuousDataProtectionEnabled": false,
        "CreateRollbackValid": false,
        "DataProtectionPoolId": null,
        "DataProtectionServerId": null,
        "DisableDataProtectionValid": false,
        "EnableDataProtectionValid": true,
        "Id": "65e604b87a7a42f0b346a4147c5421a4",
        "RetentionPeriod": "/Date(1717237779964)/",
        "Rollbacks": [],
        "Status": "Healthy",
        "StatusLevel": 0,
        "StreamSize": {
            "Value": 0
        }
    },
    "VirtualDiskSnapshotData": null,
    "WitnessId": null,
    "WitnessOption": "Default",
    "WriteThrough": false
}"""

from cmk_addons.plugins.datacore_rest.lib import (
    parse_datacore_rest,
    discover_datacore_rest,
    convert_timestamp_to_epoch,
    calculate_percentages
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
    check_levels
)


def check_datacore_rest_virtualdisks(item: str, params, section) -> CheckResult:
    """Check state of DataCore Volumes"""

    data = section.get(item)
    if data is None:
        return

    perfdata = bool('PerformanceData' in data)

    # pprint.pprint(data)

    ##########
    # Status #
    ##########

    virtualdisk_status = data['Status']
    virtualdisk_is_offline = data['Offline']
    virtualdisk_is_disabled = data['Disabled']
    virtualdisk_is_served = data['IsServed']
    write_through = data['WriteThrough']

    if virtualdisk_status == "Healthy":
        yield Result(state=State.OK, summary=virtualdisk_status)
    else:
        if virtualdisk_status == "Path down":
            if params['virtual_disk_path_down'] == 'path_down_is_warning':
                yield Result(state=State.WARN, summary=virtualdisk_status)
            elif params['virtual_disk_path_down'] == 'path_down_is_ok':
                yield Result(state=State.OK, summary=virtualdisk_status)
        elif "In full recovery" in virtualdisk_status:
            yield Result(state=State.CRIT, summary=virtualdisk_status)
        elif "In log recovery" in virtualdisk_status:
            yield Result(state=State.WARN, summary=virtualdisk_status)
        elif virtualdisk_is_offline:
            message = "Virtual Disk is offline"
            yield Result(state=State.CRIT, summary=message)
        elif virtualdisk_is_disabled:
            message = "Virtual Disk is disabled"
            yield Result(state=State.WARN, summary=message)
        else:
            yield Result(state=State.CRIT, summary=virtualdisk_status)

    if not virtualdisk_is_served:
        message = "Virtual Disk is not served to any host"
        if params['expected_mapping'] == 'virtual_disk_is_not_served':
            yield Result(state=State.OK, summary=message)
        else:
            yield Result(state=State.WARN, summary=message)

    if write_through:
        message = "Virtual Disk is in write through mode"
        yield Result(state=State.WARN, summary=message)

    ########
    # Info #
    ########

    size = data['Size']['Value']
    recovery_priority = data['RecoveryPriority']
    sector_size = data['SectorSize']['Value']
    writethrough_enabled = data['WriteThrough']
    compression_enabled = data['CompressionEnabled']
    dedup_enabled = ['DeduplicationEnabled']
    encryption_enabled = data['EncryptionEnabled']
    sector_size_unit = "B" if sector_size == 512 else "K"

    details = f"Recovery Priority: {recovery_priority}\n" \
        f"Compression enabled: {compression_enabled}\n" \
        f"Dedup enabled: {dedup_enabled}\n" \
        f"Encryption Enabled: {encryption_enabled}\n" \
        f"Write Through: {writethrough_enabled}\n" \
        f"Sector Size: {sector_size}{sector_size_unit}"

    message = f"Size: {render.bytes(size)}"
    yield Result(state=State(0), summary=message, details=details)

    ####################
    # Performance Data #
    ####################

    if perfdata:
        raw_performance_counters = ["TotalReads", "TotalWrites", "TotalBytesRead", "TotalBytesWritten"]

        # get a reference to the value_store:
        value_store = get_value_store()

        current_collection_time_in_epoch = convert_timestamp_to_epoch(data['PerformanceData']['CollectionTime'])

        rate = {}

        for counter in raw_performance_counters:
            rate[counter] = round(get_rate(value_store, counter, current_collection_time_in_epoch, data['PerformanceData'][counter], raise_overflow=True))

        write_io_levels_upper = params['write_io_levels_upper']
        write_io_levels_lower = params['write_io_levels_lower']

        yield from (check_levels(
                rate['TotalWrites'],
                levels_upper=write_io_levels_upper,
                levels_lower=write_io_levels_lower,
                label='Write IO/s',
                notice_only=False,
            ))

        yield Metric("disk_read_ios", rate['TotalReads'])
        yield Metric("disk_write_ios", rate['TotalWrites'])
        yield Metric("disk_read_throughput", rate['TotalBytesRead'])
        yield Metric("disk_write_throughput", rate['TotalBytesWritten'])
        yield Metric("percent_allocated", data['PerformanceData']['PercentAllocated'])
        yield Metric("initialization_percentage", data['PerformanceData']['InitializationPercentage'])

        # Read / Write Ratio

        percent_read, percent_write = calculate_percentages(rate['TotalReads'], rate['TotalWrites'])
        message = f"Read/Write Ratio: {round(percent_read)}/{round(percent_write)}%"
        yield Result(state=State.OK, summary=message)


agent_section_datacore_rest_virtualdisks = AgentSection(
    name="datacore_rest_virtualdisks",
    parse_function=parse_datacore_rest,
    parsed_section_name="datacore_rest_virtualdisks",
)


check_plugin_datacore_rest_virtualdisks = CheckPlugin(
    name="datacore_rest_virtualdisks",
    service_name="SANsymphony Virtual Disk %s",
    sections=["datacore_rest_virtualdisks"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_virtualdisks,
    check_default_parameters={
        'virtual_disk_path_down': 'path_down_is_warning',
        'expected_mapping': 'virtual_disk_is_served',
        'write_io_levels_upper': ('no_levels', None),
        'write_io_levels_lower': ('no_levels', None),
        'upper_read_latency_levels': ('no_levels', None),
        'upper_write_latency_levels': ('no_levels', None),
    },
    check_ruleset_name='datacore_rest_virtualdisks',
)
