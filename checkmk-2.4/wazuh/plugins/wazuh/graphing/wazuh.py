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
