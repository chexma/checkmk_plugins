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

from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    CheckResult, )

from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    register,
    Result,
    State,
    render,
    get_value_store,
    Metric
)

from cmk.base.plugins.agent_based.utils.df import df_check_filesystem_single, FILESYSTEM_DEFAULT_PARAMS

from .netapp_eseries import (parse_netapp_eseries,
                             discovery_netapp_eseries_multiple)

register.agent_section(
    name="netapp_eseries_pools",
    parse_function=parse_netapp_eseries,
)


def check_netapp_eseries_pools(item: str, params, section) -> CheckResult:
    value_store = get_value_store()
    data = section.get(item)

    size_total_bytes = int(data['totalRaidedSpace'])
    size_free_bytes = int(data['freeSpace'])
    size_used_bytes = int(data['usedSpace'])
    size = render.bytes(size_total_bytes)

    name = data.get('name')
    raid_level = data.get('raidLevel')
    status = data.get('state')
    raid_status = data.get('raidStatus')
    is_offline = data.get('offline')

    if 'performance' in data:
        perfdata = True
    else:
        perfdata = None

    if perfdata:
        disk_read_ios = round(data.get('performance').get('readIOps'), 2)
        disk_write_ios = round(data.get('performance').get('writeIOps'), 2)
        disk_read_throughput = round(data.get('performance').get('readThroughput'), 2) * 1024 * 1024
        disk_write_throughput = round(data.get('performance').get('writeThroughput'), 2) * 1024 * 1024
    
    if is_offline:
        state = State.CRIT
        message = f"Pool {name} is offline"
    else:
        message = f"Pool {name}, status: {status}"
        if status != "complete" or raid_status != 'optimal':
            state = State.WARN
        else:
            state = State.OK
    yield Result(state=State(state), summary=message)

    yield from df_check_filesystem_single(
        value_store,
        item,
        size_total_bytes / 1024 ** 2,
        size_free_bytes / 1024 ** 2,
        0,
        None,
        None,
        params=params,
    )

    if perfdata:
        yield Metric("disk_read_ios", disk_read_ios)
        yield Metric("disk_write_ios", disk_write_ios)
        yield Metric("disk_read_throughput", disk_read_throughput)
        yield Metric("disk_write_throughput", disk_write_throughput)
        state = State.OK
        message = f"Read: {render.bytes(disk_read_throughput)}/s, Write: {render.bytes(disk_write_throughput)}/s, Read operations: {disk_read_ios}/s, Write operations: {disk_write_ios}/s"
        yield Result(state=State(state), summary=message)


register.check_plugin(
    name="netapp_eseries_pools",
    service_name="Pool %s",
    sections=["netapp_eseries_pools"],
    check_default_parameters=FILESYSTEM_DEFAULT_PARAMS,
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_pools,
    check_ruleset_name="filesystem",
)
