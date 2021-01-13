# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The iosxr interface1 fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.rm_templates.interface1 import (
    Interface1Template,
)
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.argspec.interface1.interface1 import (
    Interface1Args,
)

class Interface1Facts(object):
    """ The iosxr interface1 facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = Interface1Args.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Interface1 network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = connection.get("show running-config interface")

        # parse native config using the Interface1 template
        interface1_parser = Interface1Template(lines=data.splitlines())
        objs = list(interface1_parser.parse().values())
        #import epdb;epdb.serve()

        ansible_facts['ansible_network_resources'].pop('interface1', None)

        params = utils.remove_empties(
            utils.validate_config(self.argument_spec, {"config": objs})
        )

        facts['interface1'] = params['config']
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
