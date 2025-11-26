#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Syscheck (File Integrity Monitoring) - Piggyback"""

import json
import time
from datetime import datetime
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


def parse_wazuh_syscheck(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_syscheck(section):
    """Discover the Wazuh Syscheck service."""
    if section:
        yield Service()


def _parse_iso_datetime(dt_string):
    """Parse ISO datetime string to Unix timestamp."""
    if not dt_string:
        return None
    try:
        dt_string = dt_string.replace("Z", "+00:00")
        dt = datetime.fromisoformat(dt_string)
        return dt.timestamp()
    except (ValueError, TypeError):
        return None


def check_wazuh_syscheck(params, section):
    """Check Wazuh syscheck status."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No syscheck data")
        return

    start_time = section.get("start")
    end_time = section.get("end")

    # Check if scan is running
    if start_time and not end_time:
        yield Result(
            state=State.OK,
            summary="Scan in progress",
        )
        yield Result(
            state=State.OK,
            notice=f"Started: {start_time}",
        )
        return

    # Show last scan time
    if end_time:
        end_ts = _parse_iso_datetime(end_time)
        if end_ts:
            age_seconds = time.time() - end_ts
            yield Result(
                state=State.OK,
                summary=f"Last scan: {render.timespan(age_seconds)} ago",
            )
            yield Metric("wazuh_syscheck_age", age_seconds)

            # Check scan age
            yield from check_levels(
                age_seconds,
                levels_upper=params.get("scan_age_levels"),
                metric_name="wazuh_syscheck_scan_age",
                label="Scan age",
                render_func=render.timespan,
            )
        else:
            yield Result(
                state=State.OK,
                summary=f"Last scan: {end_time}",
            )
    else:
        yield Result(
            state=State.WARN,
            summary="No scan completed yet",
        )


agent_section_wazuh_syscheck = AgentSection(
    name="wazuh_syscheck",
    parse_function=parse_wazuh_syscheck,
)


check_plugin_wazuh_syscheck = CheckPlugin(
    name="wazuh_syscheck",
    service_name="Wazuh Syscheck",
    discovery_function=discover_wazuh_syscheck,
    check_function=check_wazuh_syscheck,
    check_default_parameters={
        "scan_age_levels": ("fixed", (86400.0, 172800.0)),  # 1 day, 2 days
    },
    check_ruleset_name="wazuh_syscheck",
)
