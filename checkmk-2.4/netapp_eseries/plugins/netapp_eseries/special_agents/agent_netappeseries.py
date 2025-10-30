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
import time
from collections import namedtuple
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import requests
import urllib3
from cmk.special_agents.v0_unstable.agent_common import (SectionWriter,
                                                         special_agent_main)
from cmk.special_agents.v0_unstable.argument_parsing import (
    Args, create_default_argument_parser)
from cmk.utils import password_store


LOGGER = logging.getLogger("agent_netapp_e_series")

# API endpoint mapping: old British spelling to new American spelling
OLD_TO_NEW_ENDPOINT_MAP = {
    "/analysed-controller-statistics": "/analyzed/controller-statistics",
    "/analysed-drive-statistics": "/analyzed/drive-statistics",
    "/analysed-interface-statistics": "/analyzed/interface-statistics",
    "/analysed-volume-statistics": "/analyzed/volume-statistics",
    "/analysed-system-statistics": "/analyzed/system-statistics",
}


####################
# Retry Utility    #
####################

def retry_request(func: Callable, max_retries: int = 3, initial_delay: float = 1, backoff_factor: float = 2) -> requests.Response:
    """
    Retry a request function with exponential backoff.

    Args:
        func: Function to execute (should return requests.Response)
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds between retries
        backoff_factor: Multiplier for delay on each retry

    Returns:
        Response object if successful

    Raises:
        Last exception if all retries fail
    """
    last_exception = None
    delay = initial_delay

    for attempt in range(max_retries):
        try:
            return func()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError) as e:
            last_exception = e

            # Don't retry on client errors (4xx except 429) or if it's the last attempt
            if attempt == max_retries - 1:
                break

            if isinstance(e, requests.exceptions.HTTPError):
                # Retry on 429 (Too Many Requests) and 5xx server errors
                if e.response.status_code < 429 or (e.response.status_code >= 400 and e.response.status_code < 500 and e.response.status_code != 429):
                    break

            LOGGER.debug(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {delay}s...")
            time.sleep(delay)
            delay *= backoff_factor
        except Exception as e:
            # Don't retry on unexpected exceptions
            raise

    # All retries exhausted
    raise last_exception

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
    # required
    parser.add_argument(
        "host",
        metavar="HOSTNAME",
        help="""IP address or hostname of your Netapp E-Series Controller""",
    )

    return parser.parse_args(argv)


def fetch_storage_data(session: requests.Session, sections: List[Any], args: Args, base_url: str, controller_ids: Dict[str, Any]) -> None:
    """
    fetches all data of the different sections and, if existent, adds the perfdata from the different e-series components.
    """

    # Fetch hardware inventory with error handling
    try:
        hardware_inventory = session.get(
            base_url + "/hardware-inventory",
            verify=args.verify_ssl,
            timeout=30
        ).json()
    except requests.exceptions.RequestException as e:
        LOGGER.error(f"Failed to fetch hardware inventory: {e}")
        sys.stderr.write(f"Error: Could not fetch hardware inventory: {e}\n")
        if args.debug:
            raise
        return
    except requests.exceptions.JSONDecodeError as e:
        LOGGER.error(f"Invalid JSON response from hardware inventory: {e}")
        sys.stderr.write(f"Error: Invalid JSON from hardware inventory API\n")
        if args.debug:
            raise
        return

    for section in sections:
        # fetch data only for the activated sections
        if section.name in args.sections:
            LOGGER.debug(f"Fetching section {section.name}.")

            # Some hardware related sections (powersupplies,trays,fans...) are stored together in /hardware-inventory, so prevent fetching the same data from multiple sections
            if section.uri == "/hardware-inventory":
                try:
                    section_data = hardware_inventory[section.name]
                except KeyError as e:
                    LOGGER.error(f"Section {section.name} not found in hardware inventory: {e}")
                    sys.stderr.write(f"Warning: Section {section.name} not available in hardware inventory\n")
                    continue
            else:
                # fetch data of the current section with error handling
                try:
                    section_data = session.get(
                        base_url + section.uri,
                        verify=args.verify_ssl,
                        timeout=30
                    ).json()
                except requests.exceptions.RequestException as e:
                    LOGGER.error(f"Failed to fetch section {section.name} from {section.uri}: {e}")
                    sys.stderr.write(f"Warning: Could not fetch section {section.name}: {e}\n")
                    continue
                except requests.exceptions.JSONDecodeError as e:
                    LOGGER.error(f"Invalid JSON response for section {section.name}: {e}")
                    sys.stderr.write(f"Warning: Invalid JSON for section {section.name}\n")
                    continue

            # fetch performance data of current section if available and add it to the items
            if section.perfdata_uri is not None:
                # Use new helper function that handles both old and new API formats
                section_perfdata = fetch_performance_data(session, base_url, section, args)

                # Section "System" is the only section that is not a list with multiple json/dict items
                # We need to wrap section_data in a list for consistent processing
                if section.name == "system":
                    result = []
                    result.append(section_data)
                    section_data = add_perfdata_to_section_data(
                        section, result, section_perfdata
                    )
                # add performance data to items for list-based sections
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


####################
# Helper functions #
####################


def get_session(args: Args) -> requests.Session:

    if args.password is not None:
        password = args.password
    else:
        pw_id, pw_path = args.password_id.split(":")
        password = password_store.lookup(Path(pw_path), pw_id)

    session = requests.Session()
    session.auth = (args.user, password)
    session.verify = args.verify_ssl
    return session


def get_label_of_id(id: str, controller_ids: Dict[str, Any]) -> Any:
    return controller_ids[id]


def fetch_performance_data(session: requests.Session, base_url: str, section: Any, args: Args) -> List[Dict[str, Any]]:
    """
    Fetches performance data using new API format first, falls back to old format.
    Handles the response structure differences automatically.

    Returns: list of performance data items (unwrapped from 'statistics' if needed)
    """

    new_endpoint = OLD_TO_NEW_ENDPOINT_MAP.get(section.perfdata_uri)
    perfdata = None

    # Try new API format first
    if new_endpoint:
        try:
            LOGGER.debug(f"Trying new API endpoint: {new_endpoint}")
            response = session.get(
                base_url + new_endpoint,
                params={"statisticsFetchTime": 60},
                verify=args.verify_ssl
            )

            if response.status_code == 200:
                data = response.json()
                # New API wraps data in "statistics" key
                if isinstance(data, dict) and "statistics" in data:
                    perfdata = data["statistics"]
                    LOGGER.debug(f"Successfully fetched {len(perfdata)} items from new API endpoint")
                else:
                    LOGGER.warning(f"Unexpected response format from new API: {type(data)}")

            elif response.status_code == 404:
                LOGGER.debug(f"New API endpoint not found (404), will try old endpoint")
            elif response.status_code == 422:
                # Insufficient statistics data - this is OK, return empty
                LOGGER.info(f"Insufficient statistics data for {section.name}, returning empty perfdata")
                return []
            else:
                LOGGER.warning(f"New API returned status {response.status_code}, will try old endpoint")

        except requests.exceptions.RequestException as e:
            LOGGER.debug(f"Error fetching from new API endpoint: {e}, will try old endpoint")
        except requests.exceptions.JSONDecodeError as e:
            LOGGER.debug(f"JSON decode error from new API: {e}, will try old endpoint")

    # Try old API format if new didn't work
    if perfdata is None:
        try:
            LOGGER.debug(f"Trying old API endpoint: {section.perfdata_uri}")
            response = session.get(
                base_url + section.perfdata_uri,
                verify=args.verify_ssl,
                timeout=30
            )

            if response.status_code == 200:
                perfdata = response.json()
                # Old API returns data directly (list or dict)
                # Convert single dict to list for consistent handling
                if isinstance(perfdata, dict):
                    perfdata = [perfdata]
                LOGGER.debug(f"Successfully fetched {len(perfdata)} items from old API endpoint")
            else:
                LOGGER.warning(f"Old API returned status {response.status_code}")

        except requests.exceptions.RequestException as e:
            LOGGER.warning(f"Error fetching from old API endpoint: {e}")
        except requests.exceptions.JSONDecodeError as e:
            LOGGER.warning(f"JSON decode error from old API: {e}")

    # Return empty list if all attempts failed
    if perfdata is None:
        LOGGER.warning(f"Could not fetch performance data for {section.name} from either API version")
        return []

    return perfdata


def add_perfdata_to_section_data(section: Any, storage_data: List[Dict[str, Any]], perfdata: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Adds the performance data to the json info of the objects"""
    identifier = None
    if section.name in ["volumes", "drives", "system", "controllers"]:
        identifier = "id"
    elif section.name == "interfaces":
        identifier = "interfaceRef"

    # Build performance data index for O(1) lookup instead of O(n×m) nested loop
    # This improves performance significantly for large datasets
    perfdata_map = {}
    for perfitem in perfdata:
        perf_id = perfitem.get(section.perfdata_identifier)
        if perf_id is not None:
            perfdata_map[perf_id] = perfitem

    # Match storage items with performance data using index
    for list_counter, item in enumerate(storage_data):
        item_id = item.get(identifier)
        if item_id is not None and item_id in perfdata_map:
            storage_data[list_counter]["performance"] = perfdata_map[item_id]
            LOGGER.debug(
                f"Performance Match : {item_id} - Perfitem : {item_id}"
            )

    return storage_data


def get_storage_id_2_name_mappings(args: Args, session: requests.Session, base_url: str) -> Dict[str, Any]:
    """We need this to match the internal controller ids, e.g. tray and esm ids to the controller / ESM labels (A/B) and tray numbers (1-99)"""

    controllers = session.get(base_url + "/controllers", verify=args.verify_ssl, timeout=30).json()
    inventory = session.get(
        base_url + "/hardware-inventory", verify=args.verify_ssl, timeout=30
    ).json()

    LOGGER.debug("Mapping internal Reference IDs to labels and IDs:")

    storage_id_mappings = {}

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


def add_checkmk_item_identifier(section: Any, controller_ids: Dict[str, Any], section_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
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
        # Initialize variables to prevent UnboundLocalError
        enclosure_type = "Unknown"
        enclosure_id = "Unknown"

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
            # If physicalLocation data is missing, keep default "Unknown" values
            pass

        # Build unique identifier with safe dict access to prevent KeyError
        try:
            if section.name in ["volumes", "pools"]:
                unique_identifier = item.get("label", f"Unknown-{list_counter}")

            elif section.name == "system":
                unique_identifier = item.get("name", "Unknown")

            elif section.name in ["controllers", "drawers"]:
                unique_identifier = item.get("physicalLocation", {}).get("label", f"Unknown-{list_counter}")

            elif section.name == "interfaces":
                interface_data = item.get("ioInterfaceTypeData", {})
                interface_type = interface_data.get("interfaceType", "unknown")
                controller_ref = item.get("controllerRef")

                if controller_ref and controller_ref in controller_ids:
                    controller = controller_ids[controller_ref]
                else:
                    controller = "Unknown"

                # Get channel from nested interface type data
                interface_type_key = interface_type_mapping.get(interface_type, interface_type)
                channel = str(interface_data.get(interface_type_key, {}).get("channel", 0))

                unique_identifier = "%s %s-%s" % (
                    interface_type.upper(),
                    controller,
                    channel,
                )

            elif section.name == "drives":
                slot = str(item.get("physicalLocation", {}).get("slot", "Unknown"))
                unique_identifier = enclosure_id + "-" + slot

            elif section.name == "trays":
                unique_identifier = str(item.get("trayId", f"Unknown-{list_counter}"))

            else:
                slot = str(item.get("physicalLocation", {}).get("slot", "Unknown"))
                unique_identifier = "%s %s-%s" % (enclosure_type, enclosure_id, slot)

        except Exception as e:
            # Catch any unexpected errors and provide a fallback identifier
            LOGGER.warning(f"Error building identifier for {section.name} item {list_counter}: {e}")
            unique_identifier = f"{section.name}-{list_counter}"

        section_data[list_counter]["checkmk_item_identifier"] = unique_identifier

    return section_data


def handle_output(data: List[Dict[str, Any]]) -> None:
    output_dict = {}
    for element in data:
        output_dict.setdefault(element["checkmk_item_identifier"].strip(), element)
    sys.stdout.write(str(output_dict) + "\n")


########
# MAIN #
########


def agent_netapp_eseries_main(args: Args) -> int:

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
            timeout=30
        )
        result.raise_for_status()

    except requests.exceptions.RequestException as e:
        sys.stderr.write("Error: %s\n" % e)
        if args.debug:
            raise
        sys.exit(1)

    controller_ids = get_storage_id_2_name_mappings(args, session, base_url)

    fetch_storage_data(session, sections, args, base_url, controller_ids)

    return 0


def main() -> int:
    """Main entry point to be used"""
    return special_agent_main(parse_arguments, agent_netapp_eseries_main)


if __name__ == "__main__":
    main()
