#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Andreas Doehler <andreas.doehler@bechtle.com/andreas.doehler@gmail.com>
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

"""checkmk special agent for netapp e-series via rest api"""

import logging
import sys
from collections import namedtuple
from pathlib import Path
from typing import Any, List

import requests
import urllib3
from cmk.special_agents.v0_unstable.agent_common import (SectionWriter,
                                                         special_agent_main)
from cmk.special_agents.v0_unstable.argument_parsing import (
    Args, create_default_argument_parser)
from cmk.utils import password_store


LOGGER = logging.getLogger("agent_netapp_e_series")

############
# ArgParse #
############


def parse_arguments(argv: List[str]) -> Args:
    sections = [
        "batteries",
        "controllers",
        "drawers",
        "drives",
        "esms",
        "fans",
        "interfaces",
        "pools",
        "powerSupplies",
        "system",
        "trays",
        "volumes",
        "thermalSensors",
    ]

    parser = create_default_argument_parser(description=__doc__)

    parser.add_argument(
        "-u", "--user", default=None, help="Username for E-Series Login", required=True
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s",
        "--password",
        default=None,
        help="""Password for E-Series Login""",
    )
    group.add_argument(
        "--password-id",
        default=None,
        help="""Password ID for E-Series Login""",
    )
    # optional
    parser.add_argument(
        "-P",
        "--proto",
        default="https",
        help="""Use 'http' or 'https' (default=https)""",
    )
    parser.add_argument(
        "-i", "--system-id", default=1, help="""Your E-Series System ID"""
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8443,
        type=int,
        help="Use alternative port (default: 8443)",
    )
    parser.add_argument(
        "-m",
        "--sections",
        default=sections,
        help="Comma separated list of data to query. Possible values: %s (default: all)"
        % ",".join(sections),
    )
    parser.add_argument(
        "-l",
        "--verify_ssl",
        action="store_true",
        default=False,
    )
    # debugging
#    parser.add_argument("-v", action="count", default=0)
#    parser.add_argument(
#        "--debug",
#        action="store_true",
#        help="Debug mode: let Python exceptions come through",
#    )
    parser.add_argument(
        "-w",
        "--write",
        action="store_true",
        default=False,
        help="""Write JSON File for debugging""",
    )
    # required
    parser.add_argument(
        "host",
        metavar="HOSTNAME",
        help="""IP address or hostname of your Netapp E-Series Controller""",
    )

    return parser.parse_args(argv)


def fetch_storage_data(session, sections, args, base_url, controller_ids):
    """
    fetches all data of the different sections and, if existent, adds the perfdata from the different e-series components.
    """

    hardware_inventory = session.get(
        base_url + "/hardware-inventory", verify=args.verify_ssl
    ).json()

    # Only used for debugging
    all_storage_data = {}

    for section in sections:
        # fetch data only for the activated sections
        if section.name in args.sections:
            LOGGER.debug(f"Fetching section {section.name}.")

            # Some hardware related sections (powersupplies,trays,fans...) are stored together in /hardware-inventory, so prevent fetching the same data from multiple sections
            if section.uri == "/hardware-inventory":
                section_data = hardware_inventory[section.name]
            else:
                # fetch data of the current section
                section_data = session.get(
                    base_url + section.uri, verify=args.verify_ssl
                ).json()

            # fetch performance data of current section if available and add it to the items
            if section.perfdata_uri is not None:
                try:
                    section_perfdata = session.get(
                        base_url + section.perfdata_uri, verify=args.verify_ssl
                    ).json()
                except requests.exceptions.JSONDecodeError as e:
                    LOGGER.debug(
                        f"Performance Data could not be handled: {e} - Sending empty section_perfdata."
                    )
                    section_perfdata = {}

                # Section "System" is the only section that is not a list with multiple json/dict items, but json itself, so we 'list' it, to not break our looping
                if section.name == "system":
                    perfdata = []
                    perfdata.append(section_perfdata)
                    result = []
                    result.append(section_data)
                    section_data = add_perfdata_to_section_data(
                        section, result, perfdata
                    )

                # add performance data to items
                else:
                    section_data = add_perfdata_to_section_data(
                        section, section_data, section_perfdata
                    )

            # Add checkmk item identifier
            section_data = add_checkmk_item_identifier(
                section, controller_ids, section_data
            )

            # Output current section
            sys.stdout.write("<<<netapp_eseries_%s:sep(0)>>>\n" % section.name.lower())
            handle_output(section_data)

            if args.write is True:

                # all_storage_data will contain all sections at the end of fetch_storage_data
                all_storage_data[section.name] = section_data


####################
# Helper functions #
####################


