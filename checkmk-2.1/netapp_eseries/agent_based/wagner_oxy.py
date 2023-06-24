#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2022 Bechtle IT Systemhaus Solingen
#          Andre Eckstein <andre.eckstein@bechtle.com>

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

# DT 11.11.2021
# wagner_oxygen                           snmp       (no man page present)
# 1 Status 0 = OK, 1 = WARN, 2 = CRIT
# 2 Servicename darf keine Leerzeichen verwenden
# 3 Metriken

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    contains,
    register,
    SNMPTree,
    Result,
    Service,
    State,
    Metric
)


warn = float(16.99)
crit = float(16.95)


def discover_wagner_oxygen(section) -> DiscoveryResult:
    if section[0][0]:
        yield Service()


def check_wagner_oxygen(section) -> CheckResult:
    oxygen_value = int(section[0][0])
    oxygen_value = float(oxygen_value/100)
    infotext = f"Co2: {oxygen_value} (warn/crit) at {warn}/{crit}"

    yield Metric(
        "Co2",
        oxygen_value,
        levels=(warn, crit),
        boundaries=(0, 30))

    if oxygen_value <= crit:
        yield Result(state=State.CRIT, summary=infotext)
    elif oxygen_value <= warn:
        yield Result(state=State.WARN, summary=infotext)
    else: 
        yield Result(state=State.OK, summary=infotext)


register.snmp_section(
    name = "wagner_oxygen",
    detect=contains(".1.3.6.1.2.1.1.1.0", "eWON"),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.8284.2.1.3.1.11.1.4',
        oids = ['10'],
    ),
)


register.check_plugin(
    name='wagner_oxygen',
    service_name='Oxy Reduct Co2',
    discovery_function=discover_wagner_oxygen,
    check_function=check_wagner_oxygen,
)
