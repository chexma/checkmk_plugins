#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Check Parameter Rulesets for Wazuh"""

from cmk.rulesets.v1 import Title, Help
from cmk.rulesets.v1.form_specs import (
    Dictionary,
    DictElement,
    Float,
    Integer,
    SimpleLevels,
    LevelDirection,
    DefaultValue,
    List,
    String,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


# ============================================================================
# Wazuh Agents Summary
# ============================================================================

def _wazuh_agents_form():
    return Dictionary(
        title=Title("Wazuh Agents Thresholds"),
        help_text=Help(
            "Configure thresholds for monitoring Wazuh agent statistics. "
            "You can set warning and critical levels for disconnected, "
            "never connected, and pending agents."
        ),
        elements={
            "levels_disconnected": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Disconnected agents"),
                    help_text=Help("Number of disconnected agents"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(1, 5)),
                ),
            ),
            "levels_disconnected_percent": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Disconnected agents (percentage)"),
                    help_text=Help("Percentage of disconnected agents"),
                    form_spec_template=Float(unit_symbol="%"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(5.0, 10.0)),
                ),
            ),
            "levels_never_connected": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Never connected agents"),
                    help_text=Help("Number of agents that have never connected"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(5, 10)),
                ),
            ),
            "levels_pending": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Pending agents"),
                    help_text=Help("Number of agents pending registration"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(10, 20)),
                ),
            ),
        },
    )


rule_spec_wazuh_agents = CheckParameters(
    name="wazuh_agents",
    title=Title("Wazuh Agents"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_agents_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Manager
# ============================================================================

def _wazuh_manager_form():
    return Dictionary(
        title=Title("Wazuh Manager Settings"),
        help_text=Help(
            "Configure which Wazuh Manager processes are required to be running. "
            "By default, critical processes like wazuh-analysisd, wazuh-remoted, "
            "wazuh-syscheckd, etc. are required."
        ),
        elements={
            "required_processes": DictElement(
                required=False,
                parameter_form=List(
                    title=Title("Required processes"),
                    help_text=Help(
                        "List of Wazuh processes that must be running. "
                        "If any of these is stopped, the check will go CRITICAL."
                    ),
                    element_template=String(title=Title("Process name")),
                ),
            ),
        },
    )


rule_spec_wazuh_manager = CheckParameters(
    name="wazuh_manager",
    title=Title("Wazuh Manager"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_manager_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Cluster
# ============================================================================

def _wazuh_cluster_form():
    return Dictionary(
        title=Title("Wazuh Cluster Settings"),
        help_text=Help(
            "Configure thresholds for Wazuh cluster monitoring."
        ),
        elements={
            "expected_nodes": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Expected number of cluster nodes"),
                    help_text=Help(
                        "The expected number of nodes in the cluster. "
                        "If fewer nodes are available, the check will alert."
                    ),
                ),
            ),
            "sync_status": DictElement(
                required=False,
                parameter_form=SingleChoice(
                    title=Title("Sync status check"),
                    help_text=Help("How to handle sync status issues"),
                    elements=[
                        SingleChoiceElement(name="warn", title=Title("WARN on sync issues")),
                        SingleChoiceElement(name="crit", title=Title("CRIT on sync issues")),
                        SingleChoiceElement(name="ignore", title=Title("Ignore sync issues")),
                    ],
                    prefill=DefaultValue("warn"),
                ),
            ),
        },
    )


rule_spec_wazuh_cluster = CheckParameters(
    name="wazuh_cluster",
    title=Title("Wazuh Cluster"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_cluster_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Agent (individual, piggyback)
# ============================================================================

def _wazuh_agent_form():
    return Dictionary(
        title=Title("Wazuh Agent Settings"),
        help_text=Help(
            "Configure thresholds for individual Wazuh agent monitoring."
        ),
        elements={
            "disconnected_state": DictElement(
                required=False,
                parameter_form=SingleChoice(
                    title=Title("State when agent is disconnected"),
                    elements=[
                        SingleChoiceElement(name="warn", title=Title("WARN")),
                        SingleChoiceElement(name="crit", title=Title("CRIT")),
                    ],
                    prefill=DefaultValue("warn"),
                ),
            ),
            "levels_keepalive_age": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Last keepalive age"),
                    help_text=Help(
                        "Age of the last keepalive signal in seconds. "
                        "Alert if the agent hasn't reported in too long."
                    ),
                    form_spec_template=Integer(unit_symbol="s"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(3600, 86400)),
                ),
            ),
        },
    )


rule_spec_wazuh_agent = CheckParameters(
    name="wazuh_agent",
    title=Title("Wazuh Agent (Individual)"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_agent_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Daemon Statistics
# ============================================================================

def _wazuh_daemon_stats_form():
    return Dictionary(
        title=Title("Wazuh Daemon Statistics Settings"),
        help_text=Help(
            "Configure thresholds for Wazuh daemon statistics monitoring."
        ),
        elements={
            "queue_usage_levels": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Queue usage"),
                    help_text=Help("Percentage of queue usage"),
                    form_spec_template=Float(unit_symbol="%"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(70.0, 90.0)),
                ),
            ),
        },
    )


rule_spec_wazuh_daemon_stats = CheckParameters(
    name="wazuh_daemon_stats",
    title=Title("Wazuh Daemon Statistics"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_daemon_stats_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Logs
# ============================================================================

def _wazuh_logs_form():
    return Dictionary(
        title=Title("Wazuh Logs Settings"),
        help_text=Help(
            "Configure thresholds for Wazuh log monitoring."
        ),
        elements={
            "error_levels": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Error log entries"),
                    help_text=Help("Number of error log entries"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(1, 10)),
                ),
            ),
            "warning_levels": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Warning log entries"),
                    help_text=Help("Number of warning log entries"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(10, 50)),
                ),
            ),
        },
    )


