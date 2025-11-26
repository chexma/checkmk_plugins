#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Cluster Status"""

import json
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
    Metric,
)


def parse_wazuh_cluster(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_cluster(section):
    """Discover the Wazuh Cluster service."""
    if section:
        yield Service()


def check_wazuh_cluster(params, section):
    """Check Wazuh Cluster status."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    enabled = section.get("enabled", False)
    running = section.get("running", False)
    node_name = section.get("node_name", "unknown")
    node_type = section.get("node_type", "unknown")

    # Cluster not enabled - single node mode
    if not enabled:
        yield Result(
            state=State.OK,
            summary="Cluster disabled (single-node mode)",
        )
        yield Result(
            state=State.OK,
            summary=f"Node: {node_name} ({node_type})",
        )
        return

    # Cluster enabled but not running
    if not running:
        yield Result(
            state=State.CRIT,
            summary="Cluster enabled but not running!",
        )
        yield Result(
            state=State.OK,
            summary=f"Node: {node_name} ({node_type})",
        )
        return

    # Cluster enabled and running
    yield Result(
        state=State.OK,
        summary="Cluster running",
    )
    yield Result(
        state=State.OK,
        summary=f"This node: {node_name} ({node_type})",
    )

    # Check cluster nodes
    nodes = section.get("nodes", [])
    if nodes:
        num_nodes = len(nodes)
        expected_nodes = params.get("expected_nodes")

        # Check node count
        if expected_nodes is not None and num_nodes < expected_nodes:
            yield Result(
                state=State.WARN,
                summary=f"Only {num_nodes}/{expected_nodes} nodes available",
            )
        else:
            yield Result(
                state=State.OK,
                summary=f"{num_nodes} node(s) in cluster",
            )

        yield Metric("wazuh_cluster_nodes", num_nodes)

        # Check each node
        sync_status = params.get("sync_status", "warn")
        total_active_agents = 0
        sync_issues = []

        for node in nodes:
            name = node.get("name", "unknown")
            ntype = node.get("type", "unknown")
            version = node.get("version", "unknown")
            ip = node.get("ip", "unknown")
            n_agents = node.get("n_active_agents", 0)
            total_active_agents += n_agents

            # Check sync status
            if not node.get("sync_integrity_free", True):
                sync_issues.append(f"{name}: integrity sync in progress")
            if not node.get("sync_extravalid_free", True):
                sync_issues.append(f"{name}: extra-valid sync in progress")

            # Node details
            yield Result(
                state=State.OK,
                notice=f"Node {name}: type={ntype}, version={version}, ip={ip}, agents={n_agents}",
            )

        yield Metric("wazuh_cluster_active_agents", total_active_agents)

        # Report sync issues based on configuration
        if sync_issues:
            if sync_status == "crit":
                state = State.CRIT
            elif sync_status == "warn":
                state = State.WARN
            else:
                state = State.OK

            if sync_status != "ignore":
                yield Result(
                    state=state,
                    summary=f"Sync issues: {', '.join(sync_issues)}",
                )


agent_section_wazuh_cluster = AgentSection(
    name="wazuh_cluster",
    parse_function=parse_wazuh_cluster,
)


check_plugin_wazuh_cluster = CheckPlugin(
    name="wazuh_cluster",
    service_name="Wazuh Cluster",
    discovery_function=discover_wazuh_cluster,
    check_function=check_wazuh_cluster,
    check_default_parameters={
        "sync_status": "warn",
    },
    check_ruleset_name="wazuh_cluster",
)
