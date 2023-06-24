#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-


# (c) 2022 Bechtle IT Systemhaus Solingen
#          Andre Eckstein <andre.eckstein@bechtle.com>
# Based on the Sittig plugin by Bastian Kuhn

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from .agent_based_api.v1.type_defs import (
    StringTable,
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    contains,
    register,
    SNMPTree,
    Result,
    Service,
    OIDEnd,
    State
)


def parse_sittig_ars(string_table):
    return string_table if any(string_table) else None


register.snmp_section(
    name = "sittig_ars",
    parse_function=parse_sittig_ars,
    detect=contains(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.311.1.1.3.1.2"),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.33472.4.16.3.1',
        oids = [
            OIDEnd(),
            '1',    # online
            '2',    # online
            '3',    # bothonline
            '4'     # offlineok
        ],
    ),
)


def discover_sittig_ars(section) -> DiscoveryResult:
    for line in section:
        yield Service(item=line[0])


def check_sittig_ars(item, section) -> CheckResult:
    for line in section:
        if line[0] == item:
            if line[1:] == ["2", "2", "2", "4"]:  # online, online, bothonline, offlineok
                yield Result(state=State.OK, summary=f"ARS {item} is online.")
            else:
                yield Result(state=State.CRIT, summary=f"ARS {item} is offline or partially offline.")


register.check_plugin(
    name='sittig_ars',
    service_name='ARS %s',
    discovery_function=discover_sittig_ars,
    check_function=check_sittig_ars,
)
