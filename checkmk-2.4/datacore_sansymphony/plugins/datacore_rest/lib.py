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
from typing import Any

from collections.abc import Mapping

from cmk.agent_based.v2 import DiscoveryResult, Service, StringTable, get_rate

# =============================================================================
# Constants
# =============================================================================

# API Constants
PASSWORD_STORE_DELIMITER = ":"
API_TIMEOUT_SECONDS = 5

# Display Constants
ALERT_DISPLAY_LIMIT = 10
SNAPSHOT_DISPLAY_LIMIT = 10

# Sector Size
SECTOR_SIZE_512 = 512

# Port Error Types to Skip
PORT_SKIP_ERROR_TYPES = frozenset({"TotalErrorCount", "PrimitiveSeqProtocolErrCount"})


def discover_datacore_rest(section: Mapping[str, Any]) -> DiscoveryResult:
    """Discovers service with multiple items."""
    for item in section:
        yield Service(item=item)


def discover_datacore_rest_single(section: Any) -> DiscoveryResult:
    """Discovers service without items."""
    if section:
        yield Service()


def parse_datacore_rest(string_table: StringTable) -> dict[str, Any]:
    """Parse json for multi item sections."""
    parsed: dict[str, Any] = {}
    for line in string_table:
        entry = json.loads(line[0])
        if "Alias" in entry and entry["Alias"] is not None:
            item = entry.get("Alias")
        else:
            item = entry.get("Caption")
        parsed.setdefault(item, entry)
    return parsed


def parse_datacore_rest_single(string_table: StringTable) -> list[dict[str, Any]]:
    """Parse json for single item sections."""
    parsed: list[dict[str, Any]] = []
    for line in string_table:
        parsed.append(json.loads(line[0]))
    return parsed


def convert_timestamp(timestamp: str) -> str:
    """Both timestamp conversions in one place."""
    epoch = convert_timestamp_to_epoch(timestamp)
    readable = convert_epoch_to_readable(epoch)
    return readable


def convert_timestamp_to_epoch(timestamp: str) -> float:
    """Converts the 'CollectionTime' string of the API objects in miliseconds into epoch (in seconds)."""
    if '+' in timestamp:
        timestamp = timestamp.split('+', 1)[0]
        epoch_time_in_seconds = int(timestamp[6:]) / 1000
    else:
        epoch_time_in_seconds = int(timestamp[6:-2]) / 1000
    return epoch_time_in_seconds


def convert_epoch_to_readable(epoch_time: float) -> str:
    """Prints a human readable Format for epoch."""
    time_object = time.localtime(epoch_time)
    formatted_date = time.strftime('%d.%m.%Y %H:%M:%S', time_object)
    return formatted_date


def calculate_percentages(value1: int, value2: int) -> tuple[float, float]:
    """Returns percentages for two single values."""
    total = value1 + value2
    if total <= 0:
        return (0.0, 0.0)

    percent_value1 = (value1 / total) * 100
    percent_value2 = (value2 / total) * 100
    return percent_value1, percent_value2


# =============================================================================
# Performance Rate Calculation
# =============================================================================

def calculate_performance_rates(
    value_store: Any,
    item: str,
    counters: list[str],
    collection_time: float,
    perf_data: dict[str, Any],
    raise_overflow: bool = True
) -> dict[str, int]:
    """Calculate rates for performance counters.

    Args:
        value_store: CheckMK value store from get_value_store()
        item: Service item name for unique counter keys
        counters: List of counter names to calculate rates for
        collection_time: Current collection time in epoch seconds
        perf_data: Performance data dictionary containing counter values
        raise_overflow: Whether to raise on counter overflow

    Returns:
        Dictionary mapping counter names to their calculated rates (per second)
    """
    rate = {}
    for counter in counters:
        rate[counter] = round(
            get_rate(
                value_store,
                f"{item}.{counter}",
                collection_time,
                perf_data[counter],
                raise_overflow=raise_overflow,
            )
        )
    return rate


def calculate_average_latency(
    total_reads: int,
    total_writes: int,
    total_read_time: int,
    total_write_time: int
) -> tuple[float, float]:
    """Calculate average read and write latency.

    Args:
        total_reads: Number of read operations (rate)
        total_writes: Number of write operations (rate)
        total_read_time: Total read time (rate)
        total_write_time: Total write time (rate)

    Returns:
        Tuple of (avg_read_latency, avg_write_latency)
    """
    avg_read = round((total_read_time / total_reads), 2) if total_reads > 0 else 0.0
    avg_write = round((total_write_time / total_writes), 2) if total_writes > 0 else 0.0
    return avg_read, avg_write


# =============================================================================
# Parameter Normalization
# =============================================================================

def normalize_simplelevel_params(
    params: Mapping[str, Any],
    keys: list[str]
) -> dict[str, Any]:
    """Normalize SimpleLevels parameters from ruleset format.

    SimpleLevels from CheckMK rulesets returns: ('fixed', (warn, crit)) or ('no_levels', None)
    check_filesystem_levels expects: (warn, crit) or absent key

    Args:
        params: Original parameters from ruleset
        keys: List of parameter keys to normalize

    Returns:
        Normalized parameters dictionary
    """
    normalized = dict(params)
    for key in keys:
        if key not in normalized:
            continue
        value = normalized[key]
        if isinstance(value, tuple) and len(value) == 2:
            mode, levels = value
            if mode == 'fixed' and isinstance(levels, tuple):
                normalized[key] = levels
            elif mode in ('no_levels', 'predictive'):
                normalized.pop(key, None)
    return normalized


# =============================================================================
# Safe Data Access
# =============================================================================

def safe_get(data: dict, *keys, default: Any = None) -> Any:
    """Safely get nested dictionary value.

    Args:
        data: Dictionary to access
        *keys: Sequence of keys to traverse
        default: Default value if key not found

    Returns:
        Value at nested key path or default

    Example:
        safe_get(data, "PerformanceData", "TotalReads", default=0)
    """
    current = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current
