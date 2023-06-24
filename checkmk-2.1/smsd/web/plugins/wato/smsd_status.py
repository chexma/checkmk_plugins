try:
    from cmk.gui.i18n import _
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
    from cmk.gui.valuespec import DropdownChoice

    def _valuespec_agent_config_smsd_status():
        return     DropdownChoice(
            title = _("smsd Status"),
            help = _("This will deploy the agent plugin <tt>smsd status</tt> "),
            choices = [
                (True, _("Deploy the plugin") ),
                (False, _("Do not deploy the plugin")),
            ]
        )

    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsAgentPlugins,
            name="agent_config:smsd_status",
            valuespec=_valuespec_agent_config_smsd_status,
        ))
   
except ModuleNotFoundError:
    # RAW edition
    pass
