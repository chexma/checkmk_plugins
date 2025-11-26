#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Outdated Agents"""

import json
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
    Metric,
    check_levels,
)


def parse_wazuh_agents_outdated(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_agents_outdated(section):
    """Discover the Wazuh Outdated Agents service."""
    if section:
        yield Service()


def check_wazuh_agents_outdated(params, section):
    """Check Wazuh outdated agents."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    total = section.get("total", 0)
    agents = section.get("agents", [])

    yield from check_levels(
        total,
        levels_upper=params.get("outdated_levels"),
        metric_name="wazuh_agents_outdated",
        label="Outdated agents",
        render_func=lambda x: str(int(x)),
    )

    if agents:
        agent_list = ", ".join(
            f"{a.get('name', 'unknown')} ({a.get('version', '?')})"
            for a in agents[:5]
        )
        if total > 5:
            agent_list += f" ... and {total - 5} more"
        yield Result(
            state=State.OK,
            notice=f"Outdated: {agent_list}",
        )


agent_section_wazuh_agents_outdated = AgentSection(
    name="wazuh_agents_outdated",
    parse_function=parse_wazuh_agents_outdated,
)


check_plugin_wazuh_agents_outdated = CheckPlugin(
    name="wazuh_agents_outdated",
    service_name="Wazuh Agents Outdated",
    discovery_function=discover_wazuh_agents_outdated,
    check_function=check_wazuh_agents_outdated,
    check_default_parameters={
        "outdated_levels": ("fixed", (1, 5)),
    },
    check_ruleset_name="wazuh_agents_outdated",
)
