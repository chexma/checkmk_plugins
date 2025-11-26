#!/usr/bin/env python3
# Copyright (C) 2024 CheckMK GmbH - License: GNU General Public License v2
"""Server-Side Calls configuration for Wazuh Special Agent"""

from cmk.server_side_calls.v1 import (
    noop_parser,
    SpecialAgentConfig,
    SpecialAgentCommand,
)


def _agent_arguments(params, host_config):
    """Convert GUI parameters to command line arguments.

    Args:
        params: Dictionary from ruleset configuration
        host_config: Host configuration object with:
            - host_config.name: Host name
            - host_config.primary_ip_config.address: IP address
            - host_config.alias: Host alias
    """
    args = [
        "--hostname", host_config.primary_ip_config.address,
    ]

    if "port" in params:
        args.extend(["--port", str(params["port"])])

    if "username" in params:
        args.extend(["--username", params["username"]])

    if "password" in params:
        # Password is an object, use unsafe() to get plain text
        args.extend(["--password", params["password"].unsafe()])

    if params.get("no_cert_check"):
        args.append("--no-cert-check")

    if "timeout" in params:
        args.extend(["--timeout", str(params["timeout"])])

    if params.get("piggyback_agents"):
        args.append("--piggyback-agents")

    if params.get("piggyback_all_agents"):
        args.append("--piggyback-all-agents")

    yield SpecialAgentCommand(command_arguments=args)


special_agent_wazuh = SpecialAgentConfig(
    name="wazuh",
    parameter_parser=noop_parser,
    commands_function=_agent_arguments,
)
