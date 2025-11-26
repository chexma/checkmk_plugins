#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Daemon Statistics"""

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


def parse_wazuh_daemon_stats(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_daemon_stats(section):
    """Discover daemon stats services."""
    if section:
        for daemon_name in section:
            yield Service(item=daemon_name)


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


def check_wazuh_daemon_stats(item, params, section):
    """Check Wazuh daemon statistics."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    daemon = section.get(item)
    if not daemon:
        yield Result(state=State.UNKNOWN, summary=f"Daemon {item} not found")
        return

    metrics = daemon.get("metrics", {})
    uptime_str = daemon.get("uptime", "")

    # Calculate uptime
    uptime_ts = _parse_iso_datetime(uptime_str)
    if uptime_ts:
        uptime_seconds = time.time() - uptime_ts
        yield Result(
            state=State.OK,
            summary=f"Uptime: {render.timespan(uptime_seconds)}",
        )
        yield Metric(f"wazuh_{item.replace('-', '_')}_uptime", uptime_seconds)

    # Daemon-specific metrics
    if item == "wazuh-remoted":
        _check_remoted(metrics, params)
        tcp_sessions = metrics.get("tcp_sessions", 0)
        yield Result(state=State.OK, summary=f"TCP sessions: {tcp_sessions}")
        yield Metric("wazuh_remoted_tcp_sessions", tcp_sessions)

        bytes_recv = metrics.get("bytes", {}).get("received", 0)
        bytes_sent = metrics.get("bytes", {}).get("sent", 0)
        yield Metric("wazuh_remoted_bytes_received", bytes_recv)
        yield Metric("wazuh_remoted_bytes_sent", bytes_sent)

        queue_usage = metrics.get("queues", {}).get("received", {}).get("usage", 0)
        yield from check_levels(
            queue_usage,
            levels_upper=params.get("queue_usage_levels"),
            metric_name="wazuh_remoted_queue_usage",
            label="Queue usage",
            render_func=render.percent,
        )

    elif item == "wazuh-analysisd":
        events = metrics.get("events", {})
        processed = events.get("processed", 0)
        received = events.get("received", 0)

        yield Result(state=State.OK, summary=f"Events: {received} received, {processed} processed")
        yield Metric("wazuh_analysisd_events_received", received)
        yield Metric("wazuh_analysisd_events_processed", processed)

        # Alerts written
        written = events.get("written_breakdown", {})
        alerts = written.get("alerts", 0)
        yield Metric("wazuh_analysisd_alerts_written", alerts)

        # Check queue usage across all queues
        queues = metrics.get("queues", {})
        max_queue_usage = 0
        for queue_name, queue_data in queues.items():
            usage = queue_data.get("usage", 0)
            if usage > max_queue_usage:
                max_queue_usage = usage

        yield from check_levels(
            max_queue_usage,
            levels_upper=params.get("queue_usage_levels"),
            metric_name="wazuh_analysisd_queue_usage",
            label="Max queue usage",
            render_func=render.percent,
        )

    elif item == "wazuh-db":
        queries = metrics.get("queries", {})
        received = queries.get("received", 0)
        yield Result(state=State.OK, summary=f"Queries: {received}")
        yield Metric("wazuh_db_queries", received)

        # Execution time
        exec_time = queries.get("time", {}).get("execution", 0)
        yield Metric("wazuh_db_execution_time", exec_time)


def _check_remoted(metrics, params):
    """Additional checks for wazuh-remoted."""
    pass  # Placeholder for additional checks


agent_section_wazuh_daemon_stats = AgentSection(
    name="wazuh_daemon_stats",
    parse_function=parse_wazuh_daemon_stats,
)


check_plugin_wazuh_daemon_stats = CheckPlugin(
    name="wazuh_daemon_stats",
    service_name="Wazuh Daemon %s",
    discovery_function=discover_wazuh_daemon_stats,
    check_function=check_wazuh_daemon_stats,
    check_default_parameters={
        "queue_usage_levels": ("fixed", (70.0, 90.0)),
    },
    check_ruleset_name="wazuh_daemon_stats",
)
