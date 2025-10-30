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
)

agent_section_netapp_eseries_drawers = AgentSection(
    name="netapp_eseries_drawers",
    parse_function=parse_netapp_eseries,
    parsed_section_name="netapp_eseries_drawers",
)


def check_netapp_eseries_drawers(item: str, section) -> CheckResult:
    """Check state of Netapp E-Series Drawers"""
    data = section.get(item)

    if data is None:
        return

    status = data.get('status')
    serial_number = data.get('serialNumber')
    is_open = data.get('isOpen')

    message = f"Drawer with serial {serial_number}, status: {status}"
    if status != "optimal":
        state = State.WARN
    else:
        state = State.OK
    yield Result(state=State(state), summary=message)

    if is_open:
        message = "Drawer is open"
        state = State.WARN
        yield Result(state=State(state), summary=message)


check_plugin_netapp_eseries_drawers = CheckPlugin(
    name="netapp_eseries_drawers",
    service_name="Drawer %s",
    sections=["netapp_eseries_drawers"],
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_drawers,
)