def get_session(args):

    if args.password is not None:
        password = args.password
    else:
        pw_id, pw_path = args.password_id.split(":")
        password = password_store.lookup(Path(pw_path), pw_id)

    session = requests.Session()
    session.auth = (args.user, password)
    session.verify = args.verify_ssl
    # print(session)
    return session


def get_label_of_id(id, controller_ids):
    return controller_ids[id]


def add_perfdata_to_section_data(section, storage_data, perfdata):
    """Adds the performance data to the json info of the objects"""
    identifier = None
    if section.name in ["volumes", "drives", "system", "controllers"]:
        identifier = "id"
    elif section.name == "interfaces":
        identifier = "interfaceRef"

    for list_counter, item in enumerate(storage_data):
        for perfitem in perfdata:
            if item[identifier] == perfitem[section.perfdata_identifier]:
                storage_data[list_counter]["performance"] = perfitem
                LOGGER.debug(
                    f"Performance Match : {item[identifier]} - Perfitem : {perfitem[section.perfdata_identifier]}"
                )
    return storage_data


def get_storage_id_2_name_mappings(args, session, base_url):
    """We need this to match the internal controller ids, e.g. tray and esm ids to the controller / ESM labels (A/B) and tray numbers (1-99)"""

    controllers = session.get(base_url + "/controllers", verify=args.verify_ssl).json()
    inventory = session.get(
        base_url + "/hardware-inventory", verify=args.verify_ssl
    ).json()

    LOGGER.debug("Mapping internal Reference IDs to labels and IDs:")

    storage_id_mappings = {}

    # TODO
    """
        ids = {
            'batteries' : {'batteryRef' : batteries[physicalLocation][slot]}
            'drawer' : {'drawerRef' : 'id'}
            'esms' : {'esmRef' : esm['physicalLocation']['label']}
            'fans' : {'fanRef' : fan['physicalLocation']['slot']}
            'powersupply' : {'powerSupplyRef' : powersupply['physicalLocation']['slot']}
            'trays' : {'trayRef' : 'trayid'}
        }
    """
    for controller in controllers:
        storage_id_mappings.update(
            {controller["controllerRef"]: controller["physicalLocation"]["label"]}
        )
        LOGGER.debug(
            f"Adding controller: {controller['controllerRef']} with Label {controller['physicalLocation']['label']}"
        )

    for drawer in inventory["drawers"]:
        storage_id_mappings.update({drawer["drawerRef"]: drawer["id"]})
        LOGGER.debug(
            f"Adding Drawer Ref: {drawer['drawerRef']} with ID {str(drawer['id'])}"
        )

    for tray in inventory["trays"]:
        storage_id_mappings.update({tray["trayRef"]: tray["trayId"]})
        LOGGER.debug(
            f"Adding Tray Ref: {tray['trayRef']} with ID {str(tray['trayId'])}"
        )

    for esm in inventory["esms"]:
        storage_id_mappings.update({esm["esmRef"]: esm["physicalLocation"]["label"]})
        LOGGER.debug(
            f"Adding ESM Ref: {esm['esmRef']} with Label {str(esm['physicalLocation']['label'])}"
        )

    for battery in inventory["batteries"]:
        storage_id_mappings.update(
            {battery["batteryRef"]: battery["physicalLocation"]["slot"]}
        )
        LOGGER.debug(
            f"Adding battery Ref: {battery['batteryRef']} with Label {str(battery['physicalLocation']['label'])}"
        )

    for fan in inventory["fans"]:
        storage_id_mappings.update({fan["fanRef"]: fan["physicalLocation"]["slot"]})
        LOGGER.debug(
            f"Adding fan Ref: {fan['fanRef']} with Label {str(fan['physicalLocation']['label'])}"
        )

    for powersupply in inventory["powerSupplies"]:
        storage_id_mappings.update(
            {powersupply["powerSupplyRef"]: powersupply["physicalLocation"]["slot"]}
        )
        LOGGER.debug(
            f"Adding powersupply Ref: {powersupply['powerSupplyRef']} with Label {str(powersupply['physicalLocation']['label'])}"
        )

    return storage_id_mappings


