#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Logs Summary"""

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


def parse_wazuh_logs(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_logs(section):
    """Discover the Wazuh Logs service."""
    if section:
        yield Service()


def check_wazuh_logs(params, section):
    """Check Wazuh logs summary."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    totals = section.get("totals", {})
    components = section.get("components", {})

    errors = totals.get("error", 0)
    warnings = totals.get("warning", 0)
    critical = totals.get("critical", 0)
    info = totals.get("info", 0)

    # Critical errors
    if critical > 0:
        yield Result(
            state=State.CRIT,
            summary=f"Critical: {critical}",
        )
    else:
        yield Result(
            state=State.OK,
            summary="No critical errors",
        )

    # Errors with levels
    yield from check_levels(
        errors,
        levels_upper=params.get("error_levels"),
        metric_name="wazuh_log_errors",
        label="Errors",
        render_func=lambda x: str(int(x)),
    )

    # Warnings with levels
    yield from check_levels(
        warnings,
        levels_upper=params.get("warning_levels"),
        metric_name="wazuh_log_warnings",
        label="Warnings",
        render_func=lambda x: str(int(x)),
    )

    yield Metric("wazuh_log_critical", critical)
    yield Metric("wazuh_log_info", info)

    # List components with errors or warnings
    problem_components = []
    for comp_name, stats in components.items():
        comp_errors = stats.get("error", 0)
        comp_warnings = stats.get("warning", 0)
        comp_critical = stats.get("critical", 0)
        if comp_errors > 0 or comp_warnings > 0 or comp_critical > 0:
            problem_components.append(
                f"{comp_name}: {comp_critical}C/{comp_errors}E/{comp_warnings}W"
            )

    if problem_components:
        yield Result(
            state=State.OK,
            notice="Components with issues: " + ", ".join(problem_components[:5]),
        )


agent_section_wazuh_logs = AgentSection(
    name="wazuh_logs",
    parse_function=parse_wazuh_logs,
)


check_plugin_wazuh_logs = CheckPlugin(
    name="wazuh_logs",
    service_name="Wazuh Logs",
    discovery_function=discover_wazuh_logs,
    check_function=check_wazuh_logs,
    check_default_parameters={
        "error_levels": ("fixed", (1, 10)),
        "warning_levels": ("fixed", (10, 50)),
    },
    check_ruleset_name="wazuh_logs",
)
