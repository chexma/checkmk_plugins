#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Metrics, Graphs and Perfometers for Wazuh"""

from cmk.graphing.v1 import Title
from cmk.graphing.v1.metrics import (
    Metric,
    Color,
    Unit,
    DecimalNotation,
)
from cmk.graphing.v1.graphs import Graph, MinimalRange
from cmk.graphing.v1.perfometers import Perfometer, FocusRange, Closed, Open


# ============================================================================
# UNITS
# ============================================================================

UNIT_COUNT = Unit(DecimalNotation(""))
UNIT_PERCENT = Unit(DecimalNotation("%"))


# ============================================================================
# METRICS - Agent Statistics
# ============================================================================

metric_wazuh_agents_total = Metric(
    name="wazuh_agents_total",
    title=Title("Total Agents"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_wazuh_agents_active = Metric(
    name="wazuh_agents_active",
    title=Title("Active Agents"),
    unit=UNIT_COUNT,
    color=Color.GREEN,
)

metric_wazuh_agents_disconnected = Metric(
    name="wazuh_agents_disconnected",
    title=Title("Disconnected Agents"),
    unit=UNIT_COUNT,
    color=Color.ORANGE,
)

metric_wazuh_agents_disconnected_pct = Metric(
    name="wazuh_agents_disconnected_pct",
    title=Title("Disconnected Agents Percentage"),
    unit=UNIT_PERCENT,
    color=Color.ORANGE,
)

metric_wazuh_agents_never_connected = Metric(
    name="wazuh_agents_never_connected",
    title=Title("Never Connected Agents"),
    unit=UNIT_COUNT,
    color=Color.PURPLE,
)

metric_wazuh_agents_pending = Metric(
    name="wazuh_agents_pending",
    title=Title("Pending Agents"),
    unit=UNIT_COUNT,
    color=Color.YELLOW,
)


# ============================================================================
# METRICS - Cluster
# ============================================================================

metric_wazuh_cluster_nodes = Metric(
    name="wazuh_cluster_nodes",
    title=Title("Cluster Nodes"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_wazuh_cluster_active_agents = Metric(
    name="wazuh_cluster_active_agents",
    title=Title("Active Agents in Cluster"),
    unit=UNIT_COUNT,
    color=Color.GREEN,
)


# ============================================================================
# GRAPHS
# ============================================================================

graph_wazuh_agents_status = Graph(
    name="wazuh_agents_status",
    title=Title("Wazuh Agent Status"),
    compound_lines=[
        "wazuh_agents_active",
        "wazuh_agents_disconnected",
        "wazuh_agents_never_connected",
        "wazuh_agents_pending",
    ],
    simple_lines=[
        "wazuh_agents_total",
    ],
    minimal_range=MinimalRange(0, 10),
)

graph_wazuh_agents_health = Graph(
    name="wazuh_agents_health",
    title=Title("Wazuh Agent Health"),
    simple_lines=[
        "wazuh_agents_active",
        "wazuh_agents_disconnected",
    ],
    minimal_range=MinimalRange(0, 10),
)

graph_wazuh_cluster = Graph(
    name="wazuh_cluster",
    title=Title("Wazuh Cluster"),
    simple_lines=[
        "wazuh_cluster_nodes",
        "wazuh_cluster_active_agents",
    ],
    minimal_range=MinimalRange(0, 5),
)


# ============================================================================
# PERFOMETERS
# ============================================================================

perfometer_wazuh_agents = Perfometer(
    name="wazuh_agents",
    focus_range=FocusRange(Closed(0), Open("wazuh_agents_total")),
    segments=["wazuh_agents_active"],
)


# ============================================================================
# METRICS - Daemon Statistics
# ============================================================================

UNIT_SECONDS = Unit(DecimalNotation("s"))
UNIT_BYTES = Unit(DecimalNotation("B"))

metric_wazuh_remoted_tcp_sessions = Metric(
    name="wazuh_remoted_tcp_sessions",
    title=Title("TCP Sessions"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_wazuh_remoted_bytes_received = Metric(
    name="wazuh_remoted_bytes_received",
    title=Title("Bytes Received"),
    unit=UNIT_BYTES,
    color=Color.GREEN,
)

metric_wazuh_remoted_bytes_sent = Metric(
    name="wazuh_remoted_bytes_sent",
    title=Title("Bytes Sent"),
    unit=UNIT_BYTES,
    color=Color.BLUE,
)

metric_wazuh_remoted_queue_usage = Metric(
    name="wazuh_remoted_queue_usage",
    title=Title("Remoted Queue Usage"),
    unit=UNIT_PERCENT,
    color=Color.ORANGE,
)

metric_wazuh_analysisd_events_received = Metric(
    name="wazuh_analysisd_events_received",
    title=Title("Events Received"),
    unit=UNIT_COUNT,
    color=Color.GREEN,
)

metric_wazuh_analysisd_events_processed = Metric(
    name="wazuh_analysisd_events_processed",
    title=Title("Events Processed"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_wazuh_analysisd_alerts_written = Metric(
    name="wazuh_analysisd_alerts_written",
    title=Title("Alerts Written"),
    unit=UNIT_COUNT,
    color=Color.ORANGE,
)

metric_wazuh_analysisd_queue_usage = Metric(
    name="wazuh_analysisd_queue_usage",
    title=Title("Analysisd Queue Usage"),
    unit=UNIT_PERCENT,
    color=Color.ORANGE,
)

metric_wazuh_db_queries = Metric(
    name="wazuh_db_queries",
    title=Title("Database Queries"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_wazuh_db_execution_time = Metric(
    name="wazuh_db_execution_time",
    title=Title("DB Execution Time"),
    unit=UNIT_SECONDS,
    color=Color.GREEN,
)


# ============================================================================
# METRICS - Logs
# ============================================================================

metric_wazuh_log_errors = Metric(
    name="wazuh_log_errors",
    title=Title("Log Errors"),
    unit=UNIT_COUNT,
    color=Color.ORANGE,
)

metric_wazuh_log_warnings = Metric(
    name="wazuh_log_warnings",
    title=Title("Log Warnings"),
    unit=UNIT_COUNT,
    color=Color.YELLOW,
)

metric_wazuh_log_critical = Metric(
    name="wazuh_log_critical",
    title=Title("Log Critical"),
    unit=UNIT_COUNT,
    color=Color.RED,
)

metric_wazuh_log_info = Metric(
    name="wazuh_log_info",
    title=Title("Log Info"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)


# ============================================================================
# METRICS - Ruleset
# ============================================================================

metric_wazuh_rules_total = Metric(
    name="wazuh_rules_total",
    title=Title("Total Rules"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_wazuh_decoders_total = Metric(
    name="wazuh_decoders_total",
    title=Title("Total Decoders"),
    unit=UNIT_COUNT,
    color=Color.GREEN,
)


# ============================================================================
# METRICS - Outdated Agents
# ============================================================================

metric_wazuh_agents_outdated = Metric(
    name="wazuh_agents_outdated",
    title=Title("Outdated Agents"),
    unit=UNIT_COUNT,
    color=Color.ORANGE,
)


# ============================================================================
# METRICS - Tasks
# ============================================================================

metric_wazuh_tasks_total = Metric(
    name="wazuh_tasks_total",
    title=Title("Total Tasks"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_wazuh_tasks_in_progress = Metric(
    name="wazuh_tasks_in_progress",
    title=Title("Tasks In Progress"),
    unit=UNIT_COUNT,
    color=Color.GREEN,
)

metric_wazuh_tasks_done = Metric(
    name="wazuh_tasks_done",
    title=Title("Tasks Done"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)

metric_wazuh_tasks_pending = Metric(
    name="wazuh_tasks_pending",
    title=Title("Tasks Pending"),
    unit=UNIT_COUNT,
    color=Color.YELLOW,
)

metric_wazuh_tasks_failed = Metric(
    name="wazuh_tasks_failed",
    title=Title("Tasks Failed"),
    unit=UNIT_COUNT,
    color=Color.RED,
)


# ============================================================================
# METRICS - SCA (Security Configuration Assessment)
# ============================================================================

metric_wazuh_sca_score = Metric(
    name="wazuh_sca_score",
    title=Title("SCA Score"),
    unit=UNIT_PERCENT,
    color=Color.GREEN,
)

metric_wazuh_sca_passed = Metric(
    name="wazuh_sca_passed",
    title=Title("SCA Passed Checks"),
    unit=UNIT_COUNT,
    color=Color.GREEN,
)

metric_wazuh_sca_failed = Metric(
    name="wazuh_sca_failed",
    title=Title("SCA Failed Checks"),
    unit=UNIT_COUNT,
    color=Color.RED,
)

metric_wazuh_sca_invalid = Metric(
    name="wazuh_sca_invalid",
    title=Title("SCA Invalid Checks"),
    unit=UNIT_COUNT,
    color=Color.ORANGE,
)

metric_wazuh_sca_total = Metric(
    name="wazuh_sca_total",
    title=Title("SCA Total Checks"),
    unit=UNIT_COUNT,
    color=Color.BLUE,
)


# ============================================================================
# METRICS - Syscheck
# ============================================================================

metric_wazuh_syscheck_age = Metric(
    name="wazuh_syscheck_age",
    title=Title("Syscheck Scan Age"),
    unit=UNIT_SECONDS,
    color=Color.BLUE,
)

metric_wazuh_syscheck_scan_age = Metric(
    name="wazuh_syscheck_scan_age",
    title=Title("Syscheck Scan Age"),
    unit=UNIT_SECONDS,
    color=Color.ORANGE,
)


# ============================================================================
# GRAPHS - Daemon Statistics
# ============================================================================

graph_wazuh_analysisd_events = Graph(
    name="wazuh_analysisd_events",
    title=Title("Wazuh Analysis Events"),
    simple_lines=[
        "wazuh_analysisd_events_received",
        "wazuh_analysisd_events_processed",
        "wazuh_analysisd_alerts_written",
    ],
    minimal_range=MinimalRange(0, 100),
)

graph_wazuh_remoted_bytes = Graph(
    name="wazuh_remoted_bytes",
    title=Title("Wazuh Remoted Traffic"),
    simple_lines=[
        "wazuh_remoted_bytes_received",
        "wazuh_remoted_bytes_sent",
    ],
    minimal_range=MinimalRange(0, 1000),
)


# ============================================================================
# GRAPHS - Logs
# ============================================================================

graph_wazuh_logs = Graph(
    name="wazuh_logs",
    title=Title("Wazuh Log Messages"),
    compound_lines=[
        "wazuh_log_critical",
        "wazuh_log_errors",
        "wazuh_log_warnings",
    ],
    simple_lines=[
        "wazuh_log_info",
    ],
    minimal_range=MinimalRange(0, 10),
)


# ============================================================================
# GRAPHS - Ruleset
# ============================================================================

graph_wazuh_ruleset = Graph(
    name="wazuh_ruleset",
    title=Title("Wazuh Ruleset"),
    simple_lines=[
        "wazuh_rules_total",
        "wazuh_decoders_total",
    ],
    minimal_range=MinimalRange(0, 100),
)


# ============================================================================
# GRAPHS - Tasks
# ============================================================================

graph_wazuh_tasks = Graph(
    name="wazuh_tasks",
    title=Title("Wazuh Tasks"),
    compound_lines=[
        "wazuh_tasks_in_progress",
        "wazuh_tasks_pending",
        "wazuh_tasks_done",
        "wazuh_tasks_failed",
    ],
    simple_lines=[
        "wazuh_tasks_total",
    ],
    minimal_range=MinimalRange(0, 10),
)


# ============================================================================
# GRAPHS - SCA
# ============================================================================

graph_wazuh_sca = Graph(
    name="wazuh_sca",
    title=Title("Wazuh SCA Results"),
    compound_lines=[
        "wazuh_sca_passed",
        "wazuh_sca_failed",
        "wazuh_sca_invalid",
    ],
    simple_lines=[
        "wazuh_sca_total",
    ],
    minimal_range=MinimalRange(0, 50),
)


# ============================================================================
# PERFOMETERS - Additional
# ============================================================================

perfometer_wazuh_sca = Perfometer(
    name="wazuh_sca",
    focus_range=FocusRange(Closed(0), Closed(100)),
    segments=["wazuh_sca_score"],
)

perfometer_wazuh_queue_usage = Perfometer(
    name="wazuh_queue_usage",
    focus_range=FocusRange(Closed(0), Closed(100)),
    segments=["wazuh_analysisd_queue_usage"],
)
