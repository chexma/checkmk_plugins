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

import json
import time
from cmk.agent_based.v2 import DiscoveryResult, Service, StringTable


def discover_datacore_rest(section) -> DiscoveryResult:
    "Discovers service with multiple items"
    for item in section:
        # Move that to the special agent ?
        # if "Loopback" not in item:
        yield Service(item=item)


def discover_datacore_rest_single(section) -> DiscoveryResult:
    "Discovers service without items"
    if section:
        yield Service()


def parse_datacore_rest(string_table: StringTable):
    """parse json for multi item sections"""
    parsed = {}
    for line in string_table:
        entry = json.loads(line[0])
        if "Alias" in entry and entry["Alias"] is not None:
            item = entry.get("Alias")
        else:
            item = entry.get("Caption")
        parsed.setdefault(item, entry)
    return parsed


def parse_datacore_rest_single(string_table: StringTable):
    """parse json for single item sections"""
    parsed = {}
    for line in string_table:
        parsed = json.loads(line[0])
    return parsed


def convert_timestamp(timestamp):
    "Both timestamp conversions in one place"
    epoch = convert_timestamp_to_epoch(timestamp)
    readable = convert_epoch_to_readable(epoch)
    return readable


def convert_timestamp_to_epoch(timestamp):
    """Converts the 'CollectionTime' string of the API objects in miliseconds into epoch (in seconds)"""
    if '+' in timestamp:
        timestamp = timestamp.split('+', 1)[0]
        epoch_time_in_seconds = int(timestamp[6:]) / 1000
    else:
        epoch_time_in_seconds = int(timestamp[6:-2]) / 1000
    return epoch_time_in_seconds


def convert_epoch_to_readable(epoch_time):
    "Prints a human readable Format for epoch"
    time_object = time.localtime(epoch_time)
    formatted_date = time.strftime('%d.%m.%Y %H:%M:%S', time_object)
    return formatted_date


def calculate_percentages(value1: int, value2: int):
    "Returns percentages for two single values"
    total = value1 + value2
    if total <= 0:
        return (0, 0)

    percent_value1 = (value1 / total) * 100
    percent_value2 = (value2 / total) * 100
    return percent_value1, percent_value2
