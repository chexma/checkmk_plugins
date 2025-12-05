#!/usr/bin/env python3
"""Ruleset definition for DataCore SANsymphony Physical Disks"""

# (c) Andreas Doehler 'andreas.doehler@bechtle.com'
# License: GNU General Public License v2

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Integer,
    SimpleLevels,
    LevelDirection,
    InputHint,
    migrate_to_integer_simple_levels,
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_datacore_rest_physicaldisks():
    return Dictionary(
        elements={
            "write_io_levels_upper": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper write IO levels"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "write_io_levels_lower": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Lower write IO levels"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.LOWER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "upper_read_latency_levels": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper read latency levels"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "upper_write_latency_levels": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper write latency levels"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
        }
    )


rule_spec_datacore_rest_physicaldisks = CheckParameters(
    name="datacore_rest_physicaldisks",
    topic=Topic.STORAGE,
    condition=HostAndItemCondition(item_title=Title("SANsymphony Physical Disk")),
    parameter_form=_parameter_valuespec_datacore_rest_physicaldisks,
    title=Title("SANsymphony Physical Disk"),
)
