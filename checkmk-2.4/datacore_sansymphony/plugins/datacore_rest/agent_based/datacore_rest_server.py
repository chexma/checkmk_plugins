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
    "AluaGroupId": 2,
    "AvailableSystemMemory": {
        "Value": 37157748736
    },
    "BackupStorageFolder": "C:\\Install\\DatacoreBackup",
    "BuildType": "Release",
    "BulkStorageUsed": {
        "Value": 0
    },
    "CacheSize": {
        "Value": 0
    },
    "CacheState": 2,
    "Caption": "ssv1",
    "CdpMaxHistoryLogSizeGb": 0,
    "ConfigurationInfo": {
        "SequenceNumber": 39588,
        "TimeStamp": "/Date(1717829090942+0200)/"
    },
    "DataCoreBulkStorageUsed": {
        "Value": 0
    },
    "DataCoreStorageUsed": {
        "Value": 0
    },
    "DeduplicationPoolId": null,
    "DefaultSnapshotPoolId": null,
    "Description": "",
    "DiagnosticMode": 1,
    "ExtendedCaption": "ssv1 in RZ",
    "GroupId": "02a51922-4d06-4f8c-9dd3-eab194885e39",
    "HostName": "ssv1.akf.lan",
    "HypervisorHostId": null,
    "Id": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
    "IldcConfigurationData": null,
    "InUseCacheSize": {
        "Value": 87525687296
    },
    "InstallPath": "C:\\Program Files\\DataCore\\SANsymphony",
    "Internal": false,
    "IpAddresses": [
        "192.168.1.5"
    ],
    "IsAzureVirtualMachine": false,
    "IsLicensed": true,
    "IsPayGo": false,
    "IsTcLoaded": false,
    "IsVirtualMachine": false,
    "KmipEndpointId": null,
    "LicenseExceeded": false,
    "LicenseNumber": 2482328029411222676,
    "LicenseRemaining": 330597077295754,
    "LicenseSettings": {
        "AutoTiering": 1,
        "BidirectionalReplication": 1,
        "BulkEnabled": 0,
        "DataAtRestEncryption": 1,
        "FiberChannel": 1,
        "HeatMaps": 1,
        "ILDC": 1,
        "LicensedBulkStorage": {
            "Value": 0
        },
        "MaxBypassThreads": 256,
        "MaxMappedHosts": 2147483647,
        "MaxPartnerGroups": 99,
        "MaxPollerThreads": 256,
        "MaxServers": 2147483647,
        "Mirroring": 1,
        "PerformanceAnalysis": 2,
        "ResourceAuthorization": 2,
        "RetentionTime": 12096000000000,
        "SequentialStorage": 1,
        "SharedStorage": 1,
        "Snapshot": 1,
        "StorageCapacity": {
            "Value": 18446744073709551615
        },
        "ThinProvisioning": 1,
        "Witness": 1,
        "iSCSI": 1
    },
    "LicensedCapacityLimit": {
        "Value": 0
    },
    "LogStatus": 0,
    "LogStorePoolId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF:{4d235c44-e5c6-11ed-b80b-98f2b3e70bc1}",
    "MaxCacheSize": {
        "Value": 123419492352
    },
    "MaxPollerThreadsConfig": 12,
    "MinCacheSize": {
        "Value": 134217728
    },
    "MpioCapable": true,
    "NextExpirationDate": "/Date(1750888800000+0200)/",
    "OsVersion": "Microsoft Windows Server 2022 Standard, Build 20348",
    "OutOfCompliance": false,
    "PerformanceData": {
        "CacheReadHitBytes": 27019965585920,
        "CacheReadHits": 329937230,
        "CacheReadMissBytes": 9262837390848,
        "CacheReadMisses": 161154389,
        "CacheSize": 87525687296,
        "CacheWriteHitBytes": 19159626193920,
        "CacheWriteHits": 471643976,
        "CacheWriteMissBytes": 653742945280,
        "CacheWriteMisses": 13213613,
        "CollectionTime": "/Date(1717881200383)/",
        "CompressionRatioPercentage": 0,
        "DeduplicationPoolFreeSpace": 0,
        "DeduplicationPoolL2ARCTotalSpace": 0,
        "DeduplicationPoolL2ARCUsedSpace": 0,
        "DeduplicationPoolPercentFreeSpace": 100,
        "DeduplicationPoolSpecialMirrorTotalSpace": 0,
        "DeduplicationPoolSpecialMirrorUsedSpace": 0,
        "DeduplicationPoolTotalSpace": 0,
        "DeduplicationPoolUsedSpace": 0,
        "DeduplicationRatioPercentage": 0,
        "ExpectedDeduplicationPoolUsedSpace": 0,
        "FreeCache": 81135431680,
        "FrontEndTargetBytesTransfered": 45246054651904,
        "FrontEndTargetMaxIOTime": 31,
        "FrontEndTargetOperations": 821418242,
        "FrontEndTargetTotalOperationsTime": 356374436,
        "InitiatorBytesRead": 7656023040,
        "InitiatorBytesTransferred": 10523939798016,
        "InitiatorBytesWritten": 10516283774976,
        "InitiatorOperations": 285399763,
        "InitiatorReads": 934723,
        "InitiatorWrites": 281843789,
        "MaxReplicationTimeDifference": 0,
        "MirrorTargetBytesTransfered": 9774996794368,
        "MirrorTargetMaxIOTime": 15,
        "MirrorTargetOperations": 212477389,
        "MirrorTargetTotalOperationsTime": 27880702,
        "NullCounterMap": 0,
        "PhysicalDiskBytesTransfered": 0,
        "PhysicalDiskMaxIOTime": 0,
        "PhysicalDiskOperations": 0,
        "PhysicalDiskTotalOperationsTime": 0,
        "PollerDedicatedCPUs": 2,
        "PollerLoad": 10,
        "PollerProductiveCount": 3287383359,
        "PollerUnproductiveCount": 7401801286622,
        "PoolBytesTransfered": 45460908090368,
        "PoolMaxIOTime": 15,
        "PoolOperations": 519924203,
        "PoolTotalOperationsTime": 187049985,
        "ReplicationBufferPercentFreeSpace": 100,
        "ReplicationBytesToSend": 0,
        "SupportBytesSent": 0,
        "SupportPercentCollected": 0,
        "SupportPercentTransferred": 0,
        "SupportRemainingBytesToSend": 0,
        "TargetBytesRead": 34886125642240,
        "TargetBytesTransferred": 55021051446272,
        "TargetBytesWritten": 20134925804032,
        "TargetMaxIOTime": 31,
        "TargetOperations": 1033895631,
        "TargetReads": 520677431,
        "TargetTotalOperationsTime": 384255138,
        "TargetWrites": 505937212,
        "TotalBytesMigrated": 2650531692544,
        "TotalBytesRead": 34893781665280,
        "TotalBytesTransferred": 65544991244288,
        "TotalBytesWritten": 30651209579008,
        "TotalOperations": 1309393155,
        "TotalReads": 521612154,
        "TotalWrites": 787781001
    },
    "PhysicalDisks": [
        {
            "Alias": "ssv1-hb51-vol04",
            "AllServers": [
                "4B273A2A-1FE0-41D0-B993-6F7B35672AAF"
            ],
            "BusType": 6,
            "Caption": "ssv1-hb51-vol04",
            "CompressionSupported": false,
            "DeduplicationSupported": false,
            "DiskIndex": 44,
            "DiskStatus": 1,
            "DvaPoolDiskId": null,
            "ExtendedCaption": "ssv1-hb51-vol04 on ssv1",
            "FreeSpace": {
                "Value": 0
            },
            "HardwareEncryptionSupported": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "Id": "{0b014904-9a06-4856-944c-51c78b55ee19}",
            "InUse": true,
            "InquiryData": {
                "Product": "ETERNUS_AHB",
                "Revision": "0874",
                "Serial": "042249000046    ",
                "Vendor": "FUJITSU"
            },
            "Internal": false,
            "IsBootDisk": false,
            "IsDataCoreDisk": false,
            "IsSolidState": true,
            "Partitioned": true,
            "PoolMemberId": "5399554d-4af5-4f92-a056-c64fb1ce5098",
            "PresenceStatus": 1,
            "Protected": false,
            "ScsiPath": {
                "Bus": 0,
                "LUN": 4,
                "Port": 9,
                "Target": 2
            },
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 61949531,
            "SharedPhysicalDiskId": null,
            "Size": {
                "Value": 65970697666560
            },
            "SmartStatus": 0,
            "Status": "On-line",
            "StatusLevel": 0,
            "SystemName": "",
            "Type": 4,
            "UniqueIdentifier": "naa.6d039ea000a42dce00000207644b1f73",
            "Usage": "In pool \"SSV1-HB51\""
        },
        {
            "Alias": "ssv1-hb51-vol03",
            "AllServers": [
                "4B273A2A-1FE0-41D0-B993-6F7B35672AAF"
            ],
            "BusType": 6,
            "Caption": "ssv1-hb51-vol03",
            "CompressionSupported": false,
            "DeduplicationSupported": false,
            "DiskIndex": 43,
            "DiskStatus": 1,
            "DvaPoolDiskId": null,
            "ExtendedCaption": "ssv1-hb51-vol03 on ssv1",
            "FreeSpace": {
                "Value": 0
            },
            "HardwareEncryptionSupported": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "Id": "{9160d4fa-1e12-48e0-857f-0568aef7ea98}",
            "InUse": true,
            "InquiryData": {
                "Product": "ETERNUS_AHB",
                "Revision": "0874",
                "Serial": "042301004140    ",
                "Vendor": "FUJITSU"
            },
            "Internal": false,
            "IsBootDisk": false,
            "IsDataCoreDisk": false,
            "IsSolidState": true,
            "Partitioned": true,
            "PoolMemberId": "14d3e03f-20f2-448d-aad6-4502f66ef706",
            "PresenceStatus": 1,
            "Protected": false,
            "ScsiPath": {
                "Bus": 0,
                "LUN": 3,
                "Port": 9,
                "Target": 3
            },
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 61957467,
            "SharedPhysicalDiskId": null,
            "Size": {
                "Value": 65970697666560
            },
            "SmartStatus": 0,
            "Status": "On-line",
            "StatusLevel": 0,
            "SystemName": "",
            "Type": 4,
            "UniqueIdentifier": "naa.6d039ea000a5edc200000201644b1f73",
            "Usage": "In pool \"SSV1-HB51\""
        },
        {
            "Alias": "ssv1-hb51-vol02",
            "AllServers": [
                "4B273A2A-1FE0-41D0-B993-6F7B35672AAF"
            ],
            "BusType": 6,
            "Caption": "ssv1-hb51-vol02",
            "CompressionSupported": false,
            "DeduplicationSupported": false,
            "DiskIndex": 42,
            "DiskStatus": 1,
            "DvaPoolDiskId": null,
            "ExtendedCaption": "ssv1-hb51-vol02 on ssv1",
            "FreeSpace": {
                "Value": 0
            },
            "HardwareEncryptionSupported": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "Id": "{f69c4f3a-9ee8-44cf-9652-0f86b7f8fac1}",
            "InUse": true,
            "InquiryData": {
                "Product": "ETERNUS_AHB",
                "Revision": "0874",
                "Serial": "042249000046    ",
                "Vendor": "FUJITSU"
            },
            "Internal": false,
            "IsBootDisk": false,
            "IsDataCoreDisk": false,
            "IsSolidState": true,
            "Partitioned": true,
            "PoolMemberId": "e60d31b0-e8d3-4cff-b448-181f261fff42",
            "PresenceStatus": 1,
            "Protected": false,
            "ScsiPath": {
                "Bus": 0,
                "LUN": 2,
                "Port": 9,
                "Target": 2
            },
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 61959147,
            "SharedPhysicalDiskId": null,
            "Size": {
                "Value": 65970697666560
            },
            "SmartStatus": 0,
            "Status": "On-line",
            "StatusLevel": 0,
            "SystemName": "",
            "Type": 4,
            "UniqueIdentifier": "naa.6d039ea000a42dce00000206644b1f4d",
            "Usage": "In pool \"SSV1-HB51\""
        },
        {
            "Alias": "ssv1-hb51-vol01",
            "AllServers": [
                "4B273A2A-1FE0-41D0-B993-6F7B35672AAF"
            ],
            "BusType": 6,
            "Caption": "ssv1-hb51-vol01",
            "CompressionSupported": false,
            "DeduplicationSupported": false,
            "DiskIndex": 41,
            "DiskStatus": 1,
            "DvaPoolDiskId": null,
            "ExtendedCaption": "ssv1-hb51-vol01 on ssv1",
            "FreeSpace": {
                "Value": 0
            },
            "HardwareEncryptionSupported": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "Id": "{debe8152-474c-4c2b-aa35-126e3f94351f}",
            "InUse": true,
            "InquiryData": {
                "Product": "ETERNUS_AHB",
                "Revision": "0874",
                "Serial": "042301004140    ",
                "Vendor": "FUJITSU"
            },
            "Internal": false,
            "IsBootDisk": false,
            "IsDataCoreDisk": false,
            "IsSolidState": true,
            "Partitioned": true,
            "PoolMemberId": "b3b2466d-42ce-4f0c-afb5-5dfd8a577525",
            "PresenceStatus": 1,
            "Protected": false,
            "ScsiPath": {
                "Bus": 0,
                "LUN": 1,
                "Port": 9,
                "Target": 3
            },
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 61961070,
            "SharedPhysicalDiskId": null,
            "Size": {
                "Value": 65970697666560
            },
            "SmartStatus": 0,
            "Status": "On-line",
            "StatusLevel": 0,
            "SystemName": "",
            "Type": 4,
            "UniqueIdentifier": "naa.6d039ea000a5edc2000001ff644b1f42",
            "Usage": "In pool \"SSV1-HB51\""
        },
        {
            "Alias": "SSV1-VOL-DX-AR-SAS-02",
            "AllServers": [
                "4B273A2A-1FE0-41D0-B993-6F7B35672AAF"
            ],
            "BusType": 6,
            "Caption": "SSV1-VOL-DX-AR-SAS-02",
            "CompressionSupported": false,
            "DeduplicationSupported": false,
            "DiskIndex": 40,
            "DiskStatus": 1,
            "DvaPoolDiskId": null,
            "ExtendedCaption": "SSV1-VOL-DX-AR-SAS-02 on ssv1",
            "FreeSpace": {
                "Value": 0
            },
            "HardwareEncryptionSupported": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "Id": "{3a12056f-22cf-40ba-a058-e4b4f7629ef8}",
            "InUse": true,
            "InquiryData": {
                "Product": "ETERNUS_DXL",
                "Revision": "0000",
                "Serial": "  32117D",
                "Vendor": "FUJITSU"
            },
            "Internal": false,
            "IsBootDisk": false,
            "IsDataCoreDisk": false,
            "IsSolidState": false,
            "Partitioned": true,
            "PoolMemberId": "a3f44027-a410-4272-aff5-3fd4e7fa76b8",
            "PresenceStatus": 1,
            "Protected": false,
            "ScsiPath": {
                "Bus": 0,
                "LUN": 1,
                "Port": 9,
                "Target": 1
            },
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 57449068,
            "SharedPhysicalDiskId": null,
            "Size": {
                "Value": 39148626903040
            },
            "SmartStatus": 0,
            "Status": "On-line",
            "StatusLevel": 0,
            "SystemName": "",
            "Type": 4,
            "UniqueIdentifier": "naa.600000e00d320000003245f400010000",
            "Usage": "In pool \"SSV1-DX-200-AR\""
        },
        {
            "Alias": "SSV1-VOL-DX-AR-SAS-01",
            "AllServers": [
                "4B273A2A-1FE0-41D0-B993-6F7B35672AAF"
            ],
            "BusType": 6,
            "Caption": "SSV1-VOL-DX-AR-SAS-01",
            "CompressionSupported": false,
            "DeduplicationSupported": false,
            "DiskIndex": 39,
            "DiskStatus": 1,
            "DvaPoolDiskId": null,
            "ExtendedCaption": "SSV1-VOL-DX-AR-SAS-01 on ssv1",
            "FreeSpace": {
                "Value": 0
            },
            "HardwareEncryptionSupported": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "Id": "{72f84738-f5df-4243-8e6c-f58bfcbc372c}",
            "InUse": true,
            "InquiryData": {
                "Product": "ETERNUS_DXL",
                "Revision": "0000",
                "Serial": "  32117D",
                "Vendor": "FUJITSU"
            },
            "Internal": false,
            "IsBootDisk": false,
            "IsDataCoreDisk": false,
            "IsSolidState": false,
            "Partitioned": true,
            "PoolMemberId": "d7cefc20-8248-4b7a-b4ed-d34da505a6a6",
            "PresenceStatus": 1,
            "Protected": false,
            "ScsiPath": {
                "Bus": 0,
                "LUN": 0,
                "Port": 9,
                "Target": 0
            },
            "SectorSize": {
                "Value": 512
            },
            "SequenceNumber": 57476494,
            "SharedPhysicalDiskId": null,
            "Size": {
                "Value": 39148626903040
            },
            "SmartStatus": 0,
            "Status": "On-line",
            "StatusLevel": 0,
            "SystemName": "",
            "Type": 4,
            "UniqueIdentifier": "naa.600000e00d320000003245f400000000",
            "Usage": "In pool \"SSV1-DX-200-AR\""
        }
    ],
    "PowerState": 2,
    "ProcessorInfo": {
        "CpuArchitecture": 9,
        "NumberCores": 32,
        "NumberPhysicalCores": 32,
        "ProcessorName": "AMD EPYC 9174F 16-Core Processor               "
    },
    "ProductBuild": "15.0.1701.43466",
    "ProductName": "DataCore SANsymphony",
    "ProductType": "Standard",
    "ProductVersion": "10.0 PSP 17, Update 1",
    "RegionNodeId": "ExecutiveNode:4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
    "ReplicationBufferFolder": "",
    "SeqMaxHistoryLogSizeGb": 0,
    "SequenceNumber": 38233159,
    "ServerPorts": [
        {
            "Alias": "Server iSCSI Port 1",
            "AluaId": 2093,
            "BackEndRoleInUse": false,
            "Caption": "Server iSCSI Port 1",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "Server iSCSI Port 1 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "7ff3022c-ac6e-43e6-bfa5-3a39874684e4",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "MAC:00-62-0B-4D-FD-FA",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 3,
            "PortWwn": null,
            "PresenceStatus": 2,
            "RoleCapability": 5,
            "Roles": "None",
            "SequenceNumber": 38232346,
            "ServerPortProperties": {
                "Active": false,
                "Alias": null,
                "Authentication": 0,
                "AutoLoginMode": 0,
                "DisablePortWhileStopped": false,
                "Discovery": {
                    "SLPConfig": {
                        "ServerAgentMode": 0,
                        "UserAgentMode": 0
                    },
                    "TargetAutoDiscovery": 0,
                    "iSNSConfig": {
                        "Mode": 0,
                        "iSNSServerAddress": {
                            "Address": null,
                            "AddressType": 0,
                            "DomainName": null,
                            "TcpPort": 0
                        }
                    }
                },
                "ISID": 0,
                "IScsiPortalsConfig": null,
                "InstanceName": null,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": null,
                "PortGroup": null,
                "RecoveryLevel": 0,
                "Role": 0,
                "ScsiMode": 0,
                "SessionParams": {
                    "DataPDUInOrder": 0,
                    "DataSequenceInOrder": 0,
                    "DefaultTime2Retain": 0,
                    "DefaultTime2Wait": 0,
                    "FirstBurstLength": 0,
                    "ImmediateData": 0,
                    "InitialR2T": 0,
                    "MaxBurstLength": 0,
                    "MaxConnections": 0,
                    "MaxOutstandingR2T": 0
                },
                "TPGT": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "Server iSCSI Port 2",
            "AluaId": 2088,
            "BackEndRoleInUse": false,
            "Caption": "Server iSCSI Port 2",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "Server iSCSI Port 2 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "f20000ee-41af-4fb7-bede-b97d7f94e5e9",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "MAC:00-62-0B-4D-FD-F8",
            "PortIpAddress": "192.168.1.10",
            "PortIqn": "iqn.2000-08.com.datacore:ssv1-2",
            "PortMode": 2,
            "PortName": null,
            "PortType": 3,
            "PortWwn": null,
            "PresenceStatus": 1,
            "RoleCapability": 5,
            "Roles": "None",
            "SequenceNumber": 38232341,
            "ServerPortProperties": {
                "Active": true,
                "Alias": "",
                "Authentication": 0,
                "AutoLoginMode": 0,
                "DisablePortWhileStopped": true,
                "Discovery": {
                    "SLPConfig": {
                        "ServerAgentMode": 0,
                        "UserAgentMode": 0
                    },
                    "TargetAutoDiscovery": 0,
                    "iSNSConfig": {
                        "Mode": 2,
                        "iSNSServerAddress": {
                            "Address": {
                                "Address": "::"
                            },
                            "AddressType": 0,
                            "DomainName": "",
                            "TcpPort": 3205
                        }
                    }
                },
                "ISID": 140737488355328,
                "IScsiPortalsConfig": [
                    {
                        "Address": {
                            "Address": "::"
                        },
                        "ConnParams": {
                            "DataDigestMode": 0,
                            "HeaderDigestMode": 0,
                            "MaxRcvDataSegLen": 0
                        },
                        "DefaultGateway": {
                            "Address": "0.0.0.0"
                        },
                        "DhcpMode": 0,
                        "Dns": {
                            "Address": "0.0.0.0"
                        },
                        "Mtu": 0,
                        "SubnetMask": {
                            "Address": "0.0.0.0"
                        },
                        "TcpPort": 3260
                    }
                ],
                "InstanceName": "MAC:00-62-0B-4D-FD-F8",
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 256,
                "NodeName": "iqn.2000-08.com.datacore:ssv1-2",
                "PortGroup": null,
                "RecoveryLevel": 0,
                "Role": 0,
                "ScsiMode": 0,
                "SessionParams": {
                    "DataPDUInOrder": 0,
                    "DataSequenceInOrder": 0,
                    "DefaultTime2Retain": 0,
                    "DefaultTime2Wait": 0,
                    "FirstBurstLength": 0,
                    "ImmediateData": 0,
                    "InitialR2T": 0,
                    "MaxBurstLength": 0,
                    "MaxConnections": 0,
                    "MaxOutstandingR2T": 0
                },
                "TPGT": 1
            },
            "Status": "Ready",
            "StatusLevel": 0
        },
        {
            "Alias": "ssv1_fe2",
            "AluaId": 2092,
            "BackEndRoleInUse": false,
            "Caption": "ssv1_fe2",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "ssv1_fe2 on ssv1",
            "FrontEndRoleInUse": true,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [
                "de4a43f4c1ce4de79132bb3f8e8a3911",
                "6543950ca7674c12a7b00cbfe9c09356",
                "00857a80a2a44d53823d43cb94cd1720",
                "f4c0850bed2f49f39d3740a9d3ecb26a",
                "049b2cbe873441db9e610132791b954c",
                "715449b3bd12438cb15a07d9c253fb03",
                "7d78affb476f4be0b2ab9f3ebe5539f3",
                "d4b9a756d21f4fa4b7a89bc24de6c129",
                "eab394817d0243fea383dc62cf1cc42e",
                "ec49786adfd5471a96ba1261e55bd316",
                "5293161355e84b19b2dc258b50876f5c",
                "7c72f4ac77104b9984e79e9d382f53a7",
                "617db7922f3240f7b377bff57bf3a064",
                "333de0e24aac468e9ec9a6525d4233d8",
                "22ffa64f57dd44efaae801691867dcc9",
                "d2af3c4ab078439ab5fe49f16c72b341",
                "ff4bfbae2c564e23a659e43a9c718e36",
                "edbfad0b4f3e435f9a63e0cd41475ac4"
            ],
            "Id": "cbf72f07-5c2a-416b-8c1f-0bcb2117fc35",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC0181D0014",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "51-40-2E-C0-18-1D-00-14",
            "PresenceStatus": 1,
            "RoleCapability": 5,
            "Roles": "FE",
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
            "Status": "Loop/Link up",
            "StatusLevel": 0
        },
        {
            "Alias": "ssv1_mr2",
            "AluaId": 2091,
            "BackEndRoleInUse": false,
            "Caption": "ssv1_mr2",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "ssv1_mr2 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "610a6e0f-3a30-4087-a9f9-ec3c00a70544",
            "Internal": false,
            "MirrorRoleInUse": true,
            "PhysicalName": "51402EC0181D0286",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 3,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "51-40-2E-C0-18-1D-02-86",
            "PresenceStatus": 1,
            "RoleCapability": 7,
            "Roles": "MR",
            "SequenceNumber": 61576084,
            "ServerPortProperties": {
                "ConnectionMode": 1,
                "DataRateMode": 5,
                "DisableMirrorPortWhileStopped": true,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 4294967295,
                "HardIdMode": 2,
                "MaxActiveICommands": 1024,
                "MaxActiveTCommands": 1024,
                "NodeName": {
                    "Name": "51-40-2E-C0-18-1D-02-86"
                },
                "PortDownTimeout": 30,
                "PortGroup": null,
                "PortName": {
                    "Name": "51-40-2E-C0-18-1D-02-86"
                },
                "PrevAssignedId": 4294967295,
                "Role": 4,
                "ScsiMode": 3,
                "SymbolicNodeName": "FCP Port 32",
                "SymbolicPortName": "",
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Loop/Link up",
            "StatusLevel": 0
        },
        {
            "Alias": "ssv1_mr1",
            "AluaId": 2090,
            "BackEndRoleInUse": false,
            "Caption": "ssv1_mr1",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "ssv1_mr1 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "4ad2206f-1a05-4075-9902-123cd225c17c",
            "Internal": false,
            "MirrorRoleInUse": true,
            "PhysicalName": "51402EC0181D02AE",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 3,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "51-40-2E-C0-18-1D-02-AE",
            "PresenceStatus": 1,
            "RoleCapability": 7,
            "Roles": "MR",
            "SequenceNumber": 61576083,
            "ServerPortProperties": {
                "ConnectionMode": 1,
                "DataRateMode": 5,
                "DisableMirrorPortWhileStopped": true,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 4294967295,
                "HardIdMode": 2,
                "MaxActiveICommands": 1024,
                "MaxActiveTCommands": 1024,
                "NodeName": {
                    "Name": "51-40-2E-C0-18-1D-02-AE"
                },
                "PortDownTimeout": 30,
                "PortGroup": null,
                "PortName": {
                    "Name": "51-40-2E-C0-18-1D-02-AE"
                },
                "PrevAssignedId": 4294967295,
                "Role": 4,
                "ScsiMode": 3,
                "SymbolicNodeName": "FCP Port 31",
                "SymbolicPortName": "",
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Loop/Link up",
            "StatusLevel": 0
        },
        {
            "Alias": "ssv1_fe1",
            "AluaId": 2089,
            "BackEndRoleInUse": false,
            "Caption": "ssv1_fe1",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "ssv1_fe1 on ssv1",
            "FrontEndRoleInUse": true,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [
                "715449b3bd12438cb15a07d9c253fb03",
                "d4b9a756d21f4fa4b7a89bc24de6c129",
                "eab394817d0243fea383dc62cf1cc42e",
                "ec49786adfd5471a96ba1261e55bd316",
                "edbfad0b4f3e435f9a63e0cd41475ac4",
                "ff4bfbae2c564e23a659e43a9c718e36",
                "d2af3c4ab078439ab5fe49f16c72b341",
                "22ffa64f57dd44efaae801691867dcc9",
                "333de0e24aac468e9ec9a6525d4233d8",
                "617db7922f3240f7b377bff57bf3a064",
                "7c72f4ac77104b9984e79e9d382f53a7",
                "f4c0850bed2f49f39d3740a9d3ecb26a",
                "00857a80a2a44d53823d43cb94cd1720",
                "7d78affb476f4be0b2ab9f3ebe5539f3",
                "5293161355e84b19b2dc258b50876f5c",
                "049b2cbe873441db9e610132791b954c",
                "de4a43f4c1ce4de79132bb3f8e8a3911",
                "6543950ca7674c12a7b00cbfe9c09356"
            ],
            "Id": "0abc924e-eebc-4e85-b506-ba4f5ea81376",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC0181D02AC",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "51-40-2E-C0-18-1D-02-AC",
            "PresenceStatus": 1,
            "RoleCapability": 5,
            "Roles": "FE",
            "SequenceNumber": 61576082,
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
                    "Name": "51-40-2E-C0-18-1D-02-AC"
                },
                "PortDownTimeout": 30,
                "PortGroup": null,
                "PortName": {
                    "Name": "51-40-2E-C0-18-1D-02-AC"
                },
                "PrevAssignedId": 4294967295,
                "Role": 1,
                "ScsiMode": 2,
                "SymbolicNodeName": "FCP Port 30",
                "SymbolicPortName": "51-40-2E-C0-18-1D-02-AC",
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Loop/Link up",
            "StatusLevel": 0
        },
        {
            "Alias": "reserve_4",
            "AluaId": 2083,
            "BackEndRoleInUse": false,
            "Caption": "reserve_4",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "reserve_4 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "56aabf2b-c713-473c-ae2d-a663c52a0b34",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC001BB775E",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "00-00-00-00-00-00-00-00",
            "PresenceStatus": 2,
            "RoleCapability": 5,
            "Roles": "None",
            "SequenceNumber": 38232340,
            "ServerPortProperties": {
                "ConnectionMode": 0,
                "DataRateMode": 0,
                "DisableMirrorPortWhileStopped": false,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 0,
                "HardIdMode": 0,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PortDownTimeout": 0,
                "PortGroup": null,
                "PortName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PrevAssignedId": 0,
                "Role": 0,
                "ScsiMode": 0,
                "SymbolicNodeName": null,
                "SymbolicPortName": null,
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "reserve_2",
            "AluaId": 2082,
            "BackEndRoleInUse": false,
            "Caption": "reserve_2",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "reserve_2 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "541a7f33-76c2-4cde-9eb6-e5c81f85ea24",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC001BB775C",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "00-00-00-00-00-00-00-00",
            "PresenceStatus": 2,
            "RoleCapability": 5,
            "Roles": "None",
            "SequenceNumber": 38232339,
            "ServerPortProperties": {
                "ConnectionMode": 0,
                "DataRateMode": 0,
                "DisableMirrorPortWhileStopped": false,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 0,
                "HardIdMode": 0,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PortDownTimeout": 0,
                "PortGroup": null,
                "PortName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PrevAssignedId": 0,
                "Role": 0,
                "ScsiMode": 0,
                "SymbolicNodeName": null,
                "SymbolicPortName": null,
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "ssv1_fe2_old",
            "AluaId": 2081,
            "BackEndRoleInUse": false,
            "Caption": "ssv1_fe2_old",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "ssv1_fe2_old on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "9a5e138f-79d6-4b2d-b373-0b8872444dfd",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC000F470A8",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "00-00-00-00-00-00-00-00",
            "PresenceStatus": 2,
            "RoleCapability": 5,
            "Roles": "FE",
            "SequenceNumber": 38232338,
            "ServerPortProperties": {
                "ConnectionMode": 0,
                "DataRateMode": 0,
                "DisableMirrorPortWhileStopped": false,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 0,
                "HardIdMode": 0,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PortDownTimeout": 0,
                "PortGroup": null,
                "PortName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PrevAssignedId": 0,
                "Role": 1,
                "ScsiMode": 0,
                "SymbolicNodeName": null,
                "SymbolicPortName": null,
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "reserve_3",
            "AluaId": 2080,
            "BackEndRoleInUse": false,
            "Caption": "reserve_3",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "reserve_3 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "f37d6ebf-f9c8-4f8c-b7c0-834e58021ff5",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC001BB775A",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "00-00-00-00-00-00-00-00",
            "PresenceStatus": 2,
            "RoleCapability": 5,
            "Roles": "None",
            "SequenceNumber": 38232337,
            "ServerPortProperties": {
                "ConnectionMode": 0,
                "DataRateMode": 0,
                "DisableMirrorPortWhileStopped": false,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 0,
                "HardIdMode": 0,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PortDownTimeout": 0,
                "PortGroup": null,
                "PortName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PrevAssignedId": 0,
                "Role": 0,
                "ScsiMode": 0,
                "SymbolicNodeName": null,
                "SymbolicPortName": null,
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "reserve_1",
            "AluaId": 2079,
            "BackEndRoleInUse": false,
            "Caption": "reserve_1",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "reserve_1 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "5385d54f-9ddd-403e-b3a0-84b353992a1c",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC001BB7758",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "00-00-00-00-00-00-00-00",
            "PresenceStatus": 2,
            "RoleCapability": 5,
            "Roles": "None",
            "SequenceNumber": 38232336,
            "ServerPortProperties": {
                "ConnectionMode": 0,
                "DataRateMode": 0,
                "DisableMirrorPortWhileStopped": false,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 0,
                "HardIdMode": 0,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PortDownTimeout": 0,
                "PortGroup": null,
                "PortName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PrevAssignedId": 0,
                "Role": 0,
                "ScsiMode": 0,
                "SymbolicNodeName": null,
                "SymbolicPortName": null,
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "ssv1_mr2_old",
            "AluaId": 2078,
            "BackEndRoleInUse": false,
            "Caption": "ssv1_mr2_old",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "ssv1_mr2_old on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "afc62170-780f-4aa4-95b3-6c634ea7cfca",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC000F470BA",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 3,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "00-00-00-00-00-00-00-00",
            "PresenceStatus": 2,
            "RoleCapability": 7,
            "Roles": "MR",
            "SequenceNumber": 38232335,
            "ServerPortProperties": {
                "ConnectionMode": 0,
                "DataRateMode": 0,
                "DisableMirrorPortWhileStopped": false,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 0,
                "HardIdMode": 0,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PortDownTimeout": 0,
                "PortGroup": null,
                "PortName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PrevAssignedId": 0,
                "Role": 4,
                "ScsiMode": 0,
                "SymbolicNodeName": null,
                "SymbolicPortName": null,
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "ssv1_mr1_old",
            "AluaId": 2077,
            "BackEndRoleInUse": false,
            "Caption": "ssv1_mr1_old",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "ssv1_mr1_old on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "8e46a7ca-4587-479a-8f69-aba64d029d80",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC000F470B6",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 3,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "00-00-00-00-00-00-00-00",
            "PresenceStatus": 2,
            "RoleCapability": 7,
            "Roles": "MR",
            "SequenceNumber": 38232334,
            "ServerPortProperties": {
                "ConnectionMode": 0,
                "DataRateMode": 0,
                "DisableMirrorPortWhileStopped": false,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 0,
                "HardIdMode": 0,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PortDownTimeout": 0,
                "PortGroup": null,
                "PortName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PrevAssignedId": 0,
                "Role": 4,
                "ScsiMode": 0,
                "SymbolicNodeName": null,
                "SymbolicPortName": null,
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "ssv1_fe1_old",
            "AluaId": 2076,
            "BackEndRoleInUse": false,
            "Caption": "ssv1_fe1_old",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "ssv1_fe1_old on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "dcf8ac29-5a85-4d73-8697-e4ed2b96c51b",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "51402EC000F470B4",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 2,
            "PortName": null,
            "PortType": 2,
            "PortWwn": "00-00-00-00-00-00-00-00",
            "PresenceStatus": 2,
            "RoleCapability": 5,
            "Roles": "FE",
            "SequenceNumber": 38232333,
            "ServerPortProperties": {
                "ConnectionMode": 0,
                "DataRateMode": 0,
                "DisableMirrorPortWhileStopped": false,
                "DisablePortWhileStopped": false,
                "HardAssignedId": 0,
                "HardIdMode": 0,
                "MaxActiveICommands": 0,
                "MaxActiveTCommands": 0,
                "NodeName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PortDownTimeout": 0,
                "PortGroup": null,
                "PortName": {
                    "Name": "00-00-00-00-00-00-00-00"
                },
                "PrevAssignedId": 0,
                "Role": 1,
                "ScsiMode": 0,
                "SymbolicNodeName": null,
                "SymbolicPortName": null,
                "UseSoftWWN": false,
                "VmIdMode": 0
            },
            "Status": "Not present",
            "StatusLevel": 2
        },
        {
            "Alias": "Loopback Port 3",
            "AluaId": 2054,
            "BackEndRoleInUse": false,
            "Caption": "Loopback Port 3",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "Loopback Port 3 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "b9daa0f4-c86b-47e0-8b59-6fa17dca51b7",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "2006449F7F0D2494",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 3,
            "PortName": null,
            "PortType": 4,
            "PortWwn": "20-06-44-9F-7F-0D-24-94",
            "PresenceStatus": 1,
            "RoleCapability": 3,
            "Roles": "BE,FE",
            "SequenceNumber": 38232332,
            "ServerPortProperties": {
                "PortGroup": null,
                "Role": 3
            },
            "Status": "Connected",
            "StatusLevel": 0
        },
        {
            "Alias": "Loopback Port 2",
            "AluaId": 2053,
            "BackEndRoleInUse": false,
            "Caption": "Loopback Port 2",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "Loopback Port 2 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "6f2e1249-d14f-4a2f-a40e-b72321cc76a3",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "2004449F7F0D2494",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 3,
            "PortName": null,
            "PortType": 4,
            "PortWwn": "20-04-44-9F-7F-0D-24-94",
            "PresenceStatus": 1,
            "RoleCapability": 3,
            "Roles": "BE,FE",
            "SequenceNumber": 38232331,
            "ServerPortProperties": {
                "PortGroup": null,
                "Role": 3
            },
            "Status": "Connected",
            "StatusLevel": 0
        },
        {
            "Alias": "Loopback Port 1",
            "AluaId": 2052,
            "BackEndRoleInUse": false,
            "Caption": "Loopback Port 1",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "Loopback Port 1 on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "1f96d1f6-878e-4ed9-86f8-644d0a0a86f0",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "2002449F7F0D2494",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 3,
            "PortName": null,
            "PortType": 4,
            "PortWwn": "20-02-44-9F-7F-0D-24-94",
            "PresenceStatus": 1,
            "RoleCapability": 3,
            "Roles": "BE,FE",
            "SequenceNumber": 38232330,
            "ServerPortProperties": {
                "PortGroup": null,
                "Role": 3
            },
            "Status": "Connected",
            "StatusLevel": 0
        },
        {
            "Alias": "Loopback Port",
            "AluaId": 2051,
            "BackEndRoleInUse": false,
            "Caption": "Loopback Port",
            "Connected": true,
            "Description": null,
            "ExtendedCaption": "Loopback Port on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "fe8bf208-8436-4ad8-9f7f-917c00476a5b",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "2000449F7F0D2494",
            "PortIpAddress": null,
            "PortIqn": null,
            "PortMode": 3,
            "PortName": null,
            "PortType": 4,
            "PortWwn": "20-00-44-9F-7F-0D-24-94",
            "PresenceStatus": 1,
            "RoleCapability": 3,
            "Roles": "BE,FE",
            "SequenceNumber": 38232329,
            "ServerPortProperties": {
                "PortGroup": null,
                "Role": 3
            },
            "Status": "Connected",
            "StatusLevel": 0
        },
        {
            "Alias": "Microsoft iSCSI Initiator",
            "AluaId": 0,
            "BackEndRoleInUse": false,
            "Caption": "Microsoft iSCSI Initiator",
            "Connected": false,
            "Description": null,
            "ExtendedCaption": "Microsoft iSCSI Initiator on ssv1",
            "FrontEndRoleInUse": false,
            "HostId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF",
            "HostsServed": [],
            "Id": "0b288058-7f82-420e-8575-fb18dbe37365",
            "Internal": false,
            "MirrorRoleInUse": false,
            "PhysicalName": "MSFT-05-1991",
            "PortIpAddress": null,
            "PortIqn": "iqn.1991-05.com.microsoft:ssv1.akf.lan",
            "PortMode": 1,
            "PortName": null,
            "PortType": 3,
            "PortWwn": null,
            "PresenceStatus": 1,
            "RoleCapability": 6,
            "Roles": "BE,MR",
            "SequenceNumber": 38232328,
            "ServerPortProperties": {
                "PortGroup": null,
                "Role": 6
            },
            "Status": "Not connected",
            "StatusLevel": 0
        }
    ],
    "SnapshotMapStoreId": "",
    "SnapshotMapStorePoolId": "4B273A2A-1FE0-41D0-B993-6F7B35672AAF:{4d235c44-e5c6-11ed-b80b-98f2b3e70bc1}",
    "State": 2,
    "Status": "Running",
    "StatusLevel": 0,
    "StorageUsed": {
        "Value": 342180044472320
    },
    "SupportState": 1,
    "SupportsCapacityOptimization": true,
    "SupportsEncryption": false,
    "TotalSystemMemory": {
        "Value": 137133355008
    },
    "VirtualDiskStorage": {
        "Value": 307907279192064
    }
}
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
    get_value_store,
    get_rate,
)


def check_datacore_rest_servers(item: str, section) -> CheckResult:
    """Check state of DataCore Servers"""

    data = section.get(item)
    if data is None:
        return

    perfdata = bool("PerformanceData" in data)

    # Status

    if not data["Status"] == "Running":
        message = f"SANsymphony Server is in state {data['Status']}"
        yield Result(state=State.CRIT, summary=message)
    else:
        message = "SANsymphony Server is running"
        yield Result(state=State.OK, summary=message)

    if data["CacheState"] != 2:
        message = "Cache is disabled"
        yield Result(state=State.WARN, summary=message)

    # Info

    if data["IsLicensed"] is False:
        message = "Server is not licensed"
        yield Result(state=State.WARN, summary=message)

    if data["LicenseExceeded"] is True:
        message = "License exceeded"
        yield Result(state=State.CRIT, summary=message)

    # InUseCacheSize
    # LicenseRemaining
    # LicensedCapacityLimit

    message = f"Version: {data['ProductVersion']}".replace(" ", "").replace(",", " ")
    details = f"Version: {data['ProductVersion']}\n Build: {data['ProductBuild']}\n OS: {data['OsVersion']}\n CPUs: {data['ProcessorInfo']['NumberCores']} x {data['ProcessorInfo']['ProcessorName']}"
    yield Result(state=State.OK, summary=message, details=details)

    # Perfdata

    if perfdata:

        raw_performance_counters = [
            "TotalReads",
            "TotalWrites",
            "TotalBytesRead",
            "TotalBytesWritten",
            "InitiatorReads",
            "InitiatorWrites",
            "InitiatorBytesRead",
            "InitiatorBytesWritten",
            "TargetReads",
            "TargetWrites",
            "TargetBytesRead",
            "TargetBytesWritten",
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
        # TODO yield Metric
        percent_read, percent_write = calculate_percentages(
            rate["TotalReads"], rate["TotalWrites"]
        )

        performance_metrics = [
            ("disk_read_ios", rate["TotalReads"]),
            ("disk_write_ios", rate["TotalWrites"]),
            ("disk_read_throughput", rate["TotalBytesRead"]),
            ("disk_write_throughput", rate["TotalBytesWritten"]),
            ("ssv_initiator_reads", rate["InitiatorReads"]),
            ("ssv_initiator_writes", rate["InitiatorWrites"]),
            ("ssv_initiator_read_throughput", rate["InitiatorBytesRead"]),
            ("ssv_initiator_write_throughput", rate["InitiatorBytesWritten"]),
            ("ssv_target_reads", rate["TargetReads"]),
            ("ssv_target_writes", rate["TargetWrites"]),
            ("ssv_target_read_throughput", rate["TargetBytesRead"]),
            ("ssv_target_write_throughput", rate["TargetBytesWritten"]),
        ]

        for description, metric in performance_metrics:
            yield Metric(description, metric)


agent_section_datacore_rest_servers = AgentSection(
    name="datacore_rest_servers",
    parse_function=parse_datacore_rest,
    parsed_section_name="datacore_rest_servers",
)


check_plugin_datacore_rest_servers = CheckPlugin(
    name="datacore_rest_servers",
    service_name="SANsymphony Server %s",
    sections=["datacore_rest_servers"],
    discovery_function=discover_datacore_rest,
    check_function=check_datacore_rest_servers,
)
