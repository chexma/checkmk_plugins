#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh API Health"""

import json
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
)


def parse_wazuh_api(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_api(section):
    """Discover the Wazuh API service."""
    if section:
        yield Service()


def check_wazuh_api(section):
    """Check Wazuh API availability and version."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    api_version = section.get("api_version", "unknown")
    manager_version = section.get("manager_version", "unknown")
    hostname = section.get("hostname", "unknown")
    manager_name = section.get("manager_name", "unknown")
    manager_type = section.get("manager_type", "server")

    yield Result(
        state=State.OK,
        summary=f"API v{api_version}, Manager v{manager_version}",
    )

    yield Result(
        state=State.OK,
        summary=f"Host: {hostname}",
    )

    # Additional details
    details_parts = [
        f"Manager name: {manager_name}",
        f"Manager type: {manager_type}",
    ]

    if section.get("manager_path"):
        details_parts.append(f"Installation path: {section['manager_path']}")

    if section.get("manager_tz_name"):
        details_parts.append(f"Timezone: {section['manager_tz_name']} ({section.get('manager_tz_offset', '')})")

    if section.get("timestamp"):
        details_parts.append(f"API timestamp: {section['timestamp']}")

    yield Result(
        state=State.OK,
        notice="\n".join(details_parts),
    )


agent_section_wazuh_api = AgentSection(
    name="wazuh_api",
    parse_function=parse_wazuh_api,
)


check_plugin_wazuh_api = CheckPlugin(
    name="wazuh_api",
    service_name="Wazuh API",
    discovery_function=discover_wazuh_api,
    check_function=check_wazuh_api,
)