def add_checkmk_item_identifier(section, controller_ids, section_data):
    """Adds a persistent identifier "checkmk_item_identifier" to the dict of the monitored items, which is used as the "item" to create the service name"""

    interface_type_mapping = {
        "fc": "fibre",
        "sas": "sas",
        "iscsi": "iscsi",
        "pcie": "pcie",
        'ib': 'ib'
    }

    unique_identifier = ""

    for list_counter, item in enumerate(section_data):

        try:
            if item["physicalLocation"]["trayRef"]:
                enclosure_type = "Tray"
                enclosure_id = str(
                    get_label_of_id(item["physicalLocation"]["trayRef"], controller_ids)
                )
            elif item["physicalLocation"]["drawerRef"]:
                enclosure_type = "Drawer"
                enclosure_id = str(
                    get_label_of_id(
                        item["physicalLocation"]["drawerRef"], controller_ids
                    )
                )
        except KeyError:
            pass

        if section.name in ["volumes", "pools"]:
            unique_identifier = item["label"]

        elif section.name == "system":
            unique_identifier = item["name"]

        elif section.name in ["controllers", "drawers"]:
            unique_identifier = item["physicalLocation"]["label"]

        elif section.name == "interfaces":
            interface_type = item["ioInterfaceTypeData"]["interfaceType"]
            controller = get_label_of_id(item["controllerRef"], controller_ids)
            channel = str(
                item["ioInterfaceTypeData"][interface_type_mapping[interface_type]][
                    "channel"
                ]
            )
            unique_identifier = "%s %s-%s" % (
                interface_type.upper(),
                controller,
                channel,
            )

        elif section.name == "drives":
            slot = str(item["physicalLocation"]["slot"])
            unique_identifier = enclosure_id + "-" + slot

        elif section.name == "trays":
            unique_identifier = str(item["trayId"])

        else:
            slot = str(item["physicalLocation"]["slot"])
            unique_identifier = "%s %s-%s" % (enclosure_type, enclosure_id, slot)

        section_data[list_counter]["checkmk_item_identifier"] = unique_identifier

    return section_data


def handle_output(data):
    output_dict = {}
    for element in data:
        output_dict.setdefault(element["checkmk_item_identifier"].strip(), element)
    sys.stdout.write(str(output_dict) + "\n")


########
# MAIN #
########


def agent_netapp_eseries_main(args: Any = None) -> int:

    Section = namedtuple(
        "Section", ["name", "uri", "perfdata_uri", "perfdata_identifier"]
    )
    sections = [
        Section(
            name="batteries",
            uri="/hardware-inventory",
            perfdata_uri=None,
            perfdata_identifier=None,
        ),
        Section(
            name="controllers",
            uri="/controllers",
            perfdata_uri="/analysed-controller-statistics",
            perfdata_identifier="controllerId",
        ),
        Section(
            name="drawers",
            uri="/hardware-inventory",
            perfdata_uri=None,
            perfdata_identifier=None,
        ),
        Section(
            name="drives",
            uri="/drives",
            perfdata_uri="/analysed-drive-statistics",
            perfdata_identifier="diskId",
        ),
        Section(
            name="esms",
            uri="/hardware-inventory",
            perfdata_uri=None,
            perfdata_identifier=None,
        ),
        Section(
            name="fans",
            uri="/hardware-inventory",
            perfdata_uri=None,
            perfdata_identifier=None,
        ),
        Section(
            name="interfaces",
            uri="/interfaces",
            perfdata_uri="/analysed-interface-statistics",
            perfdata_identifier="interfaceId",
        ),
        Section(
            name="pools",
            uri="/storage-pools",
            perfdata_uri=None,
            perfdata_identifier=None,
        ),
        Section(
            name="powerSupplies",
            uri="/hardware-inventory",
            perfdata_uri=None,
            perfdata_identifier=None,
        ),
        Section(
            name="system",
            uri="/",
            perfdata_uri="/analysed-system-statistics",
            perfdata_identifier="storageSystemId",
        ),
        Section(
            name="trays",
            uri="/hardware-inventory",
            perfdata_uri=None,
            perfdata_identifier=None,
        ),
        Section(
            name="volumes",
            uri="/volumes",
            perfdata_uri="/analysed-volume-statistics",
            perfdata_identifier="volumeId",
        ),
        Section(
            name="thermalSensors",
            uri="/hardware-inventory",
            perfdata_uri=None,
            perfdata_identifier=None,
        ),
    ]

    if not args.verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    logging.basicConfig(
        format="%(levelname)s %(asctime)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level={0: logging.WARN, 1: logging.INFO, 2: logging.DEBUG}.get(
            args.verbose, logging.DEBUG
        ),
    )

    LOGGER.debug(
        "Calling special agent netapp e-series with parameters: %s", args.__repr__()
    )

    # Start REST Session Object
    session = get_session(args)

    # Base URL for all requests
    base_url = f"{args.proto}://{args.host}:{str(args.port)}/devmgr/v2/storage-systems/{str(args.system_id)}"

    try:
        result = session.get(
            base_url,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            verify=args.verify_ssl,
        )
        result.raise_for_status()

    except requests.exceptions.RequestException as e:
        sys.stderr.write("Error: %s\n" % e)
        if args.debug:
            raise
        sys.exit(1)

    controller_ids = get_storage_id_2_name_mappings(args, session, base_url)

    fetch_storage_data(session, sections, args, base_url, controller_ids)


def main() -> int:
    """Main entry point to be used"""
    return special_agent_main(parse_arguments, agent_netapp_eseries_main)


if __name__ == "__main__":
    main()
