#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Contract End Date Monitoring - Ruleset
# Copyright (C) 2025

from cmk.rulesets.v1 import Title, Help, Label
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
    SingleChoice,
    SingleChoiceElement,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_form():
    return Dictionary(
        title=Title("Contract End Date Monitoring"),
        help_text=Help(
            "This rule allows you to monitor hardware support contracts by their end date. "
            "The check will alert you when a contract is approaching its expiration based on "
            "the configured thresholds."
        ),
        elements={
            "contract_name": DictElement(
                parameter_form=String(
                    title=Title("Contract Name"),
                    help_text=Help("Name of the contract. This will be used as the service name."),
                ),
                required=True,
            ),
            "end_date": DictElement(
                parameter_form=String(
                    title=Title("Contract End Date"),
                    help_text=Help("The expiration date of the contract. Format depends on the selected date format below."),
                ),
                required=True,
            ),
            "date_format": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Date Format"),
                    help_text=Help("Select the format of the end date you entered above."),
                    elements=[
                        SingleChoiceElement(
                            name="iso8601",
                            title=Title("ISO 8601 (YYYY-MM-DD)"),
                        ),
                        SingleChoiceElement(
                            name="eu_date",
                            title=Title("European format (DD.MM.YYYY)"),
                        ),
                        SingleChoiceElement(
                            name="eu_date_slash",
                            title=Title("European format with slash (DD/MM/YYYY)"),
                        ),
                        SingleChoiceElement(
                            name="us_date",
                            title=Title("US format (MM/DD/YYYY)"),
                        ),
                        SingleChoiceElement(
                            name="us_date_dash",
                            title=Title("US format with dash (MM-DD-YYYY)"),
                        ),
                    ],
                    prefill=DefaultValue("iso8601"),
                ),
                required=True,
            ),
            "levels": DictElement(
                parameter_form=Dictionary(
                    title=Title("Time remaining thresholds"),
                    help_text=Help(
                        "Set the thresholds for warning and critical states based on the remaining time "
                        "until the contract expires. For example, warn at 30 days and critical at 7 days."
                    ),
                    elements={
                        "warn": DictElement(
                            parameter_form=TimeSpan(
                                title=Title("Warning at"),
                                help_text=Help("Warn when the remaining time is less than or equal to this value"),
                                displayed_magnitudes=[
                                    TimeMagnitude.DAY,
                                    TimeMagnitude.HOUR,
                                    TimeMagnitude.MINUTE,
                                    TimeMagnitude.SECOND,
                                ],
                                prefill=DefaultValue(30 * 24 * 3600.0),  # 30 days in seconds
                            ),
                            required=True,
                        ),
                        "crit": DictElement(
                            parameter_form=TimeSpan(
                                title=Title("Critical at"),
                                help_text=Help("Critical when the remaining time is less than or equal to this value"),
                                displayed_magnitudes=[
                                    TimeMagnitude.DAY,
                                    TimeMagnitude.HOUR,
                                    TimeMagnitude.MINUTE,
                                    TimeMagnitude.SECOND,
                                ],
                                prefill=DefaultValue(7 * 24 * 3600.0),  # 7 days in seconds
                            ),
                            required=True,
                        ),
                    },
                ),
                required=True,
            ),
            "additional_info": DictElement(
                parameter_form=String(
                    title=Title("Additional Information"),
                    help_text=Help(
                        "Optional additional information about the contract. "
                        "This will be displayed in the service details."
                    ),
                ),
                required=False,
            ),
        },
    )


rule_spec_contract_enddate = CheckParameters(
    name="contract_enddate",
    title=Title("Contract End Date Monitoring"),
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form,
    condition=HostAndItemCondition(
        item_title=Title("Contract Item"),
    ),
)
