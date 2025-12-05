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
    "Alias": "ssv1_fe2",
    "AluaId": 2092,
    "CapabilityInfo": {
        "ExtraCapability": {
            "Valid": false,
            "VmIdModes": 1
        },
        "MaxActiveICommands": 2048,
        "MaxActiveTCommands": 2048,
        "MaxSGSegments": 257,
        "MaxTransferSize": 1048576,
        "NeedPhysAddresses": true,
        "SoftWWNames": true,
        "SupportedConnections": [
            1,
            2,
            3,
            0
        ],
        "SupportedDataRates": [
            4,
            5,
            6,
            8,
            0
        ],
        "SupportedScsiModes": [
            1,
            2,
            3
        ]
    },
    "Caption": "ssv1_fe2",
    "Connected": true,
    "CurrentConfigInfo": {
        "ConnectionMode": 1,
        "DataRateMode": 5,
        "DisableMirrorPortWhileStopped": false,
        "DisablePortWhileStopped": true,
        "HardAssignedId": 4294967295,
        "HardIdMode": 2,
        "MaxActiveICommands": 2,
        "MaxActiveTCommands": 2046,
        "NodeName": {
            "Name": "51-40-2E-C0-18-1D-00-14"
        },
        "NumaNode": 1,
        "PortDownTimeout": 30,
        "PortName": {
            "Name": "51-40-2E-C0-18-1D-00-14"
        },
        "PrevAssignedId": 4294967295,
        "ScsiMode": 2,
        "SymbolicNodeName": "FCP Port 33",
        "SymbolicPortName": "",
        "UseSoftWWN": false,
        "VmIdMode": 0
    },
    "Description": null,
    "ExtendedCaption": "ssv1_fe2 on ssv1",
    "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
    "Id": "cbf72f07-5c2a-416b-8c1f-0bcb2117fc35",
    "IdInfo": {
        "ChipsetVersion": "2.A.0.E",
        "DriverName": "DataCore QLogic 2X",
        "DriverVersion": "15.0.1700.41043",
        "FirmwareVersion": "9.6.2.53461",
        "HBAProductName": "SN1610Q \u00e2\u20ac\u201c 2P Enhanced 32GFC Dual Port",
        "HBAVendorName": "QLogic",
        "OriginalNodeName": {
            "Name": "51-40-2E-C0-18-1D-00-14"
        },
        "OriginalPortName": {
            "Name": "51-40-2E-C0-18-1D-00-14"
        },
        "PCIInfo": {
            "Bus": 130,
            "DeviceId": 8833,
            "Function": 0,
            "InterruptLevel": 6,
            "Slot": 0,
            "SubVendorId": 0,
            "VendorId": 4215
        }
    },
    "Internal": false,
    "PerformanceData": {
        "BusyCount": 0,
        "CollectionTime": "/Date(1717881200383)/",
        "InitiatorBytesRead": 0,
        "InitiatorBytesTransferred": 0,
        "InitiatorBytesWritten": 0,
        "InitiatorMaxReadTime": 0,
        "InitiatorMaxWriteTime": 0,
        "InitiatorOperations": 0,
        "InitiatorReadTime": 0,
        "InitiatorReads": 0,
        "InitiatorWriteTime": 0,
        "InitiatorWrites": 0,
        "InvalidCrcCount": 0,
        "InvalidTransmissionWordCount": 0,
        "LinkFailureCount": 1,
        "LossOfSignalCount": 0,
        "LossOfSyncCount": 0,
        "NullCounterMap": 0,
        "PendingInitiatorCommands": 0,
        "PendingTargetCommands": 3,
        "PrimitiveSeqProtocolErrCount": 0,
        "TargetBytesRead": 17427869888512,
        "TargetBytesTransferred": 22609117241344,
        "TargetBytesWritten": 5181247352832,
        "TargetMaxIOTime": 15,
        "TargetMaxReadTime": 15,
        "TargetMaxWriteTime": 15,
        "TargetOperations": 410729703,
        "TargetReadTime": 103631907,
        "TargetReads": 260314860,
        "TargetTotalOperationsTime": 178224919,
        "TargetWriteTime": 74593012,
        "TargetWrites": 148179777,
        "TotalBytesRead": 17427869888512,
        "TotalBytesTransferred": 22609117241344,
        "TotalBytesWritten": 5181247352832,
        "TotalOperations": 410729703,
        "TotalPendingCommands": 3,
        "TotalReads": 260314860,
        "TotalWrites": 148179777
    },
    "PhysicalName": "51402EC0181D0014",
    "PortMode": 2,
    "PortName": "51-40-2E-C0-18-1D-00-14",
    "PortType": 2,
    "PresenceStatus": 1,
    "RoleCapability": 5,
    "SequenceNumber": 61576085,
    "ServerPortProperties": {
        "ConnectionMode": 1,
        "DataRateMode": 5,
        "DisableMirrorPortWhileStopped": false,
        "DisablePortWhileStopped": true,
        "HardAssignedId": 4294967295,
        "HardIdMode": 2,
        "MaxActiveICommands": 2,
        "MaxActiveTCommands": 2046,
        "NodeName": {
            "Name": "51-40-2E-C0-18-1D-00-14"
        },
        "PortDownTimeout": 30,
        "PortGroup": null,
        "PortName": {
            "Name": "51-40-2E-C0-18-1D-00-14"
        },
        "PrevAssignedId": 4294967295,
        "Role": 1,
        "ScsiMode": 2,
        "SymbolicNodeName": "FCP Port 33",
        "SymbolicPortName": "51-40-2E-C0-18-1D-00-14",
        "UseSoftWWN": false,
        "VmIdMode": 0
    },
    "StateInfo": {
        "Active": true,
        "Connection": 3,
        "DataRate": 5,
        "LinkErrors": {
            "InvalidCrcCount": 0,
            "InvalidTransmissionWordCount": 0,
            "LinkFailureCount": 1,
            "LossOfSignalCount": 0,
            "LossOfSyncCount": 0,
            "PrimitiveSeqProtocolErrCount": 0,
            "TotalErrorCount": 1
        },
        "LoopId": 4294967295,
        "PortId": 726272,
        "State": 5
    }
}}"""

from cmk_addons.plugins.datacore_rest.lib import (
    parse_datacore_rest,
    discover_datacore_rest,
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
    render,
    get_value_store,
    check_levels,
    get_rate,
)


def check_datacore_rest_ports(
    item: str, params: Mapping[str, Any], section: Mapping[str, Any]
) -> CheckResult:
    """Check state of DataCore Server Ports (e.g. iSCSI or Fibre Channel)."""
    data = section.get(item)
    if data is None:
        return

    perfdata = bool("PerformanceData" in data)

    ##########
    # Status #
    ##########

    # Connected
    if data["Connected"] is False:
        message = "Disconnected"
        if params["expected_port_connection_status"] == "connected":
            yield Result(state=State.WARN, summary=message)
        else:
            yield Result(state=State.OK, summary=message)
    else:
        message = "Connected"
        yield Result(state=State.OK, summary=message)

    # Link errors
    if "StateInfo" in data:
        for link_error_type in data["StateInfo"]["LinkErrors"]:
            # Skip these error types
            if link_error_type in ("TotalErrorCount", "PrimitiveSeqProtocolErrCount"):
                continue

            upper_levels = params[link_error_type]
            value = data["StateInfo"]["LinkErrors"][link_error_type]

            yield from (
                check_levels(
                    value,
                    levels_upper=upper_levels,
                    label=link_error_type,
                    notice_only=True,
                )
            )

        ########
        # Info #
        ########

        details = f"PortName: {data['PortName']}\n"

        if "IdInfo" in data:
            if "PCIInfo" in data["IdInfo"]:
                pci_info = (
                    f"Slot {data['IdInfo']['PCIInfo']['Slot']}, "
                    f"Bus {data['IdInfo']["PCIInfo"]['Bus']}, "
                    f"Device {data['IdInfo']["PCIInfo"]['DeviceId']}, "
                    f"Function {data['IdInfo']["PCIInfo"]['Function']}"
                )

                details += f"PCI: {pci_info}\n"

            if "FirmwareVersion" in data["IdInfo"]:
                details += (
                    f"Driver: {data['IdInfo']['DriverName']}\n"
                    f"Driver Version: {data['IdInfo']['DriverVersion']}\n"
                    f"Firmware Version: {data['IdInfo']['FirmwareVersion']}\n"
                    f"Type: {data['IdInfo']['HBAVendorName']} {data['IdInfo']['HBAProductName']}\n"
                )
        yield Result(state=State.OK, notice=message, details=details)

    ####################
    # Performance Data #
    ####################

    if perfdata:

        raw_performance_counters = [
            "TotalReads",
            "TotalWrites",
            "TotalBytesRead",
            "TotalBytesWritten",
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
        ]

        # StateInfo only present in FC port data
        if "StateInfo" in data:
            performance_metrics.extend(
                [
                    ("InvalidCrcCount", data["PerformanceData"]["InvalidCrcCount"]),
                    (
                        "InvalidTransmissionWordCount",
                        data["StateInfo"]["LinkErrors"]["InvalidTransmissionWordCount"],
                    ),
                    (
                        "LinkFailureCount",
                        data["StateInfo"]["LinkErrors"]["LinkFailureCount"],
                    ),
                    (
                        "LossOfSignalCount",
                        data["StateInfo"]["LinkErrors"]["LossOfSignalCount"],
                    ),
                    (
                        "LossOfSyncCount",
                        data["StateInfo"]["LinkErrors"]["LossOfSyncCount"],
                    ),
                ]
            )
        for description, metric in performance_metrics:
            yield Metric(description, metric)

        message = f"Read: {render.iobandwidth(rate['TotalBytesRead'])}, Write: {render.iobandwidth(rate['TotalBytesWritten'])}, Read IO/s: {rate['TotalReads']}/s, Write IO/s: {rate['TotalWrites']}/s"
        yield Result(state=State.OK, summary=message)


agent_section_datacore_rest_ports = AgentSection(
    name="datacore_rest_ports",
    parse_function=parse_datacore_rest,
    parsed_section_name="datacore_rest_ports",
)


check_plugin_datacore_rest_ports = CheckPlugin(
    name="datacore_rest_ports",
    service_name="SANsymphony Port %s",
    sections=["datacore_rest_ports"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_ports,
    check_default_parameters={
        "InvalidCrcCount": ("fixed", (1, 2)),
        "InvalidTransmissionWordCount": ("fixed", (1, 2)),
        "LinkFailureCount": ("fixed", (1, 2)),
        "LossOfSignalCount": ("fixed", (1, 2)),
        "LossOfSyncCount": ("fixed", (1, 2)),
        "expected_port_connection_status": "connected",
    },
    check_ruleset_name="datacore_rest_ports",
)
