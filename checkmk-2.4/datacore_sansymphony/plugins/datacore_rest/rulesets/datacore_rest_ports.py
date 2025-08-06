#!/usr/bin/env python3
"""Ruleset definition for DataCore Sansymphony Ports"""


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
    migrate_to_integer_simple_levels
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _parameter_valuespec_datacore_rest_ports():
    return Dictionary(
        elements={
            "LinkFailureCount": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper level for number of link failures"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "InvalidCrcCount": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper level for number of invalid CRC count"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "LossOfSignalCount": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper level for number of signal loss"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "LossOfSyncCount": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper level for number of sync loss"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "InvalidTransmissionWordCount": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper level for invalid transmission word count"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(0, 0)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "expected_port_connection_status": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Expected port connection status"),
                    elements=[
                        SingleChoiceElement(
                            name="connected",
                            title=Title("Port is connected"),
                        ),
                        SingleChoiceElement(
                            name="disconnected",
                            title=Title("Port is not connected"),
                        ),
                    ]
                )
            )
        },
    )


rule_spec_datacore_rest_ports = CheckParameters(
    name="datacore_rest_ports",
    topic=Topic.APPLICATIONS,
    condition=HostAndItemCondition(item_title=Title("SANsymphony Port")),
    parameter_form=_parameter_valuespec_datacore_rest_ports,
    title=Title("SANsymphony Port"),
)
