#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Andre Eckstein 'andre.eckstein@bechtle.com'
# License: GNU General Public License v2

from typing import Dict, Optional
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    all_of,
    exists,
    register,
    startswith,
    Result,
    Service,
    SNMPTree,
    State,
)

from cmk.base.plugins.agent_based.agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    StringTable,
)

Section = Dict[str, Dict[str, str]]


def parse_sophosxg_s2s(string_table: StringTable) -> Optional[Section]:
    parsed = {}
    for s2s_tunnel in string_table:
        parsed.setdefault(s2s_tunnel[0], {"state": s2s_tunnel[1], "status_detail": s2s_tunnel[2]})
    return parsed


def discover_sophosxg_s2s(section: Section) -> DiscoveryResult:
    for s2s_tunnel in section.keys():
        yield Service(item=s2s_tunnel)


def check_sophosxg_s2s(item: str, section: Optional[Section]) -> CheckResult:
    data = section.get(item)
    if not data:
        return

    tunnel_state_dict: Dict[int, str] = {
        0: "inactive",
        1: "?",
        2: "active",
    }

    tunnel_status_detail_dict: Dict[int, str] = {
        0: "inactive",
        1: "active",
        2: "warning",
    }

    tunnel_status = int(data["state"])
    tunnel_status_detail = int(data["status_detail"])
                               
    if tunnel_status == 2 and tunnel_status_detail == 1:
        yield Result(state=State.OK, summary=f"S2S Tunnel {item} is up, state is {tunnel_state_dict[tunnel_status]}")
    else:
        yield Result(state=State.CRIT, summary=f"S2S is down, state is {tunnel_state_dict[tunnel_status]}, detailed status {tunnel_status_detail_dict[tunnel_status_detail]} ")


register.snmp_section(
    name="sophosxg_s2s",
    parse_function=parse_sophosxg_s2s,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.2604.5.1.6.1.1.1.1",
         oids=[
            "2",   # S2S Name
            "6",   # S2S Status (An/aus)
            "9",   # S2S Zustand (0=inactive, 1=active, 2=Warnung(Netzbeziehung down)
        ],
    ),
    detect=all_of(
        startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.2604.5"),
        exists(".1.3.6.1.4.1.2604.5.1.1.*"),
    ),
)
 
register.check_plugin(
    name="sophosxg_s2s",
    service_name="Sophos S2S-VPN %s",
    discovery_function=discover_sophosxg_s2s,
    check_function=check_sophosxg_s2s,
)