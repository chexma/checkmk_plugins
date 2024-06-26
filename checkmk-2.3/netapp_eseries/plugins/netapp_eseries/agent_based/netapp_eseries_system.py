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

from cmk.plugins.netapp_eseries.lib import (
    parse_netapp_eseries,
    discovery_netapp_eseries_multiple
)

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
    Metric
)


agent_section_netapp_eseries_pools = AgentSection(
    name="netapp_eseries_system",
    parse_function=parse_netapp_eseries,
    parsed_section_name="netapp_eseries_system",
)


def check_netapp_eseries_system(item: str, section) -> CheckResult:
    """Check state of Netapp E-Series System"""
    data = section.get(item)

    if data is None:
        return

    status = data.get('status')
    serial_number = data.get('chassisSerialNumber')
    firmware_version = data.get('fwVersion')
    boot_version = data.get('bootVersion')
    model = data.get('model').upper()

    disk_read_ios = round(data.get('performance').get('readIOps'), 3)
    disk_write_ios = round(data.get('performance').get('writeIOps'), 3)
    disk_read_throughput = round(data.get('performance').get('readThroughput'), 3) * 1024 * 1024
    disk_write_throughput = round(data.get('performance').get('writeThroughput'), 3) * 1024 * 1024
    disk_read_responsetime = round(data.get('performance').get('readResponseTime'), 3)
    disk_write_responsetime = round(data.get('performance').get('writeResponseTime'), 3)

    message = f"E-Series {model}, status: {status}, serial nr.: {serial_number}"
    if status != "optimal":
        state = State.WARN
    else:
        state = State.OK
    yield Result(state=State(state), summary=message)

    yield Result(state=State.OK,
        notice = f"Firmware Version: {firmware_version} \n \
                   Boot Version : {boot_version} \n \
                   Serial Number: {serial_number} \n \
            ")

    yield Metric("disk_read_ios", disk_read_ios)
    yield Metric("disk_write_ios", disk_write_ios)
    yield Metric("disk_read_throughput", disk_read_throughput)
    yield Metric("disk_write_throughput", disk_write_throughput)
    yield Metric("read_latency", disk_read_responsetime / 1000)
    yield Metric("write_latency", disk_write_responsetime / 1000)


check_plugin_netapp_eseries_system = CheckPlugin(
    name="netapp_eseries_system",
    service_name="System Info %s",
    sections=["netapp_eseries_system"],
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_system,
)
