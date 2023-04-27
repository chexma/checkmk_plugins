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
    render,
    Metric,
)

from .netapp_eseries import (parse_netapp_eseries,
                             discovery_netapp_eseries_multiple)

register.agent_section(
    name="netapp_eseries_volumes",
    parse_function=parse_netapp_eseries,
)


def check_netapp_eseries_volumes(item: str, params, section) -> CheckResult:
    data = section.get(item)
    
    size_bytes = int(data['totalSizeInBytes'])
    size = render.bytes(size_bytes)
    status = data['status']
    state = 0

    name = data['name'],
    is_mapped = data['mapped']
    size_capacity = int(data['capacity'])
    is_thin_provisioned = data['thinProvisioned']
    raid_level = data['raidLevel']
    is_offline = data['offline']
    is_flash_cached = data['flashCached']

    if 'performance' in data:
        perfdata = True
    else:
        perfdata = None

    if perfdata:
        disk_read_ios = round(data.get('performance').get('readIOps'), 3)
        disk_write_ios = round(data.get('performance').get('writeIOps'), 3)
        disk_read_throughput = round(data.get('performance').get('readThroughput'), 3) * 1024 * 1024
        disk_write_throughput = round(data.get('performance').get('writeThroughput'), 3) * 1024 * 1024
        disk_read_responsetime = round(data.get('performance').get('readResponseTime'), 3)
        disk_write_responsetime = round(data.get('performance').get('writeResponseTime'), 3)

    if is_offline is True:
        message = f"Volume {item} is OFFLINE"
        state = State.CRIT
    else:
        message = f"Volume {item}, size: {size}, raidlevel: {raid_level}, status: {status}"
        if status != "optimal":
            state = State.WARN
        else:
            state = State.OK
    yield Result(state=State(state), summary=message)

# Details
    yield Result(state=State.OK, notice = f"Mapped: {is_mapped}\n \
            Thin provisioned: {is_thin_provisioned}\n \
            Flash cached: {is_flash_cached}")

# Metrics
    if perfdata and not is_offline:
        yield Metric("disk_read_ios", disk_read_ios)
        yield Metric("disk_write_ios", disk_write_ios)
        yield Metric("disk_read_throughput", disk_read_throughput)
        yield Metric("disk_write_throughput", disk_write_throughput)
        yield Metric("read_latency", disk_read_responsetime / 1000)
        yield Metric("write_latency", disk_write_responsetime / 1000)

        state = State.OK
        message = f"Read: {render.iobandwith(disk_read_throughput)}, Write: {render.iobandwith(disk_write_throughput)}, Read operations: {disk_read_ios}/s, Write operations: {disk_write_ios}/s"
        yield Result(state=State(state), summary=message)


register.check_plugin(
    name="netapp_eseries_volumes",
    service_name="Volume %s",
    sections=["netapp_eseries_volumes"],
    check_default_parameters={
        'volume_state': 0,
    },
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_volumes,
    check_ruleset_name="netapp_eseries_volumes",
)