rule_spec_wazuh_logs = CheckParameters(
    name="wazuh_logs",
    title=Title("Wazuh Logs"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_logs_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Ruleset
# ============================================================================

def _wazuh_ruleset_form():
    return Dictionary(
        title=Title("Wazuh Ruleset Settings"),
        help_text=Help(
            "Configure thresholds for Wazuh ruleset monitoring."
        ),
        elements={
            "min_rules": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Minimum number of rules"),
                    help_text=Help(
                        "Alert if the number of active rules falls below this value."
                    ),
                ),
            ),
            "min_decoders": DictElement(
                required=False,
                parameter_form=Integer(
                    title=Title("Minimum number of decoders"),
                    help_text=Help(
                        "Alert if the number of active decoders falls below this value."
                    ),
                ),
            ),
        },
    )


rule_spec_wazuh_ruleset = CheckParameters(
    name="wazuh_ruleset",
    title=Title("Wazuh Ruleset"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_ruleset_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Agents Outdated
# ============================================================================

def _wazuh_agents_outdated_form():
    return Dictionary(
        title=Title("Wazuh Outdated Agents Settings"),
        help_text=Help(
            "Configure thresholds for Wazuh outdated agents monitoring."
        ),
        elements={
            "outdated_levels": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Outdated agents"),
                    help_text=Help("Number of agents running outdated versions"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(1, 5)),
                ),
            ),
        },
    )


rule_spec_wazuh_agents_outdated = CheckParameters(
    name="wazuh_agents_outdated",
    title=Title("Wazuh Outdated Agents"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_agents_outdated_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Tasks
# ============================================================================

def _wazuh_tasks_form():
    return Dictionary(
        title=Title("Wazuh Tasks Settings"),
        help_text=Help(
            "Configure thresholds for Wazuh task monitoring."
        ),
        elements={
            "failed_levels": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Failed tasks"),
                    help_text=Help("Number of failed tasks"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(1, 5)),
                ),
            ),
        },
    )


rule_spec_wazuh_tasks = CheckParameters(
    name="wazuh_tasks",
    title=Title("Wazuh Tasks"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_tasks_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh SCA (Security Configuration Assessment)
# ============================================================================

def _wazuh_sca_form():
    return Dictionary(
        title=Title("Wazuh SCA Settings"),
        help_text=Help(
            "Configure thresholds for Wazuh Security Configuration Assessment monitoring."
        ),
        elements={
            "score_levels": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("SCA Score"),
                    help_text=Help("Alert if the SCA score falls below these thresholds"),
                    form_spec_template=Float(unit_symbol="%"),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=DefaultValue(value=(70.0, 50.0)),
                ),
            ),
            "failed_levels": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Failed checks"),
                    help_text=Help("Number of failed SCA checks"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(10, 25)),
                ),
            ),
        },
    )


rule_spec_wazuh_sca = CheckParameters(
    name="wazuh_sca",
    title=Title("Wazuh SCA"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_sca_form,
    condition=HostCondition(),
)


# ============================================================================
# Wazuh Syscheck
# ============================================================================

def _wazuh_syscheck_form():
    return Dictionary(
        title=Title("Wazuh Syscheck Settings"),
        help_text=Help(
            "Configure thresholds for Wazuh Syscheck (File Integrity Monitoring)."
        ),
        elements={
            "scan_age_levels": DictElement(
                required=False,
                parameter_form=SimpleLevels(
                    title=Title("Scan age"),
                    help_text=Help(
                        "Alert if the last syscheck scan is older than these thresholds (in seconds)."
                    ),
                    form_spec_template=Integer(unit_symbol="s"),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=DefaultValue(value=(86400, 172800)),
                ),
            ),
        },
    )


rule_spec_wazuh_syscheck = CheckParameters(
    name="wazuh_syscheck",
    title=Title("Wazuh Syscheck"),
    topic=Topic.APPLICATIONS,
    parameter_form=_wazuh_syscheck_form,
    condition=HostCondition(),
)
