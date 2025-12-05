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

"""
Output:
{
    "Caller": "ServerMachine.UpdateLicense",
    "HighPriority": true,
    "Id": {
        "MachineId": "FDD5406C-1664-467B-AACC-889775A2C32E",
        "SequenceNumber": 286
    },
    "Level": 1,
    "MachineName": "WIN-I832JQVQNMJ",
    "MessageData": [
        "WIN-I832JQVQNMJ"
    ],
    "MessageText": "No license found for server {0}. Loading trial license.",
    "NeedsAcknowledge": false,
    "Sources": [
        {
            "SourceCaption": "WIN-I832JQVQNMJ in Server Group",
            "SourceId": "FDD5406C-1664-467B-AACC-889775A2C32E",
            "SourceType": 12
        },
        {
            "SourceCaption": "Server Group",
            "SourceId": "6bdeb641-2986-4b67-932d-2d9cd074c9ca",
            "SourceType": 12
        }
    ],
    "TimeStamp": "/Date(1717005930152)/",
    "UserId": null,
    "UserName": null,
    "Visibility": 64
}"""

from typing import Any
from collections.abc import Mapping

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    Result,
    State,
    Metric,
    check_levels,
)

from cmk_addons.plugins.datacore_rest.lib import (
    discover_datacore_rest_single,
    parse_datacore_rest_single,
    convert_timestamp_to_epoch,
    convert_epoch_to_readable,
    safe_get,
    ALERT_DISPLAY_LIMIT,
)


agent_section_datacore_rest_alerts = AgentSection(
    name="datacore_rest_alerts",
    parse_function=parse_datacore_rest_single,
    parsed_section_name="datacore_rest_alerts",
)


def check_datacore_rest_alerts(
    params: Mapping[str, Any], section: list[Any]
) -> CheckResult:
    """Check state of DataCore Alerts."""

    alert_list = []

    # The section is a list containing a single list of alerts: [[alert1, alert2, ...]]
    # Flatten it to get the actual alerts
    alerts = section[0] if section and isinstance(section[0], list) else section

    for alert in alerts:
        # Use safe_get for robust field access
        message_text = safe_get(alert, "MessageText", default="Unknown alert")
        message_data = safe_get(alert, "MessageData")
        timestamp = safe_get(alert, "TimeStamp")

        if not timestamp:
            continue  # Skip alerts without timestamp

        text_string = message_text

        # Replace the {0} {1}... placeholders in the alert text string with the data from the MessageData dictionary
        if message_data is not None:
            nr_of_placeholders = len(message_data)
            for message_idx in range(nr_of_placeholders):
                placeholder = "{" + str(message_idx) + "}"
                if placeholder in text_string:
                    replacement = str(message_data[message_idx]) if message_data[message_idx] else ""
                    text_string = text_string.replace(placeholder, replacement)

        remove_support = params.get("remove_support_bundle_messages", "remove")
        if remove_support == "remove" and "Support bundle" in text_string:
            continue

        alert_list.append((convert_timestamp_to_epoch(timestamp), text_string))

    if len(alert_list) == 0:
        yield Metric("alerts", 0)
        yield Result(state=State.OK, summary="No alerts present")
        return

    nr_of_alerts = len(alert_list)
    sorted_alerts = sorted(alert_list, key=lambda x: x[0], reverse=True)
    top_entries = sorted_alerts[:ALERT_DISPLAY_LIMIT]

    details = ""
    for date, message in top_entries:
        details += f"{convert_epoch_to_readable(date)} {message} \n"

    latest_entry = (
        f"{convert_epoch_to_readable(top_entries[0][0])}: "
        f"{top_entries[0][1][:80]}"
    )

    upper_levels = params.get("number_of_alerts", ("fixed", (1, 1)))

    yield from (
        check_levels(
            nr_of_alerts,
            levels_upper=upper_levels,
            label="Alerts",
            notice_only=True,
            metric_name="alerts",
        )
    )

    message = f"latest alert: {latest_entry}"
    yield Result(state=State.OK, summary=message, details=details)


check_plugin_datacore_rest_alerts = CheckPlugin(
    name="datacore_rest_alerts",
    service_name="SANsymphony Alerts",
    sections=["datacore_rest_alerts"],
    discovery_function=discover_datacore_rest_single,
    check_function=check_datacore_rest_alerts,
    check_default_parameters={
        "number_of_alerts": ("fixed", (1, 1)),
        "remove_support_bundle_messages": "remove",
    },
    check_ruleset_name="datacore_rest_alerts",
)
