#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Ruleset for Wazuh Special Agent"""

from cmk.rulesets.v1 import Title, Label, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    String,
    Integer,
    Password,
    BooleanChoice,
    DefaultValue,
    migrate_to_password,
)
from cmk.rulesets.v1.rule_specs import SpecialAgent, Topic


def _formspec():
    return Dictionary(
        title=Title("Wazuh SIEM/XDR Monitoring"),
        help_text=Help(
            "Configure monitoring of Wazuh Manager via REST API. "
            "This special agent connects to the Wazuh API (default port 55000) "
            "and monitors manager processes, cluster health, and agent statistics."
        ),
        elements={
            "port": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("API Port"),
                    help_text=Help("Wazuh API port (default: 55000)"),
                    prefill=DefaultValue(55000),
                ),
            ),
            "username": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("API Username"),
                    help_text=Help("Username for Wazuh API authentication"),
                    prefill=DefaultValue("wazuh"),
                ),
            ),
            "password": DictElement(
                required=True,
                parameter_form=Password(
                    title=Title("API Password"),
                    help_text=Help("Password for Wazuh API authentication"),
                    migrate=migrate_to_password,
                ),
            ),
            "no_cert_check": DictElement(
                required=False,
                parameter_form=BooleanChoice(
                    title=Title("Disable SSL certificate verification"),
                    help_text=Help(
                        "Skip SSL certificate validation. "
                        "Not recommended for production environments."
                    ),
                    prefill=DefaultValue(False),
                ),
            ),
            "timeout": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Connection timeout (seconds)"),
                    help_text=Help("Timeout for API connections in seconds"),
                    prefill=DefaultValue(30),
                ),
            ),
            "piggyback_agents": DictElement(
                required=False,
                parameter_form=BooleanChoice(
                    title=Title("Create piggyback data for disconnected agents"),
                    help_text=Help(
                        "Generate piggyback host data for agents that are not active "
                        "(disconnected, never connected, pending). "
                        "This creates separate hosts in CheckMK for these agents."
                    ),
                    prefill=DefaultValue(False),
                ),
            ),
            "piggyback_all_agents": DictElement(
                required=False,
                parameter_form=BooleanChoice(
                    title=Title("Include active agents in piggyback"),
                    help_text=Help(
                        "Also create piggyback data for active agents. "
                        "Warning: This can create many hosts in large environments!"
                    ),
                    prefill=DefaultValue(False),
                ),
            ),
        },
    )


rule_spec_wazuh = SpecialAgent(
    name="wazuh",
    title=Title("Wazuh SIEM/XDR"),
    topic=Topic.APPLICATIONS,
    parameter_form=_formspec,
)
