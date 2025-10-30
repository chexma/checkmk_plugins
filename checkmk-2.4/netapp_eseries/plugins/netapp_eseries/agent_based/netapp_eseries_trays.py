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


agent_section_netapp_eseries_pools = AgentSection(
    name="netapp_eseries_trays",
    parse_function=parse_netapp_eseries,
    parsed_section_name="netapp_eseries_trays",
)


def check_netapp_eseries_trays(item: str, section) -> CheckResult:
    """Check state of Netapp E-Series Trays"""

    data = section.get(item)

    if data is None:
        return

    dev_type = data.get("type")
    slots = data.get("numDriveSlots")
    serial_number = data.get("serialNumber").strip()
    part_number = data.get("partNumber").strip()
    tray_id = data.get("trayId")

    message = f"Tray ID {tray_id}, type: {dev_type} with {slots} slots, serial nr.: {serial_number}, part number: {part_number}"
    yield Result(state=State(State.OK), summary=message)

    error_list = ["trayIDMismatch", "esmVersionMismatch", "esmMiswire",
                  "drvMHSpeedMismatch", "unsupportedTray", "esmGroupError",
                  "uncertifiedTray", "esmHardwareMismatch", "isMisconfigured",
                  "esmFactoryDefaultsMismatch", "nonRedundantAccess"]

    for element in error_list:
        if data.get(element):
            state = State.WARN
            message += f", {element}"
            yield Result(state=State(state), summary=message)


check_plugin_netapp_eseries_trays = CheckPlugin(
    name="netapp_eseries_trays",
    service_name="Tray %s",
    sections=["netapp_eseries_trays"],
    discovery_function=discovery_netapp_eseries_multiple,
    check_function=check_netapp_eseries_trays,
)
