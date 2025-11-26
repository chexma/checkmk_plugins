#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Agent Statistics"""

import json
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
    Metric,
    check_levels,
    render,
)


def parse_wazuh_agents(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_agents(section):
    """Discover the Wazuh Agents service."""
    if section:
        yield Service()


def check_wazuh_agents(params, section):
    """Check Wazuh agent statistics."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    active = section.get("active", 0)
    disconnected = section.get("disconnected", 0)
    never_connected = section.get("never_connected", 0)
    pending = section.get("pending", 0)
    total = section.get("total", 0)

    # Calculate percentages
    disconnected_pct = (disconnected / total * 100) if total > 0 else 0.0

    # Main status
    yield Result(
        state=State.OK,
        summary=f"Total: {total}, Active: {active}",
    )

    # Disconnected Agents (absolute)
    yield from check_levels(
        disconnected,
        levels_upper=params.get("levels_disconnected"),
        metric_name="wazuh_agents_disconnected",
        label="Disconnected",
        render_func=lambda x: str(int(x)),
    )

    # Disconnected Agents (percentage)
    yield from check_levels(
        disconnected_pct,
        levels_upper=params.get("levels_disconnected_percent"),
        metric_name="wazuh_agents_disconnected_pct",
        label="Disconnected",
        render_func=render.percent,
    )

    # Never Connected
    yield from check_levels(
        never_connected,
        levels_upper=params.get("levels_never_connected"),
        metric_name="wazuh_agents_never_connected",
        label="Never connected",
        render_func=lambda x: str(int(x)),
    )

    # Pending
    yield from check_levels(
        pending,
        levels_upper=params.get("levels_pending"),
        metric_name="wazuh_agents_pending",
        label="Pending",
        render_func=lambda x: str(int(x)),
    )

    # Additional metrics
    yield Metric("wazuh_agents_active", active)
    yield Metric("wazuh_agents_total", total)


agent_section_wazuh_agents = AgentSection(
    name="wazuh_agents",
    parse_function=parse_wazuh_agents,
)


check_plugin_wazuh_agents = CheckPlugin(
    name="wazuh_agents",
    service_name="Wazuh Agents",
    discovery_function=discover_wazuh_agents,
    check_function=check_wazuh_agents,
    check_default_parameters={
        "levels_disconnected": ("fixed", (1, 5)),
        "levels_disconnected_percent": ("fixed", (5.0, 10.0)),
        "levels_never_connected": ("fixed", (5, 10)),
        "levels_pending": ("fixed", (10, 20)),
    },
    check_ruleset_name="wazuh_agents",
)
