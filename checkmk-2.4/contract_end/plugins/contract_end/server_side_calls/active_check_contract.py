#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Contract End Date Active Check - Server Side Calls
# Copyright (C) 2025

from collections.abc import Iterable

from pydantic import BaseModel

from cmk.server_side_calls.v1 import (
    ActiveCheckCommand,
    ActiveCheckConfig,
    HostConfig,
)


class Parameters(BaseModel):
    contract_name: str
    end_date: str
    date_format: str = "iso8601"
    levels: dict[str, int]  # {"warn": seconds, "crit": seconds}
    contract_id: str | None = None
    start_date: str | None = None
    additional_info: str | None = None


def make_check_contract_commands(
    params: Parameters, host_config: HostConfig
) -> Iterable[ActiveCheckCommand]:
    """Generate the active check command for contract monitoring."""

    # Extract warn and crit thresholds
    warn_threshold = params.levels.get("warn", 30 * 24 * 3600)
    crit_threshold = params.levels.get("crit", 7 * 24 * 3600)

    # Build command arguments
    args = [
        "--contract-name", params.contract_name,
        "--end-date", params.end_date,
        "--date-format", params.date_format,
        "--warn", str(warn_threshold),
        "--crit", str(crit_threshold),
    ]

    if params.contract_id:
        args.extend(["--contract-id", params.contract_id])

    if params.start_date:
        args.extend(["--start-date", params.start_date])

    if params.additional_info:
        args.extend(["--additional-info", params.additional_info])

    yield ActiveCheckCommand(
        service_description=f"Contract {params.contract_name}",
        command_arguments=args,
    )


active_check_contract_enddate = ActiveCheckConfig(
    name="contract_enddate",
    parameter_parser=Parameters.model_validate,
    commands_function=make_check_contract_commands,
)
