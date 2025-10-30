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
    get_value_store,
    render
)

from cmk.plugins.lib.temperature import (
    check_temperature,
)


agent_section_netapp_eseries_drives = AgentSection(
    name="netapp_eseries_drives",
    parse_function=parse_netapp_eseries,
    parsed_section_name="netapp_eseries_drives",
)


def check_netapp_eseries_drives(item: str, params, section) -> CheckResult:
    """Check state of Netapp E-Series Drives"""
    data = section.get(item)

    if data is None:
        return

    # Failed drives show 255
    if data['driveTemperature']['currentTemp'] == 255:
        data['driveTemperature']['currentTemp'] = 0

    if 'performance' in data:
        perfdata = True
    else:
        perfdata = None

    if perfdata:
        disk_read_ios = round(data.get('performance').get('readIOps'), 3)
        disk_write_ios = round(data.get('performance').get('writeIOps'), 3)
        disk_read_throughput = round(data.get('performance').get('readThroughput'), 3) * 1024 * 1024
        disk_write_throughput = round(data.get('performance').get('writeThroughput'), 3) * 1024 * 1024

    # Status
    status = data['status']
    hasDegradedChannel = data['hasDegradedChannel']
    is_offline = data['offline']
    temperature = data['driveTemperature']['currentTemp']

    # Details
    size_bytes = int(data['usableCapacity'])
    firmware_version = data['firmwareVersion']
    manufacturer = data['manufacturer']
    media_type = data['driveMediaType']
    hot_spare = str(data['hotSpare'])
    serial_number = data['serialNumber']

    # SSD related
    if media_type == 'ssd':
        erase_count = int(data['ssdWearLife']['averageEraseCountPercent'])
        endurance_used = int(data['ssdWearLife']['percentEnduranceUsed'])
        spare_blocks = int(data['ssdWearLife']['spareBlocksRemainingPercent'])

    size = render.bytes(size_bytes)

# Status

    if is_offline is True:
        message = f"{media_type.upper()} Drive {item}, size: {size} is OFFLINE"
        state = State.CRIT
    else:
        message = f"{media_type.upper()} Drive {item}, status: {status}, size: {size}"
        if status != "optimal":
            state = State.WARN
        else:
            state = State.OK
    yield Result(state=State(state), summary=message)

    if hasDegradedChannel is True:
        message = "Drive has degraded Channel"
        yield Result(state=State.CRIT, summary=message)

# Details

    yield Result(state=State.OK,
        notice = f" \
            Firmware Version: {firmware_version}, \n \
            Manufacturer: {manufacturer}, \n \
            Media Type: {media_type.upper()}, \n \
            HotSpare: {hot_spare}, \n \
            Serial Number: {serial_number}")

# Metrics
    if perfdata and not is_offline:
        yield Metric("disk_read_ios", disk_read_ios)
        yield Metric("disk_write_ios", disk_write_ios)
        yield Metric("disk_read_throughput", disk_read_throughput)
        yield Metric("disk_write_throughput", disk_write_throughput)

        state = State.OK
        message = f"Read: {render.iobandwidth(disk_read_throughput)}, Write: {render.iobandwidth(disk_write_throughput)}, Read operations: {disk_read_ios}/s, Write operations: {disk_write_ios}/s"
        yield Result(state=State(state), summary=message)

    # SSD related
    if media_type == 'ssd':
        yield Metric("endurance", endurance_used, boundaries=(0, 100))
        yield Metric("spareBlocks", spare_blocks, boundaries=(0, 100))
        yield Metric("erase", erase_count, boundaries=(0, 100))

    yield from check_temperature(temperature,
                                 params,
                                 unique_name="netapp_eseries_temp_%s" % item,
                                 value_store=get_value_store(),)


check_plugin_netapp_eseries_drives = CheckPlugin(
    name="netapp_eseries_drives",
    service_name="Drive %s",
    sections=["netapp_eseries_drives"],
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_drives,
    check_default_parameters={
         'drive_state': 0,
    },
    check_ruleset_name="netapp_eseries_drives",
)
