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
    discovery_netapp_eseries_multiple,
#    NetappAPIData
)

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
    render
)


agent_section_netapp_eseries_batteries = AgentSection(
    name="netapp_eseries_batteries",
    parse_function=parse_netapp_eseries,
    parsed_section_name="netapp_eseries_batteries",
)


def check_netapp_eseries_batteries(item: str, section) -> CheckResult:
    """Check state of Netapp E-Series Batteries"""
    data = section.get(item)

    if data is None:
        return

    status = data['status']
    serial_number = data['vendorSN']

    last_test = data.get('learnCycleData').get('lastBatteryLearnCycle')
    next_test = data.get('learnCycleData').get('nextBatteryLearnCycle')
    battery_life_remaining = abs(data.get('batteryLifeRemaining'))
    battery_age = data.get('batteryAge')

    message = f"Battery {item}, status: {status}, serial nr.: {serial_number}"

    if status in ["optimal", "maintenanceCharging", "learning"]:
        state = State.OK
    else:
        state = State.WARN
    yield Result(state=State(state), summary=message)

    yield Result(state=State.OK,
            notice = f"Last test: {render.datetime(last_test)} \n \
            Next test: {render.datetime(next_test)}, \n \
            Life remaining: {battery_life_remaining} \n \
            Age: {battery_age}")


check_plugin_netapp_eseries_batteries = CheckPlugin(
    name="netapp_eseries_batteries",
    service_name="Battery %s",
    sections=["netapp_eseries_batteries"],
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_batteries,
)
