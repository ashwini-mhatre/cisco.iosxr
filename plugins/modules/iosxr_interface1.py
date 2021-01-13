#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for iosxr_interface1
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: interface1
version_added: 2.9
short_description: Manage interface attributes on Cisco IOS-XR network devices
description: This module manages the interface attributes on Cisco IOS-XR network devices.
author: Ashwini Mhatre
options:
  config:
    description: A dictionary of interface options
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Full name of the interface to configure in C(type + path) format. e.g. C(GigabitEthernet0/0/0/0)
        type: str
        required: True
      description:
        description:
          - Interface description.
        type: str
      enable:
        default: True
        description:
          - Administrative state of the interface.
          - Set the value to C(True) to administratively enable the interface or C(False) to disable it.
        type: bool
  state:
    choices:
      - merged
      - replaced
      - overridden
      - deleted
    default: merged
    description:
      - The state the configuration should be left in
    type: str
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.argspec.interface1.interface1 import (
    Interface1Args,
)
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.config.interface1.interface1 import (
    Interface1,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Interface1Args.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Interface1(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
