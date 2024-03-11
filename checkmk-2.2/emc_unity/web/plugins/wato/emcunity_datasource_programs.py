#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourceProgramsHardware
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
    MigrateToIndividualOrStoredPassword
)
from cmk.gui.valuespec import (
    Dictionary,
    FixedValue,
    TextInput
)

def _valuespec_special_agents_emcunity():
    return Dictionary(
        elements=[
            ("username", TextInput(title=_("Username"))),
            ("password", MigrateToIndividualOrStoredPassword(title=_("Password"))),
            ("lockbox",
             FixedValue(
                 True,
                 title=_("Use Credentials From:"),
                 totext=_("Lockbox"),
             )),
        ],
        title=_("EMC Unity"),
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsHardware,
        name="special_agents:emcunity",
        valuespec=_valuespec_special_agents_emcunity,
    ))
