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
[
  {
    "OurGroup": true,
    "Alias": "Server Group",
    "Description": null,
    "State": 1,
    "SmtpSettings": null,
    "SyslogSettings": null,
    "MaxStaleDataWeight": 96,
    "StaleDataWeightStep": 32,
    "FeatureFlags": {
      "StaleDataMigration": true,
      "SnapshotGroupGranularCreation": true
    },
    "LicenseSettings": {
      "MaxServers": 2,
      "MaxPartnerGroups": 2147483647,
      "MaxMappedHosts": 2147483647,
      "BidirectionalReplication": 0,
      "FiberChannel": 0,
      "ThinProvisioning": 0,
      "Snapshot": 0,
      "iSCSI": 0,
      "StorageCapacity": {
        "Value": 1125899906842624
      },
      "LicensedBulkStorage": {
        "Value": 0
      },
      "BulkEnabled": 0,
      "RetentionTime": 9223372036854775807,
      "AutoTiering": 0,
      "HeatMaps": 0,
      "SharedStorage": 0,
      "PerformanceAnalysis": 1,
      "ResourceAuthorization": 1,
      "SequentialStorage": 0,
      "MaxBypassThreads": 0,
      "MaxPollerThreads": 0,
      "Mirroring": 0,
      "Witness": 0,
      "DataAtRestEncryption": 0,
      "ILDC": 1
    },
    "LicenseType": 1,
    "ContactData": {
      "ContactName": null,
      "PhoneNumber": null,
      "EmailAddress": null,
      "CompanyName": null
    },
    "StorageUsed": {
      "Value": 22548578304
    },
    "BulkStorageUsed": {
      "Value": 0
    },
    "MaxStorage": {
      "Value": 1125899906842624
    },
    "RecoverySpeed": 32,
    "ExistingProductKeys": [],
    "DataCoreStorageUsed": {
      "Value": 0
    },
    "SupportBundleRelayAddress": null,
    "MirrorTrunkMappingEnabled": false,
    "SelfHealingDelay": 480,
    "DefaultWitness": null,
    "DefaultWitnessOption": 0,
    "WitnessAllowed": false,
    "Telemetry": "Enabled",
    "DefaultKmipEndpoint": null,
    "CrashRecoveryCount": 0,
    "OutOfCompliance": false,
    "NextExpirationDate": "/Date(-62135596800000)/",
    "LicenseRemaining": 0,
    "GroupCdpMaxHistoryLogSizeGb": 10240,
    "GroupSeqMaxHistoryLogSizeGb": 10240,
    "SequenceNumber": 159086,
    "Id": "6bdeb641-2986-4b67-932d-2d9cd074c9ca",
    "Caption": "Server Group",
    "ExtendedCaption": "Server Group",
    "Internal": false
  }
]

"""

from cmk_addons.plugins.datacore_rest.lib import (
    discover_datacore_rest,
    parse_datacore_rest,
    convert_timestamp,
)

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
    render,
)


def check_datacore_rest_servergroups(item, section) -> CheckResult:
    """Check state of DataCore Servergroups"""

    data = section.get(item)
    if data is None:
        return

    # Infos

    group_capacity = data["LicenseSettings"]["StorageCapacity"]["Value"]
    group_capacity_used = data["StorageUsed"]["Value"]
    next_expiration_date = convert_timestamp(data["NextExpirationDate"])
    message = f"Group capacity: {render.bytes(group_capacity)}, Group capacity Used: {render.bytes(group_capacity_used)}, next expiration data: {next_expiration_date}"

    if data["SmtpSettings"] is not None:
        smtp_settings = f"SMTP Server: {data['SmtpSettings']['SmtpServer']}, E-Mail Address: {data['SmtpSettings']['EmailAddress']}"
    else:
        smtp_settings = "Not configured"

    if data["SyslogSettings"] is not None:
        syslog_settings = f"Syslog Server: {data['SyslogSettings']['SyslogServer']}, Log Level: {data['SyslogSettings']['SyslogLogLevel']}"
    else:
        syslog_settings = "Not configured"

    details = (
        f"CrashRecoveryCount: {data['CrashRecoveryCount']} \n"
        f"SMTP Settings: {smtp_settings}\n"
        f"Syslog Settings: {syslog_settings}\n"
        f"Max Servers: {data['LicenseSettings']['MaxServers']}\n"
        f"StorageCapacity: {render.bytes(data['LicenseSettings']['StorageCapacity']['Value'])}\n"
        f"Group Capacity:  {render.bytes(group_capacity)}\n"
        f"Group capacity Used: {render.bytes(group_capacity_used)}\n"
        f"LicenseRemaining: {data['LicenseRemaining']}\n"
        f"Max Storage: {render.bytes(data['MaxStorage']['Value'])}\n"
        f"Telemetry: {data['Telemetry']}\n"
        f"SupportBundleRelayAddress: {data['SupportBundleRelayAddress']}\n"
    )
    yield Result(state=State.OK, summary=message, details=details)


agent_section_datacore_rest_servergroups = AgentSection(
    name="datacore_rest_servergroups",
    parse_function=parse_datacore_rest,
    parsed_section_name="datacore_rest_servergroups",
)


check_plugin_datacore_rest_servergroups = CheckPlugin(
    name="datacore_rest_servergroups",
    service_name="SANsymphony ServerGroup %s",
    sections=["datacore_rest_servergroups"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_servergroups,
)
