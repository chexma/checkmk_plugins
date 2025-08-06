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

import logging
import sys
from collections import namedtuple
from pathlib import Path
from typing import Any, List

import requests
from cmk.special_agents.v0_unstable.agent_common import (SectionWriter,
                                                         special_agent_main)
from cmk.special_agents.v0_unstable.argument_parsing import (
    Args, create_default_argument_parser)
from cmk.utils import password_store


def parse_arguments(argv: List[str]) -> Args:
    sections = [
        "alerts",
        "hosts",
        "hostgroups",
        "physicaldisks",
        "pools",
        "ports",
        "servergroups",
        "servers",
        "snapshots",
        "virtualdisks",
    ]

    parser = create_default_argument_parser(description=__doc__)

    parser.add_argument(
        "-u", "--user",
        help="Username for DataCore Sansymphony V Login", 
        required=True
    )
    parser.add_argument(
        "-s",
        "--password_id",
        help="Password ID for DataCore Sansymphony V Login",
        required=True
    )
    parser.add_argument(
        "-n",
        "--nodename",
        help="DataCore Node to fetch data for",
        required=True
    )
    parser.add_argument(
        "-P",
        "--proto",
        default="https",
        help="Use 'http' or 'https' (default=https)",
    )
    parser.add_argument(
        "-m",
        "--sections",
        default=sections,
        help=f"Comma separated list of data to query. Possible values: {','.join(sections)} (default: all)",
    )
    parser.add_argument(
        "-l",
        "--verify_ssl",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "host",
        metavar="HOSTNAME",
        help="IP address or hostname of your DataCore Server",
    )

    return parser.parse_args(argv)


def get_session(args):
    """Create requests session"""
    pw_id, pw_path = args.password_id.split(":")
    password = password_store.lookup(Path(pw_path), pw_id)

    session = requests.Session()
    session.auth = (args.user, password)
    session.verify = args.verify_ssl
    return session


def get_objects(object_name, api_url_base, headers, session, args):
    """Get section data e.g. virtualdisk, pools"""
    try:
        logging.debug(f"Fetching the whole section {object_name} : {api_url_base}/{object_name}")
        response = session.get(f'{api_url_base}/{object_name}', headers=headers, timeout=5, verify=args.verify_ssl)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching {object_name} section: {e}")
        sys.exit(1)


def request_object_perfdata(object, api_url_base, headers, session, args):
    """Get perfdata for specific objects"""
    try:
        logging.debug(f"Fetching performance data of single object: {api_url_base}/performance/{object['Id']}")
        response = session.get(f'{api_url_base}/performance/{object["Id"]}', headers=headers, timeout=5, verify=args.verify_ssl)
        response.raise_for_status()
        perfdata = response.json()

        if perfdata:
            object["PerformanceData"] = perfdata[0]
        else:
            logging.warning(f"No performance data returned for object ID: {object['Id']}")
            object["PerformanceData"] = None

        return object
    except requests.RequestException as e:
        logging.error(f"Error fetching performance data for object ID {object['Id']}: {e}")
        object["PerformanceData"] = None
        return object


def add_perfdata(objects, api_url_base, headers, session, args):
    """Add Perfdata to objects"""
    result = []
    for item in objects:
        updated_object = request_object_perfdata(item, api_url_base, headers, session, args)
        result.append(updated_object)
    return result


def caption_from_id(id, json_data):
    """Get Caption for a given ID"""
    for item in json_data:
        if item["Id"] == id:
            return str(item["Caption"])


def get_id_of_servername(servername, api_url_base, headers, session, args):
    """Get Server ID for a given SSV Servername"""
    servers = get_objects('servers', api_url_base, headers, session, args)
    for server in servers:
        if server['Caption'].lower() == servername.lower():
            logging.debug(f"Servername: {server['Caption']} - Server ID: {server['Id']}")
            return server['Id']


