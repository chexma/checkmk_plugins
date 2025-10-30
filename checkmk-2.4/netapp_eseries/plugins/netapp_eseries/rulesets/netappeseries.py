#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Andreas Doehler <andreas.doehler@bechtle.com/andreas.doehler@gmail.com>
# (c) Andre Eckstein <andre.eckstein@bechtle.com>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.rulesets.v1 import Title, Help

from cmk.rulesets.v1.form_specs import (
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    Integer,
    MultipleChoice,
    MultipleChoiceElement,
    Password,
    String,
    validators,
    migrate_to_password
)

from cmk.rulesets.v1.rule_specs import Topic, SpecialAgent

from cmk.rulesets.v1.form_specs.validators import LengthInRange, NetworkPort


def _valuespec_special_agents_netapp_eseries() -> Dictionary:
    return Dictionary(
        elements={
            "user": DictElement(
                parameter_form=String(
                    title = Title("Username"),
                    prefill=DefaultValue("monitor")
                ),
                required=True
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password"),
                    custom_validate=(LengthInRange(min_value=1),),
                    migrate=migrate_to_password,
                ),
                required=True,
            ),
            "sections": DictElement(
                parameter_form=MultipleChoice(
                    title=Title("Retrieve information about..."),
                    elements = [
                        MultipleChoiceElement(
                            name="batteries", title=Title("Batteries"),
                        ),
                        MultipleChoiceElement(
                            name="controllers", title=Title("Controllers"),
                        ),
                        MultipleChoiceElement(
                            name="drawers", title=Title("Drawers"),
                        ),
                        MultipleChoiceElement(
                            name="drives", title=Title("Drives"),
                        ),
                        MultipleChoiceElement(
                            name="esms", title=Title("ESMS"),
                        ),
                        MultipleChoiceElement(
                            name="fans", title=Title("Fans"),
                        ),
                        MultipleChoiceElement(
                            name="interfaces", title=Title("Interfaces"),
                        ),
                        MultipleChoiceElement(
                            name="pools", title=Title("Pools"),
                        ),
                        MultipleChoiceElement(
                            name="powerSupplies", title=Title("Powersupplies"),
                        ),
                        MultipleChoiceElement(
                            name="system", title=Title("System"),
                        ),
                        MultipleChoiceElement(
                            name="thermalSensors", title=Title("Thermal sensors"),
                        ),
                        MultipleChoiceElement(
                            name="trays", title=Title("Trays"),
                        ),
                        MultipleChoiceElement(
                            name="volumes", title=Title("Volumes"),
                        ),
                    ],
                    prefill=DefaultValue(
                        [
                            "batteries",
                            "controllers",
                            "drawers",
                            "drives",
                            "esms",
                            "fans",
                            "interfaces",
                            "pools",
                            "powerSupplies",
                            "system",
                            "trays",
                            "volumes",
                            "thermalSensors",
                        ],
                    ),
                ),
                required=False,
            ),
            "port": DictElement(
                parameter_form=Integer(
                    title=Title("Advanced - TCP Port number"),
                    help_text=Help(
                        "Port number for connection to the Rest API. Usually 8443 (TLS)"
                    ),
                    prefill=DefaultValue(8443),
                    custom_validate=(NetworkPort(),),
                ),
                required=False,
            ),
            "proto": DictElement(
                parameter_form=CascadingSingleChoice(
                    title=Title("Advanced - Protocol"),
                    prefill=DefaultValue("https"),
                    help_text=Help(
                        "Protocol for the connection to the Rest API."
                        "https is highly recommended!!!"
                    ),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="http",
                            title=Title("http"),
                            parameter_form=FixedValue(value=None),
                        ),
                        CascadingSingleChoiceElement(
                            name="https",
                            title=Title("https"),
                            parameter_form=FixedValue(value=None),
                        ),
                    ],
                ),
                required=False,
            ),
            "system_id": DictElement(
                parameter_form=Integer(
                    title=Title("Advanced - E-Series-System-ID"),
                    help_text=Help(
                        "The System ID of your Netapp E-Series. Should always be 1 if not connected through a SANtricity Web Proxy"
                    ),
                    prefill=DefaultValue(1),
                    custom_validate=(validators.NumberInRange(min_value=1, max_value=1024),),
                ),
                required=False,
            ),
        },
    )


rule_spec_netapp_eseries_datasource_programs = SpecialAgent(
    name="netappeseries",
    title=Title("Netapp E-Series via REST API"),
    topic=Topic.STORAGE,
    parameter_form=_valuespec_special_agents_netapp_eseries,
    help_text=(
        "This rule selects the Agent Redfish instead of the normal Check_MK Agent "
        "which collects the data through the REST API."
        "Please use the user \"monitor\" available for this purpose on the E-Series instead of the \"admin\" user."
    ),
)
