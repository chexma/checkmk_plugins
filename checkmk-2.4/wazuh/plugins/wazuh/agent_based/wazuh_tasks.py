#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Tasks"""

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


def parse_wazuh_tasks(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_tasks(section):
    """Discover the Wazuh Tasks service."""
    if section:
        yield Service()


def check_wazuh_tasks(params, section):
    """Check Wazuh tasks status."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    total = section.get("total", 0)
    by_status = section.get("by_status", {})

    if total == 0:
        yield Result(state=State.OK, summary="No tasks")
        return

    # Count by status
    in_progress = by_status.get("In progress", 0)
    failed = by_status.get("Failed", 0)
    done = by_status.get("Done", 0)
    pending = by_status.get("Pending", 0)

    yield Result(
        state=State.OK,
        summary=f"Tasks: {total} total",
    )

    yield Metric("wazuh_tasks_total", total)
    yield Metric("wazuh_tasks_in_progress", in_progress)
    yield Metric("wazuh_tasks_done", done)
    yield Metric("wazuh_tasks_pending", pending)

    # Check failed tasks
    yield from check_levels(
        failed,
        levels_upper=params.get("failed_levels"),
        metric_name="wazuh_tasks_failed",
        label="Failed",
        render_func=lambda x: str(int(x)),
    )

    # Summary of status
    status_parts = []
    if in_progress > 0:
        status_parts.append(f"{in_progress} in progress")
    if pending > 0:
        status_parts.append(f"{pending} pending")
    if done > 0:
        status_parts.append(f"{done} done")
    if failed > 0:
        status_parts.append(f"{failed} failed")

    if status_parts:
        yield Result(
            state=State.OK,
            notice=", ".join(status_parts),
        )


agent_section_wazuh_tasks = AgentSection(
    name="wazuh_tasks",
    parse_function=parse_wazuh_tasks,
)


check_plugin_wazuh_tasks = CheckPlugin(
    name="wazuh_tasks",
    service_name="Wazuh Tasks",
    discovery_function=discover_wazuh_tasks,
    check_function=check_wazuh_tasks,
    check_default_parameters={
        "failed_levels": ("fixed", (1, 5)),
    },
    check_ruleset_name="wazuh_tasks",
)
