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


agent_section_netapp_eseries_controllers = AgentSection(
    name="netapp_eseries_controllers",
    parse_function=parse_netapp_eseries,
    parsed_section_name="netapp_eseries_controllers",
)


def check_netapp_eseries_controllers(item: str, section) -> CheckResult:
    """Check state of Netapp E-Series Controllers"""

    data = section.get(item)

    if data is None:
        return

    status = data.get('status')
    serial_number = data.get('serialNumber').rstrip()
    name = data.get('physicalLocation').get('label')
    # is_active = data.get('active')
    # appVersion = data.get('appVersion')
    model = data.get('modelName')

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

        avg_cpu_utilization = round(data.get('performance').get('cpuAvgUtilization'))
        fullStripeWrites = round(data.get('performance').get('fullStripeWritesBytesPercent'))

    message = f"Controller {name} Model {model}, status: {status}, serial nr.: {serial_number}"
    if status != "optimal":
        state = State.WARN
    else:
        state = State.OK
    yield Result(state=State(state), summary=message)

    # Metrics
    if perfdata:
        yield Metric("disk_read_ios", disk_read_ios)
        yield Metric("disk_write_ios", disk_write_ios)
        yield Metric("disk_read_throughput", disk_read_throughput)
        yield Metric("disk_write_throughput", disk_write_throughput)
        yield Metric("read_latency", disk_read_responsetime / 1000)
        yield Metric("write_latency", disk_write_responsetime / 1000)
        yield Metric("fullStripeWrites", value=fullStripeWrites, boundaries=(0, 100))
        yield Metric("util", avg_cpu_utilization)


check_plugin_netapp_eseries_controllers = CheckPlugin(
    name="netapp_eseries_controllers",
    service_name="Controller %s",
    sections=["netapp_eseries_controllers"],
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_controllers,
)
