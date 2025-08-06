#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from collections.abc import Iterator

from cmk.server_side_calls.v1 import (
    HostConfig,
    Secret,
    SpecialAgentCommand,
    SpecialAgentConfig,
)

from pydantic import BaseModel


class Params(BaseModel):
    user: str | None = None
    password: Secret | None = None
    proto: tuple[str, str | None]
    sections: list | None = None
    nodename: str | None = None


def generate_datacore_rest_command(
    params: Params,
    host_config: HostConfig,
) -> Iterator[SpecialAgentCommand]:

    command_arguments: list[str | Secret] = []

    if params.user is not None:
        command_arguments += ["--user", params.user]
    if params.password is not None:
        command_arguments += ["--password_id", params.password]
    if params.proto is not None:
        command_arguments += ["--proto", params.proto[0]]
    if params.sections is not None:
        command_arguments += ["--sections", ",".join(params.sections)]

    if params.nodename is not None:
        command_arguments += ["--nodename", (params.nodename)]
    else:
        command_arguments += ["--nodename", host_config.name]

    command_arguments.append(host_config.primary_ip_config.address or host_config.name)

    yield SpecialAgentCommand(command_arguments=command_arguments)


special_agent_datacore_rest = SpecialAgentConfig(
    name="datacore_rest",
    parameter_parser=Params.model_validate,
    commands_function=generate_datacore_rest_command,
)
