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

from cmk.gui.i18n import _
from cmk.gui.plugins.wato.utils import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersHardware,
)
from cmk.gui.valuespec import Dictionary, DropdownChoice


def _parameters_valuespec_netapp_eseries_interfaces():
    interface_status_choice = [
        ("up", _("Up")),
        ("down", _("Down")),
        ("unknown", _("Unknown")),
    ]
    return Dictionary(
        elements=[
            (
                "interface_state",
                DropdownChoice(
                    title=_("Wanted Interface State"),
                    choices=interface_status_choice,
                    default_value="on",
                ),
            ),
        ],
        title=_("Wanted Interface State for Netapp E-Series Interfaces"),
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="netapp_eseries_interfaces",
        group=RulespecGroupCheckParametersHardware,
        match_type="dict",
        parameter_valuespec=_parameters_valuespec_netapp_eseries_interfaces,
        title=lambda: _("Netapp E-Series Interface Status"),
    )
)