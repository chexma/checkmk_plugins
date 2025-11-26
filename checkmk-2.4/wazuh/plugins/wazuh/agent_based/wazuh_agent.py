#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Agent (Individual, Piggyback)"""

import json
import time
from datetime import datetime
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
    HostLabel,
    check_levels,
    render,
)


def parse_wazuh_agent(string_table):
    """Parse JSON output from piggyback data."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def host_label_wazuh_agent(section):
    """Generate host labels from agent data."""
    if not section:
        return

    yield HostLabel("cmk/wazuh_agent", "yes")

    if section.get("os_platform"):
        yield HostLabel("cmk/os_platform", section["os_platform"])

    if section.get("os_name"):
        yield HostLabel("cmk/os_name", section["os_name"])

    if section.get("group"):
        groups = section["group"]
        if isinstance(groups, list):
            for group in groups:
                yield HostLabel(f"wazuh/group/{group}", "yes")


def discover_wazuh_agent(section):
    """Discover the Wazuh Agent service."""
    if section:
        yield Service()


def _parse_iso_datetime(dt_string):
    """Parse ISO datetime string to Unix timestamp."""
    if not dt_string:
        return None
    try:
        # Handle format: "2024-01-15T10:30:45Z" or "2024-01-15T10:30:45+00:00"
        dt_string = dt_string.replace("Z", "+00:00")
        dt = datetime.fromisoformat(dt_string)
        return dt.timestamp()
    except (ValueError, TypeError):
        return None


def check_wazuh_agent(params, section):
    """Check individual Wazuh agent status."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    agent_id = section.get("id", "unknown")
    name = section.get("name", "unknown")
    status = section.get("status", "unknown")
    version = section.get("version", "unknown")
    ip = section.get("ip", "unknown")
    manager = section.get("manager", "unknown")
    node_name = section.get("node_name", "")

    # Determine state based on agent status
    status_map = {
        "active": State.OK,
        "pending": State.WARN,
        "disconnected": State.WARN,
        "never_connected": State.WARN,
    }

    # Allow configuration of disconnected state
    disconnected_state = params.get("disconnected_state", "warn")
    if status == "disconnected":
        if disconnected_state == "crit":
            agent_state = State.CRIT
        else:
            agent_state = State.WARN
    else:
        agent_state = status_map.get(status, State.UNKNOWN)

    yield Result(
        state=agent_state,
        summary=f"Status: {status}",
    )

    yield Result(
        state=State.OK,
        summary=f"Version: {version}",
    )

    # Check keepalive age
    last_keepalive = section.get("last_keepalive", "")
    if last_keepalive:
        keepalive_ts = _parse_iso_datetime(last_keepalive)
        if keepalive_ts:
            keepalive_age = time.time() - keepalive_ts
            yield from check_levels(
                keepalive_age,
                levels_upper=params.get("levels_keepalive_age"),
                label="Last keepalive",
                render_func=render.timespan,
            )

    # Additional information
    info_parts = [f"ID: {agent_id}", f"IP: {ip}", f"Manager: {manager}"]
    if node_name:
        info_parts.append(f"Node: {node_name}")

    yield Result(
        state=State.OK,
        notice=", ".join(info_parts),
    )

    # OS information in details
    os_name = section.get("os_name", "")
    os_version = section.get("os_version", "")
    os_platform = section.get("os_platform", "")

    if os_name or os_version or os_platform:
        os_info = f"{os_name} {os_version}".strip()
        if os_platform:
            os_info = f"{os_info} ({os_platform})"
        yield Result(
            state=State.OK,
            notice=f"OS: {os_info}",
        )

    # Group membership in details
    groups = section.get("group", [])
    if groups:
        if isinstance(groups, list):
            group_str = ", ".join(groups)
        else:
            group_str = str(groups)
        yield Result(
            state=State.OK,
            notice=f"Groups: {group_str}",
        )

    # Registration date in details
    date_add = section.get("date_add", "")
    if date_add:
        yield Result(
            state=State.OK,
            notice=f"Registered: {date_add}",
        )


agent_section_wazuh_agent = AgentSection(
    name="wazuh_agent",
    parse_function=parse_wazuh_agent,
    host_label_function=host_label_wazuh_agent,
)


check_plugin_wazuh_agent = CheckPlugin(
    name="wazuh_agent",
    service_name="Wazuh Agent",
    discovery_function=discover_wazuh_agent,
    check_function=check_wazuh_agent,
    check_default_parameters={
        "disconnected_state": "warn",
        "levels_keepalive_age": ("fixed", (3600, 86400)),  # 1 hour, 24 hours
    },
    check_ruleset_name="wazuh_agent",
)
