#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Plugin: Wazuh Ruleset Status"""

import json
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    Service,
    Result,
    State,
    Metric,
)


def parse_wazuh_ruleset(string_table):
    """Parse JSON output from special agent."""
    if not string_table:
        return None
    try:
        return json.loads(string_table[0][0])
    except (json.JSONDecodeError, IndexError):
        return None


def discover_wazuh_ruleset(section):
    """Discover the Wazuh Ruleset service."""
    if section:
        yield Service()


def check_wazuh_ruleset(params, section):
    """Check Wazuh ruleset status."""
    if not section:
        yield Result(state=State.UNKNOWN, summary="No data from Wazuh API")
        return

    rules_total = section.get("rules_total", 0)
    decoders_total = section.get("decoders_total", 0)

    yield Result(
        state=State.OK,
        summary=f"Rules: {rules_total}, Decoders: {decoders_total}",
    )

    yield Metric("wazuh_rules_total", rules_total)
    yield Metric("wazuh_decoders_total", decoders_total)

    # Check minimum rules
    min_rules = params.get("min_rules")
    if min_rules and rules_total < min_rules:
        yield Result(
            state=State.WARN,
            summary=f"Rules below minimum ({rules_total} < {min_rules})",
        )

    # Check minimum decoders
    min_decoders = params.get("min_decoders")
    if min_decoders and decoders_total < min_decoders:
        yield Result(
            state=State.WARN,
            summary=f"Decoders below minimum ({decoders_total} < {min_decoders})",
        )


agent_section_wazuh_ruleset = AgentSection(
    name="wazuh_ruleset",
    parse_function=parse_wazuh_ruleset,
)


check_plugin_wazuh_ruleset = CheckPlugin(
    name="wazuh_ruleset",
    service_name="Wazuh Ruleset",
    discovery_function=discover_wazuh_ruleset,
    check_function=check_wazuh_ruleset,
    check_default_parameters={},
    check_ruleset_name="wazuh_ruleset",
)