def agent_datacore_rest_main(args: Any = None) -> int:
    """Main Special Agent"""

    print(args)

    Section = namedtuple(
        "Section", ["name", "api_version", "has_perfdata", "item_identifier"]
    )
    sections = [
        Section(
            name="alerts",
            api_version=1,
            has_perfdata=False,
            item_identifier=None),
        Section(
            name="hosts",
            api_version=2,
            has_perfdata=True,
            item_identifier=None),
        Section(
            name="hostgroups",
            api_version=1,
            has_perfdata=True,
            item_identifier=None),
        Section(
            name="physicaldisks",
            api_version=2,
            has_perfdata=True,
            item_identifier='HostId'),
        Section(
            name="pools",
            api_version=2,
            has_perfdata=True,
            item_identifier='ServerId'),
        Section(
            name="ports",
            api_version=1,
            has_perfdata=True,
            item_identifier='HostId'),
        Section(
            name="servergroups",
            api_version=1,
            has_perfdata=False,
            item_identifier=None),
        Section(
            name="servers",
            api_version=2,
            has_perfdata=True,
            item_identifier='Id'),
        Section(
            name="snapshots",
            api_version=1,
            has_perfdata=False,
            item_identifier=None),
        Section(
            name="virtualdisks",
            api_version=2,
            has_perfdata=True,
            item_identifier=None),
    ]

    # Session erstellen
    session = get_session(args)

    pw_id, pw_path = args.password_id.split(":")
    password = password_store.lookup(Path(pw_path), pw_id)

    headers = {'ServerHost': args.nodename, 'Authorization': 'Basic ' + args.user + " " + password}
    base_api_url = f"{args.proto}://{args.host}/RestService/rest.svc"

    my_server_id = get_id_of_servername(args.nodename, f"{base_api_url}/1.0", headers, session, args)

    resources_dict = {}

    for section in sections:
        if section.name in args.sections:
            api_url_base = f"{base_api_url}/{section.api_version}.0"
            whole_section = get_objects(section.name, api_url_base, headers, session, args)

            if section.has_perfdata and section.api_version == 1:
                resources_dict[section.name] = add_perfdata(whole_section, api_url_base, headers, session, args)

            # this can be optimized :  (physicaldisks api version is 2 but its perfdata is only available in 1...)
            if section.name == 'physicaldisks':
                api_url_base = f"{args.proto}://{args.host}/RestService/rest.svc/1.0"
                resources_dict[section.name] = add_perfdata(whole_section, api_url_base, headers, session, args)
            else:
                resources_dict[section.name] = whole_section

    # Create Header for labels
    sys.stdout.write("<<<check_mk>>>\n")
    sys.stdout.write("Version: 2.3\n")
    # manager_os = []
    # if isinstance(manager_data, dict):
    
    sys.stdout.write("OSType: Storage\n")
    sys.stdout.write("OSName: SANsymphony\n")
    # get that from the resources_dict
    sys.stdout.write("OSVersion: SANsymphony\n")
    sys.stdout.write("OSPlatform: DataCore\n")
    
    for section in sections:
        if section.name in resources_dict:
            if section.name in ['alerts', 'snapshots']:
                with SectionWriter(f"datacore_rest_{section.name}") as writer:
                    writer.append_json(resources_dict[section.name])
            else:
                for item in resources_dict[section.name]:
                    if section.name == 'virtualdisks':
                        if not item['IsSnapshotVirtualDisk'] and (item['FirstHostId'] == my_server_id or item['SecondHostId'] == my_server_id):
                            with SectionWriter(f"datacore_rest_{section.name}") as writer:
                                writer.append_json(item)
                    elif section.name == 'ports':
                        if item[section.item_identifier] == my_server_id and "Loopback" not in item['Caption']:
                            with SectionWriter(f"datacore_rest_{section.name}") as writer:
                                writer.append_json(item)
                    elif section.item_identifier:
                        if item[section.item_identifier] == my_server_id:
                            with SectionWriter(f"datacore_rest_{section.name}") as writer:
                                writer.append_json(item)
                    else:
                        with SectionWriter(f"datacore_rest_{section.name}") as writer:
                            writer.append_json(item)


def main() -> int:
    """Main entry point to be used"""
    return special_agent_main(parse_arguments, agent_datacore_rest_main)


if __name__ == '__main__':
    main()
