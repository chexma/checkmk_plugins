#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh SCA (Security Configuration Assessment) - Piggyback"""

import json
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


def parse_wazuh_sca(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_sca(section):
    """Discover SCA policy services."""
    if section:
        policies = section.get("policies", [])
        for policy in policies:
            policy_id = policy.get("policy_id")
            if policy_id:
                yield Service(item=policy_id)


def check_wazuh_sca(item, params, section):
    """Check Wazuh SCA policy status."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No SCA data")
        return

    policies = section.get("policies", [])
    policy = None
    for p in policies:
        if p.get("policy_id") == item:
            policy = p
            break

    if not policy:
        yield Result(state=State.UNKNOWN, summary=f"Policy {item} not found")
        return

    name = policy.get("name", item)
    passed = policy.get("pass", 0)
    failed = policy.get("fail", 0)
    invalid = policy.get("invalid", 0)
    total = policy.get("total_checks", passed + failed + invalid)
    score = policy.get("score", 0)

    # Main summary with score
    yield Result(
        state=State.OK,
        summary=f"{name}: Score {score}%",
    )

    # Score metric with levels
    yield from check_levels(
        score,
        levels_lower=params.get("score_levels"),
        metric_name="wazuh_sca_score",
        label="Score",
        render_func=render.percent,
    )

    # Failed checks with levels
    yield from check_levels(
        failed,
        levels_upper=params.get("failed_levels"),
        metric_name="wazuh_sca_failed",
        label="Failed",
        render_func=lambda x: str(int(x)),
    )

    yield Metric("wazuh_sca_passed", passed)
    yield Metric("wazuh_sca_total", total)
    yield Metric("wazuh_sca_invalid", invalid)

    # Details
    yield Result(
        state=State.OK,
        notice=f"Checks: {passed} passed, {failed} failed, {invalid} invalid (total: {total})",
    )

    # Last scan info
    end_scan = policy.get("end_scan")
    if end_scan:
        yield Result(
            state=State.OK,
            notice=f"Last scan: {end_scan}",
        )


agent_section_wazuh_sca = AgentSection(
    name="wazuh_sca",
    parse_function=parse_wazuh_sca,
)


check_plugin_wazuh_sca = CheckPlugin(
    name="wazuh_sca",
    service_name="Wazuh SCA %s",
    discovery_function=discover_wazuh_sca,
    check_function=check_wazuh_sca,
    check_default_parameters={
        "score_levels": ("fixed", (70.0, 50.0)),  # WARN below 70%, CRIT below 50%
        "failed_levels": ("fixed", (10, 25)),
    },
    check_ruleset_name="wazuh_sca",
)
