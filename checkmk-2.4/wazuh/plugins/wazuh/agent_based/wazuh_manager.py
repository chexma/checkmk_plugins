#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Manager Processes"""

import json
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
)


# Critical processes that must be running
DEFAULT_REQUIRED_PROCESSES = [
    "wazuh-analysisd",
    "wazuh-remoted",
    "wazuh-syscheckd",
    "wazuh-logcollector",
    "wazuh-modulesd",
    "wazuh-db",
    "wazuh-execd",
]

# Optional processes (can be stopped)
OPTIONAL_PROCESSES = {
    "wazuh-dbd",
    "wazuh-reportd",
    "wazuh-maild",
    "wazuh-agentlessd",
    "wazuh-integratord",
    "wazuh-csyslogd",
    "wazuh-monitord",
    "wazuh-authd",
    "wazuh-clusterd",
    "wazuh-apid",
}


def parse_wazuh_manager(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_manager(section):
    """Discover the Wazuh Manager service."""
    if section:
        yield Service()


def check_wazuh_manager(params, section):
    """Check Wazuh Manager process status."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    running = []
    stopped = []
    failed_required = []

    # Get required processes from params or use defaults
    required = set(params.get("required_processes", DEFAULT_REQUIRED_PROCESSES))

    for process, status in section.items():
        if status == "running":
            running.append(process)
        else:
            stopped.append(process)
            if process in required:
                failed_required.append(process)

    # Determine overall status
    if failed_required:
        state = State.CRIT
        summary = f"{len(failed_required)} required process(es) stopped"
    else:
        state = State.OK
        summary = f"{len(running)} processes running"

    yield Result(state=state, summary=summary)

    # Show failed required processes
    if failed_required:
        yield Result(
            state=State.CRIT,
            summary=f"Stopped required: {', '.join(sorted(failed_required))}",
        )

    # Show stopped optional processes (informational)
    optional_stopped = [p for p in stopped if p not in required]
    if optional_stopped:
        yield Result(
            state=State.OK,
            notice=f"Stopped optional: {', '.join(sorted(optional_stopped))}",
        )

    # Detailed list of all processes
    details_lines = ["Process Status:"]
    for process in sorted(section.keys()):
        status = section[process]
        marker = "[OK]" if status == "running" else "[STOPPED]"
        required_marker = " (required)" if process in required else ""
        details_lines.append(f"  {marker} {process}{required_marker}")

    yield Result(
        state=State.OK,
        notice="\n".join(details_lines),
    )


agent_section_wazuh_manager = AgentSection(
    name="wazuh_manager",
    parse_function=parse_wazuh_manager,
)


check_plugin_wazuh_manager = CheckPlugin(
    name="wazuh_manager",
    service_name="Wazuh Manager",
    discovery_function=discover_wazuh_manager,
    check_function=check_wazuh_manager,
    check_default_parameters={
        "required_processes": DEFAULT_REQUIRED_PROCESSES,
    },
    check_ruleset_name="wazuh_manager",
)
