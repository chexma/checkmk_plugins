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

# Example Output:
#
#

from .agent_based_api.v1.type_defs import (
    CheckResult, )

from .agent_based_api.v1 import (
    register,
    Result,
    State,
    Metric,
    render
)

from .netapp_eseries import (parse_netapp_eseries,
                             discovery_netapp_eseries_multiple)

register.agent_section(
    name="netapp_eseries_interfaces",
    parse_function=parse_netapp_eseries,
)


def check_netapp_eseries_interfaces(item: str, params, section) -> CheckResult:
    data = section.get(item)

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
    if interface_type == "sas":
        status = interface_data['iocPort']['state']
    elif interface_type == "iscsi":
        status = interface_data['interfaceData']['ethernetData']['linkStatus']
    elif interface_type == "fibre":
        status = interface_data['linkStatus']
        
    message = f"Port status: {status}"

    if status not in ["optimal", "up"]:
        state = State.WARN
    else:
        state = State.OK
    yield Result(state=State(state), summary=message)

    # Metrics
    if perfdata and status != 'down':
        yield Metric("disk_read_ios", disk_read_ios)
        yield Metric("disk_write_ios", disk_write_ios)
        yield Metric("disk_read_throughput", disk_read_throughput)
        yield Metric("disk_write_throughput", disk_write_throughput)
        
        state = State.OK
        message = f"Read: {render.bytes(disk_read_throughput)}/s, Write: {render.bytes(disk_write_throughput)}/s, Read operations: {disk_read_ios}/s, Write operations: {disk_write_ios}/s"
        yield Result(state=State(state), summary=message)

register.check_plugin(
    name="netapp_eseries_interfaces",
    service_name="Interface %s",
    sections=["netapp_eseries_interfaces"],
    check_default_parameters={
        'interface_state': 0,
    },
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_interfaces,
    check_ruleset_name="netapp_eseries_interfaces",
)
