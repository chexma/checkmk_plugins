#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Iterator, Mapping

from cmk.server_side_calls.v1 import (
    HostConfig,
    noop_parser,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)


def generate_netapp_command(
    params: Mapping[str, object],
    host_config: HostConfig,
) -> Iterator[SpecialAgentCommand]:

#    assert isinstance(secret := params["password"], Secret)

    args: list[str | Secret] = [
        "-u", params["user"],
        "--password-id", params["password"],
#        "--password-id", secret.unsafe(),
    ]

    if "port" in params:
        args.extend(["--port", str(params["port"])])
    if "proto" in params:
        args.extend(["--proto", (params["proto"][0])])
    if "system_id" in params:
        args.extend(["--system-id", str(params["system_id"])])
    if "sections" in params:
        args.extend(["--sections", ",".join(params["sections"])])

    args.append(host_config.primary_ip_config.address or host_config.name)

    yield SpecialAgentCommand(command_arguments=args)


special_agent_netapp_eseries = SpecialAgentConfig(
    name="netappeseries",
    parameter_parser=noop_parser,
    commands_function=generate_netapp_command,
)
