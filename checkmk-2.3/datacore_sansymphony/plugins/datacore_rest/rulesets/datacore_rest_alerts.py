#!/usr/bin/env python3
"""Ruleset definition for DataCore Sansymphony Ports"""


from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Integer,
    SimpleLevels,
    LevelDirection,
    InputHint,
    SingleChoice,
    SingleChoiceElement,
    DefaultValue,
    migrate_to_integer_simple_levels
)

from cmk.rulesets.v1.rule_specs import CheckParameters, HostCondition, Topic


def _parameter_valuespec_datacore_rest_alerts():
    return Dictionary(
        elements={
            "number_of_alerts": DictElement(
                parameter_form=SimpleLevels[int](
                    title=Title("Upper level for number of alerts"),
                    form_spec_template=Integer(),
                    level_direction=LevelDirection.UPPER,
                    prefill_fixed_levels=InputHint(value=(1, 1)),
                    migrate=migrate_to_integer_simple_levels,
                )
            ),
            "remove_support_bundle_messages": DictElement(
                parameter_form=SingleChoice(
                    title=Title("Remove SupportBundle collection messages from alerts"),
                    elements=[
                        SingleChoiceElement(
                            name='remove',
                            title=Title("Remove messages"),
                        ),
                        SingleChoiceElement(
                            name='dont_remove',
                            title=Title("Don´t remove messages"),
                        ),
                    ],
                    prefill=DefaultValue('remove'),
                )
            )
        },
    )


rule_spec_datacore_rest_alerts = CheckParameters(
    name="datacore_rest_alerts",
    topic=Topic.APPLICATIONS,
    condition=HostCondition(),
    parameter_form=_parameter_valuespec_datacore_rest_alerts,
    title=Title("SANsymphony Alerts"),
)
