#!/usr/bin/env python3
"""Ruleset definition for Windows firewall status check"""

# (c) Andreas Doehler 'andreas.doehler@bechtle.com'
# License: GNU General Public License v2

from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    SingleChoice,
    SingleChoiceElement,
    Integer,
    SimpleLevels,
    LevelDirection,
    InputHint,
    migrate_to_integer_simple_levels,
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_datacore_rest_virtualdisks():
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
            "expected_mapping": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Expected mapping state"),
                    elements=[
                        SingleChoiceElement(
                            name="virtual_disk_is_served",
                            title=Title("Virtual Disk is served"),
                        ),
                        SingleChoiceElement(
                            name="virtual_disk_is_not_served",
                            title=Title("Virtual Disk is not served"),
                        ),
                    ]
                )
            ),
            "virtual_disk_path_down": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Expected path state for the virtual disk"),
                    elements=[
                        SingleChoiceElement(
                            name="path_down_is_ok",
                            title=Title("Path down is \"OK\""),
                        ),
                        SingleChoiceElement(
                            name="path_down_is_warning",
                            title=Title("Path down is \"Warning\""),
                        ),
                    ]
                )
            ),
        }
    )


rule_spec_datacore_rest_ports = CheckParameters(
    name="datacore_rest_virtualdisks",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(item_title=Title("SANsymphony Virtual Disk")),
    parameter_form=_parameter_valuespec_datacore_rest_virtualdisks,
    title=Title("SANsymphony Virtual Disk"),
)
