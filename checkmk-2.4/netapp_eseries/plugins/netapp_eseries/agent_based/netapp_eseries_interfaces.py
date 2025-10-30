#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Andreas Doehler <andreas.doehler@bechtle.com/andreas.doehler@gmail.com>
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


from cmk_addons.plugins.netapp_eseries.lib import (
    parse_netapp_eseries,
    discovery_netapp_eseries_multiple
)

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
    Metric,
    render
)

agent_section_netapp_eseries_interfaces = AgentSection(
    name="netapp_eseries_interfaces",
    parse_function=parse_netapp_eseries,
    parsed_section_name="netapp_eseries_interfaces",
)


def check_netapp_eseries_interfaces(item: str, section) -> CheckResult:
    """Check state of Netapp E-Series Interfaces"""
    data = section.get(item)

    if data is None:
        return

    if 'performance' in data:
        perfdata = True
    else:
        perfdata = None

    if perfdata:
        disk_read_ios = round(data.get('performance').get('readIOps', 0), 3)
        disk_write_ios = round(data.get('performance').get('writeIOps', 0), 3)
        disk_read_throughput = round(data.get('performance').get('readThroughput', 0), 3) * 1024 * 1024
        disk_write_throughput = round(data.get('performance').get('writeThroughput', 0), 3) * 1024 * 1024

    channel_type = data.get('channelType')
    interface_type = data.get("ioInterfaceTypeData").get("interfaceType")
    if interface_type == "fc":
        interface_type = "fibre"
    interface_data = data.get("ioInterfaceTypeData").get(interface_type)

    # Backend Ports (driveside)
    if channel_type == "driveside":

        if interface_type == "pcie":
            channel = interface_data['channel']
            status = f"driveside nvme - channel {channel} - status undefined"

            current_interface_speed = interface_data['currentInterfaceSpeed']
            maximum_interface_speed = interface_data['maximumInterfaceSpeed']

            message = f"Port status: {status}"
            details = f"Port status: {status} \n"

            state = State.OK

        if interface_type == "sas":
            channel = interface_data['channel']
            status = interface_data['iocPort']['state']

            current_interface_speed = interface_data['currentInterfaceSpeed']
            maximum_interface_speed = interface_data['maximumInterfaceSpeed']
            is_degraded = interface_data['isDegraded']

            message = f"Port status: {status}"
            details = f"Port status: {status} \n"

            if is_degraded != 'False':
                state = State.OK
            else:
                state = State.WARN

    # Frontend Ports (hostside)
    elif channel_type == "hostside":

        if interface_type == "ib":
            status = interface_data['linkState']
            message = f"Port status: {status}"
            details = f"Port status: {status} \n"
            # interface speed: {current_interface_speed} \n \
            # maximum speed: {maximum_interface_speed} \n \
            # configured speed: {speed_setting}

        elif interface_type == "sas":
            status = interface_data['iocPort']['state']
            message = f"Port status: {status}"
            details = f"Port status: {status} \n"
            # interface speed: {current_interface_speed} \n \
            # maximum speed: {maximum_interface_speed} \n \
            # configured speed: {speed_setting}

        elif interface_type == "iscsi":
            status = interface_data['interfaceData']['ethernetData']['linkStatus']
            message = f"Port status: {status}"
            details = f"Port status: {status} \n"
            # interface speed: {current_interface_speed} \n \
            # maximum speed: {maximum_interface_speed} \n \
            # configured speed: {speed_setting}

        elif interface_type == "fibre":
            status = interface_data['linkStatus']
            wwpn = interface_data['portName']
            topology = interface_data['topology']
            speed_setting = interface_data['speedControl']
            current_interface_speed = interface_data['currentInterfaceSpeed']
            maximum_interface_speed = interface_data['maximumInterfaceSpeed']

            message = f"Port status: {status}, wwwpn: {wwpn}, , interface speed: {current_interface_speed}"
            details = f"Port status: {status} \n \
                        Topology: {topology} \n \
                        World Wide Portname: {wwpn} \n \
                        interface speed: {current_interface_speed} \n \
                        maximum speed: {maximum_interface_speed} \n \
                        configured speed: {speed_setting} \
            "

        if status not in ["optimal", "up", "active"]:
            state = State.WARN
        else:
            state = State.OK

    yield Result(state=State(state), summary=message, details=details)

    # Metrics
    if perfdata and status != 'down':
        yield Metric("disk_read_ios", disk_read_ios)
        yield Metric("disk_write_ios", disk_write_ios)
        yield Metric("disk_read_throughput", disk_read_throughput)
        yield Metric("disk_write_throughput", disk_write_throughput)

        state = State.OK
        message = f"Read: {render.iobandwidth(disk_read_throughput)}, Write: {render.iobandwidth(disk_write_throughput)}, Read operations: {disk_read_ios}/s, Write operations: {disk_write_ios}/s"
        yield Result(state=State(state), summary=message)


check_plugin_netapp_eseries_interfaces = CheckPlugin(
    name="netapp_eseries_interfaces",
    service_name="Interface %s",
    sections=["netapp_eseries_interfaces"],
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_interfaces,
)
