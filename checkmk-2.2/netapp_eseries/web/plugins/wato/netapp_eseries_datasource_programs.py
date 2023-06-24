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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    TextAscii,
    DropdownChoice,
    Integer,
    ListChoice,
)

from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
    IndividualOrStoredPassword,
)

from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourceProgramsHardware


def _valuespec_special_agents_netappeseries():
    return Dictionary(
        title=_("Netapp E-Series via REST API"),
        elements=[
            ("user", TextAscii(
                help = _("Please use the user \"monitor\" available for this purpose on the E-Series instead of the \"admin\" user."),
                title = _("Username"),
                allow_empty = False,
            )),
            ('password', IndividualOrStoredPassword(
                title=_("Password"),
                allow_empty=False,
            )),
            ("sections", ListChoice(
                title = _("Retrieve information about..."),
                choices = [
                    ("batteries", _("Batteries")),
                    ("controllers", _("Controllers")),
                    ("drawers", _("Drawers")),
                    ("drives", _("Drives")),
                    ("esms", _("ESMs")),
                    ("fans", _("Fans")),
                    ("interfaces", _("Interfaces")),
                    ("pools", _("Pools")),
                    ("powerSupplies", _("Powersupplies")),
                    ("system", _("System")),
                    ("thermalSensors", _("Thermal sensors")),
                    ("trays", _("Trays")),
                    ("volumes", _("Volumes")),
                ],
                default_value = [
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
                allow_empty = False,
            )),
            ("port", Integer(
                title = _("Advanced - TCP Port number"),
                help = _("Port number for connection to the Rest API. Usually 8443 (TLS)"),
                default_value = 8443,
                minvalue = 1,
                maxvalue = 65535,
            )),
            ("proto", DropdownChoice(
                title = _("Advanced - Protocol"),
                default_value = 'https',
                help = _("Protocol for the connection to the Rest API. https is highly recommended!!!"),
                choices = [
                    ('http', _("http")),
                    ('https', _("https")),
                ],
            )),
            ("system-id", TextAscii(
                title = _("Advanced - E-Series-System-ID"),
                help = _("The System ID of your Netapp E-Series. Should always be 1 if not connected through a SANtricity Web Proxy"),
                default_value = 1,
            )),
        ],
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsHardware,
        name="special_agents:netappeseries",
        valuespec=_valuespec_special_agents_netappeseries,
    ))
