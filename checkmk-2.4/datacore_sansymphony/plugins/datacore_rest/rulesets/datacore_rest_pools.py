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

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Float,
    Integer,
    LevelDirection,
    Percentage,
    SimpleLevels,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _formspec_datacore_rest_pool_capacity() -> Dictionary:
    """
    Form specification for DataCore pool capacity monitoring.
    Uses standard filesystem-style parameters with levels and magic factor support.
    """
    return Dictionary(
        title=Title("Pool capacity levels"),
        help_text=Help(
            "Specify the threshold levels for pool capacity. The levels can be specified as "
            "percentages of the total pool size. Additionally, the magic factor allows for "
            "dynamic level adjustments based on pool size - larger pools get more lenient thresholds."
        ),
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels for pool usage"),
                    help_text=Help(
                        "Specify the percentage levels at which warnings and critical alerts should be triggered. "
                        "These levels apply to the used space in the pool."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((80.0, 90.0)),
                ),
                required=True,
            ),
            "magic_normsize": DictElement(
                parameter_form=Integer(
                    title=Title("Reference size for magic factor"),
                    help_text=Help(
                        "The magic factor allows dynamic level adjustment based on pool size. "
                        "Larger pools get more generous thresholds. This is the reference size "
                        "in GB. A pool of this size uses the standard levels. Smaller pools get "
                        "more aggressive levels, larger pools get more lenient ones."
                    ),
                    prefill=DefaultValue(20),
                    unit_symbol="GB",
                ),
                required=False,
            ),
            "levels_low": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Minimum levels for magic factor"),
                    help_text=Help(
                        "These are the most lenient levels applied by the magic factor, "
                        "used for very large pools."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Percentage(),
                    prefill_fixed_levels=DefaultValue((50.0, 60.0)),
                ),
                required=False,
            ),
            "trend_range": DictElement(
                parameter_form=TimeSpan(
                    title=Title("Time range for trend computation"),
                    help_text=Help(
                        "Specify the time range over which the trend is computed. "
                        "The trend shows the rate of pool space consumption."
                    ),
                    displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR],
                    prefill=DefaultValue(24.0 * 3600.0),  # 24 hours in seconds
                ),
                required=False,
            ),
            "trend_perfdata": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Levels on trends in MB per time range"),
                    help_text=Help(
                        "Set levels on the growth rate of pool usage. "
                        "The levels are in MB per the configured time range."
                    ),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Float(),
                    prefill_fixed_levels=DefaultValue((0.0, 0.0)),
                ),
                required=False,
            ),
        },
    )


rule_spec_datacore_rest_pool_capacity = CheckParameters(
    name="datacore_rest_pool_capacity",
    topic=Topic.STORAGE,
    condition=HostAndItemCondition(item_title=Title("Pool")),
    parameter_form=_formspec_datacore_rest_pool_capacity,
    title=Title("DataCore SANsymphony Pool Capacity"),
    help_text=Help(
        "This ruleset allows you to configure thresholds for DataCore SANsymphony storage pool capacity. "
        "The pool is treated as a filesystem, with support for percentage levels and magic factor "
        "for dynamic thresholds based on pool size."
    ),
)
