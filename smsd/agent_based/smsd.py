#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# 2014 Karsten Schoeke karsten.schoeke@geobasis-bb.de
# 2022 Andre Eckstein, Andre Eckstein@Bechtle.com

# Example output from agent:
# <<<smsd>>>
# status i---------------------------------------------------------------
# mon -61

from .agent_based_api.v1 import (
    register,
    Result,
    Metric,
    State,
    Service,
)


def parse_smsd_status(string_table):
    parsed = ()
    smsd_state = string_table[0][1][0]
    smsd_mon = string_table[1][1]
    parsed = (smsd_state, smsd_mon)
    return parsed


register.agent_section(
    name = "smsd_status",
    parse_function = parse_smsd_status,
)


def discover_smsd_status(section):
    if len(section) == 2:
        yield Service()


def check_smsd_status(section):

    if len(section) == 0:
        yield Result(state=State.UNKNOWN,
                     summary="no information from SMSD: SMSD daemon not running or smsd status file not configured.")
   
    if len(section) == 2:
        (smsd_state, smsd_mon) = section
        message = ""

        if smsd_state == "b":
            s = State.CRIT
            message += "smsd is blocked."
        if smsd_state == "-":
            s = State.UNKNOWN
            message += "smsd is not configured or not connected."
        if smsd_state == "s":
            s = State.OK
            message += "smsd is sending."
        if smsd_state == "r":
            s = State.OK
            message += "smsd ist receiving."
        if smsd_state == "i":
            s = State.OK
            message += "smsd is idle."
        
        # receiving intensity to low
        try:
            smsd_mon=int(smsd_mon)
            print(type(smsd_mon))
            if smsd_mon < -100:
                yield Result(state=State.WARN, summary="intensity is to low %s dBm" % smsd_mon)    
            yield Metric("dBm", smsd_mon)
        except ValueError:
            pass

        yield Result(
            state = s,
            summary = message)
        return


register.check_plugin(
    name="smsd_status",
    service_name="SMSD Status",
    discovery_function=discover_smsd_status,
    check_function=check_smsd_status,
)
