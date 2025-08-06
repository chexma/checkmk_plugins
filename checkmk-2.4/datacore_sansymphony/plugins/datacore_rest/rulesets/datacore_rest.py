#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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
    MultipleChoice,
    MultipleChoiceElement,
    Password,
    String,
)

from cmk.rulesets.v1.rule_specs import Topic, SpecialAgent

from cmk.rulesets.v1.form_specs.validators import LengthInRange


def _valuespec_special_agents_datacore_rest() -> Dictionary:
    return Dictionary(
        elements={
            "user": DictElement(
                parameter_form=String(
                    title = Title("Username"),
                    help_text=Help(
                        "User Account to login to the Sansymphony Rest API"
                    ),
                ),
                required=True
            ),
            "password": DictElement(
                parameter_form=Password(
                    title=Title("Password"),
                    # custom_validate=(LengthInRange(min_value=1))
                ),
                required=True,
            ),
            "sections": DictElement(
                parameter_form=MultipleChoice(
                    title=Title("Retrieve information about..."),
                    elements = [
                        MultipleChoiceElement(
                            name="alerts", title=Title("Alerts"),
                        ),
                        MultipleChoiceElement(
                            name="hosts", title=Title("Hosts (SAN Clients)"),
                        ),
                        MultipleChoiceElement(
                            name="hostgroups", title=Title("Hostgroups"),
                        ),
                        MultipleChoiceElement(
                            name="physicaldisks", title=Title("Physical Disks"),
                        ),
                        MultipleChoiceElement(
                            name="pools", title=Title("Pools"),
                        ),
                        MultipleChoiceElement(
                            name="ports", title=Title("Ports (FC, iSCSI)"),
                        ),
                        MultipleChoiceElement(
                            name="servergroups", title=Title("Servergroups"),
                        ),
                        MultipleChoiceElement(
                            name="servers", title=Title("Servers"),
                        ),
                        MultipleChoiceElement(
                            name="snapshots", title=Title("Snapshots"),
                        ),
                        MultipleChoiceElement(
                            name="virtualdisks", title=Title("Virtual Disks"),
                        ),
                    ],
                    prefill=DefaultValue(
                        [   "alerts",
                            "hosts",
                            "hostgroups",
                            "physicaldisks",
                            "pools",
                            "ports",
                            "servergroups",
                            "servers",
                            "servers",
                            "snapshots",
                            "virtualdisks",
                        ],
                    ),
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
                required=True,
            ),
            "nodename": DictElement(
                parameter_form=String(
                    title = Title("Advanced - Sansymphony Servername to fetch infos for"),
                    help_text=Help(
                        "This is necessary, if the Sansymphony internal server name differs from your hostname in checkmk"
                    ),
                ),
                required=False,
            ),
        },
    )


rule_spec_datacore_rest_datasource_programs = SpecialAgent(
    name="datacore_rest",
    title=Title("DataCore Sansymphony via REST API"),
    topic=Topic.STORAGE,
    parameter_form=_valuespec_special_agents_datacore_rest,
    help_text=(
        "This rule selects the Agent DataCore SANsymphony instead of the normal Check_MK Agent"
        "which collects the data through the REST API."
        "Please create a read-only account in SANsymphony instead of using administrative accounts."
    ),
)
