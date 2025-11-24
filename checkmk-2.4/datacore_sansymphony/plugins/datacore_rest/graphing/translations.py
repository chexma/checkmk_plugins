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
Graphing translations for DataCore SANsymphony pool capacity metrics.

The check_filesystem_levels() function outputs metrics in MB, but the
CheckMK graphing system expects fs_used, fs_size, fs_free in bytes.
This translation scales the metrics by 1048576 (1024^2) to convert MB to bytes.
"""

from cmk.graphing.v1.translations import PassiveCheck, RenameToAndScaleBy, ScaleBy, Translation

# 1 MiB = 1024 * 1024 = 1048576 bytes
MIB = 1048576

translation_datacore_rest_pool_capacity = Translation(
    name="datacore_rest_pool_capacity",
    check_commands=[PassiveCheck("datacore_rest_pool_capacity")],
    translations={
        "fs_used": ScaleBy(MIB),
        "fs_size": ScaleBy(MIB),
        "fs_free": ScaleBy(MIB),
        "reserved": ScaleBy(MIB),
        "uncommitted": ScaleBy(MIB),
        "overprovisioned": ScaleBy(MIB),
        "growth": RenameToAndScaleBy("fs_growth", MIB / 86400.0),
        "trend": RenameToAndScaleBy("fs_trend", MIB / 86400.0),
        "trend_hoursleft": ScaleBy(3600),
    },
)
