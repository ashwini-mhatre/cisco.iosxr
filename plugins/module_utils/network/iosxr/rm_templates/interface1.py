# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The Interface1 parser templates file. This contains 
a list of parser definitions and associated functions that 
facilitates both facts gathering and native command generation for 
the given network resource.
"""

import re
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.network_template import (
    NetworkTemplate,
)


def tmplt_enabled(config_data):
    command = ""
    if "enable" in config_data:
        if config_data["enable"]:
            command = "no interface " + config_data["name"] + " shutdown"
        else:
            command = "interface" + config_data["name"] + "shutdown"

    return command


def test(data):
    cmd = "show interface"
    return cmd

class Interface1Template(NetworkTemplate):
    def __init__(self, lines=None):
        super(Interface1Template, self).__init__(lines=lines, tmplt=self)

    # fmt: off
    PARSERS = [
        {
            "name": "name",
            "getval": re.compile(
                r"""
                ^interface\s(preconfigure\s)?(?P<interface>\S+)
                $""", re.VERBOSE),
            "setval": "interface {{ interface}}",
            "result": {
                "{{interface}}":
                    {
                        "name": "{{ interface }}"
                    }
            },
            "shared": True
        },
        {
            "name": "description",
            "getval": re.compile(
                r"""
                \sdescription\s(?P<description>.*)
                $""", re.VERBOSE),
            "setval": "interface {{name}} description {{ description }}",
            "result": {
                "{{interface}}":
                    {
                        "description": "{{ description }}"
                    }
            },
        },
        {
            "name": "enable",
            "getval": re.compile(
                r"""
                \s+shutdown(?P<shutdown>)
                $""", re.VERBOSE),
            "setval": tmplt_enabled,
            "result": {
                "{{interface}}":
                    {
                        "enable": "{{ False if shutdown is defined }}"
                    }
            },
        }
    ]
    # fmt: on
