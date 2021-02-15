#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for iosxr_bgp_neighbor_address_family
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: iosxr_bgp_global
short_description: Manages BGP global resource module.
description:
- This module configures and manages the attributes of BGP global on Cisco IOS-XR platforms.
version_added: 2.0.0
author: Ashwini Mhatre (amhatre)
notes:
- Tested against Cisco IOS-XR 6.1.3.
- This module works with connection C(network_cli).
options:
    config:
      description: A list of configurations for BGP address family.
      type: dict
      suboptions:
        AS_number:
          description: Autonomous system number.
          type: str
        neighbors:
          neighbors: &neighbors
            description: Specify a neighbor router.
            type: list
            elements: dict
            suboptions:
              neighbor:
                description:
                  - Neighbor router address.
                type: str
                required: true
              remote_as:
                description:
                type: int
              address_family:
                description: Enable address family and enter its config mode
                type: list
                elements: dict
                suboptions:
                  afi: &afi
                    description: address family.
                    type: str
                    choices: [ 'ipv4', 'ipv6']
                  af_modifier:
                    description: Address Family modifier
                    type: str
                    choices: [ 'flowspec', 'mdt', 'multicast', 'mvpn', 'rt-filter', 'tunnel', 'unicast', 'labeled-unicast' ]
                  advertise_permanent_network:
                    type: bool
                    description: Per neighbor advertisement options.
                  aigp:
                    description: AIGP attribute
                    type: dict
                    suboptions:
                      disable:
                        description: Ignore AIGP attribute.
                        type: bool
                      set:
                        description: Set AIGP attribute.
                        type: bool
                      send_cost_community_disable:
                        description: send AIGP attribute.
                        type: bool
                      send_med:
                        set:
                          type: bool
                          description: set Send AIGP value in MED.
                        disable:
                          description: disable Send AIGP value in MED.
                          type: bool
                  allowas_in: &allowas_in
                    type: dict
                    description: Allow as-path with my AS present in it.
                    suboptions:
                      value:
                        type: int
                        description: Number of occurences of AS number 1-10.
                      set:
                        type: bool
                        description: set allowas_in
                  as_overrride: &as_override
                    type: dict
                    description: Override matching AS-number while sending update
                    suboptions:
                      set:
                        type: bool
                        description: set as_override
                      inheritance_disable:
                        type: bool
                        description: Prevent as-override from being inherited from the parent.
                  bestpath_origin_as_allow_invalid:
                    type: bool
                    description: Change default route selection criteria.Allow BGP origin-AS knobs.
                  capability_orf_prefix: &capability
                    type: str
                    description: Advertise address prefix ORF capability to this neighbor.
                    choices: ['both', 'send', 'none', 'receive']
                  default_originate: &default_originate
                    type: dict
                    description: Originate default route to this neighbor.
                    suboptions:
                      set:
                        type: bool
                        description: set default route.
                      route_policy:
                        type: str
                        description: Route policy to specify criteria to originate default
                      inheritance_disable:
                        type: bool
                        description: Prevent default-originate from being inherited from the parent.
                  long_lived_graceful_restart: &long_lived_graceful_restart
                    type: dict
                    description: Enable long lived graceful restart support.
                    suboptions:
                      capable:
                        type: bool
                        description: Treat neighbor as LLGR capable.
                      stale_time_send:
                        type: int
                        description: Maximum time to wait before purging long-lived stale routes.
                  maximum_prefix: &maximum_prefix
                    type: dict
                    description: Maximum number of prefixes to accept from this peer.
                    suboptions:
                      max_limit:
                        type: int
                        description:  maximum no. of prefix limit.<1-4294967295.
                      threshold_value:
                        type: int
                        description: hreshold value (%) at which to generate a warning msg <1-100>.
                      restart:
                        type: int
                        description: Restart time interval.
                      warning_only:
                        type: bool
                        description: Only give warning message when limit is exceeded.
                      discard_extra_paths:
                        description: Discard extra paths when limit is exceeded.
                        type: bool
                  multipath: &multipath
                    type: bool
                    description: Paths from this neighbor is eligible for multipath.
                  next_hop_self: &next_hop_self
                    type: dict
                    description: Disable the next hop calculation for this neighbor.
                    suboptions:
                      set:
                        type: bool
                        description: set next hop self.
                      inheritance_disable:
                        type: bool
                        description: Prevent next_hop_self from being inherited from the parent.
                  next_hop_unchanged: &next_hop_unchanged
                    type: dict
                    description: Disable the next hop calculation for this neighbor.
                    suboptions:
                      set:
                        type: bool
                        description: set next hop unchanged.
                      inheritance_disable:
                        type: bool
                        description: Prevent next_hop_unchanged from being inherited from the parent.
                      multipath:
                        type: bool
                        description: Do not overwrite nexthop before advertising multipaths.
                  optimal_route_reflection_group_name: &optimal_route_reflection
                    type: str
                    description: Configure optimal-route-reflection group.
                  orf_route_policy: &orf_route_policy
                    type: str
                    description: Specify ORF and inbound filtering criteria.'
                  origin_as:
                    description: BGP origin-AS knobs.
                    type: dict
                    suboptions:
                      validation:
                        description: BGP origin-AS validation knobs.
                        type: dict
                        suboptions:
                          disable:
                            description: Disable RPKI origin-AS validation.
                            type: bool
                  remove_private_AS: &remove_private_AS
                    type: dict
                    description: Remove private AS number from outbound updates.
                    suboptions:
                      set:
                        type: bool
                        description: set remove private As.
                      inbound:
                        type: bool
                        description: Remove private AS number from inbound updates.
                      entire_aspath:
                        type: bool
                        description: remove only if all ASes in the path are private.
                      inheritance_disable:
                        type: bool
                        description: Prevent remove-private-AS from being inherited from the parent.
                  route_policy: &route_policy
                    type: str
                    description: Apply route policy to neighbor.
                  route_reflector_client: &route_reflector_client
                    type: dict
                    description:  Configure a neighbor as Route Reflector client.
                    suboptions:
                      set:
                        type: bool
                        description: set route-reflector-client.
                      inheritance-disable:
                        type: bool
                        description: Prevent route-reflector-client from being inherited from the parent.
                  send_community_ebgp: &send_community_ebgp
                    description: Send community attribute to this external neighbor.
                    type: dict
                    suboption:
                      set:
                        type: bool
                        description: set send_community_ebgp.
                      inheritance-disable:
                        type: bool
                        description: Prevent send_community_ebgp from being inherited from the parent.
                  send_community_gshut_ebgp: &send_community_gshut_ebgp
                    description: Allow the g-shut community to be sent to this external neighbor.
                    type: dict
                    suboption:
                      set:
                        type: bool
                        description: set send_community_gshut_ebgp.
                      inheritance-disable:
                        type: bool
                        description: Prevent send_community_gshut_ebgp from being inherited from the parent.
                  send_extended_community_ebgp: &send_extended_community_ebgp
                    description: Send extended community attribute to this external neighbor.
                    type: dict
                    suboptions:
                      set:
                        type: bool
                        description: set send_extended_community_ebgp.
                      inheritance-disable:
                        type: bool
                        description: Prevent send_extended_community_ebgp from being inherited from the parent.
                  send_multicast_attributes:
                    description: Send multicast attributes to this neighbor .
                    type: dict
                    suboptions:
                      set:
                        type: bool
                        description: set send_multicast_attributes.
                      disable:
                        type: bool
                        description: Disable send multicast attributes.
                  soft_reconfiguration: &soft_reconfiguration
                    description: Per neighbor soft reconfiguration.
                    type: dict
                    suboptions:
                      inbound_always:
                        type: bool
                        description: Allow inbound soft reconfiguration for this neighbor. Always use soft reconfig, even if route refresh is supported.
                      inbound_inheritance-disable:
                        type: bool
                        description: Prevent soft_reconfiguration from being inherited from the parent.
                  weight: &wt
                    type: int
                    description: Set default weight for routes from this neighbor.
                  validation: &validation
                    type: dict
                    description: Flowspec Validation for this neighbor.
                    suboptions:
                      set:
                       type: bool
                       description: set validation.
                      redirect:
                        type: bool
                        description: Flowspec Redirect nexthop Validation.
                      disable:
                        type: bool
                        description:  disable validation.
        vrfs:
          description: Configure BGP in a VRF.
          type: list
          elements: dict
          suboptions:
            vrf_name:
             description: VRF name.
             type: str
            neighbors:
              neighbors:
                description: Specify a neighbor router.
                type: list
                elements: dict
                suboptions:
                  neighbor:
                    description:
                      - Neighbor router address.
                    type: str
                    required: true
                  remote_as:
                    description:
                    type: int
                  address_family:
                    description: Enable address family and enter its config mode
                    type: list
                    elements: dict
                    suboptions:
                      afi: *afi
                      af_modifier:
                        description: Address Family modifier
                        type: str
                        choices: [ 'flowspec', 'multicast', 'mvpn', 'unicast', 'labeled-unicast' ]
                      aigp:
                        type: dict
                        description: Enable AIGP for this neighbor .
                        suboptions:
                          set:
                            type: bool
                            description: set aigp
                          disable:
                            type: bool
                            description: disable aigp.
                          send:
                            type: dict
                            description: Copy AIGP
                            suboptions:
                              med:
                                type: dict
                                description: Send AIGP value in MED.
                                suboptions:
                                  set:
                                    type: bool
                                    description: set med
                                  disable:
                                    type: bool
                                    description: disable med
                              cost_community:
                                type: dict
                                description: Send AIGP value in cost-community.
                                suboptions:
                                  set:
                                    type: bool
                                    description: set cost-community.
                                  disable:
                                    type: bool
                                    description: disable cost-community.
                      allowas_in: *allowas_in
                      as_overrride: *as_override
                      capability_orf_prefix: *capability
                      default_originate: *default_originate
                      long_lived_graceful_restart: *long_lived_graceful_restart
                      maximum_prefix: *maximum_prefix
                      multipath: *multipath
                      next_hop_self: *next_hop_self
                      next_hop_unchanged: *next_hop_unchanged
                      optimal_route_reflection_group_name: *optimal_route_reflection
                      orf_route_policy: *orf_route_policy
                      remove_private_AS: *remove_private_AS
                      route_policy: *route_policy
                      route_reflector_client: *route_reflector_client
                      send_community_ebgp: *send_community_ebgp
                      send_community_gshut_ebgp: *send_community_gshut_ebgp
                      send_extended_community_ebgp: *send_extended_community_ebgp
                      soft_reconfiguration: *soft_reconfiguration
                      site_of_origin:
                        description: Site-of-Origin extended community associated with the neighbor.
                        type: str
                      weight: *wt
                      validation: *validation

    running_config:
      description:
      - This option is used only with state I(parsed).
      - The value of this option should be the output received from the Iosxr device by
        executing the command B(show running-config router bgp).
      - The state I(parsed) reads the configuration from C(running_config) option and
        transforms it into Ansible structured data as per the resource module's argspec
        and the value is then returned in the I(parsed) key within the result.
      type: str
    state:
      description:
      - The state the configuration should be left in.
      type: str
      choices: [deleted, merged, overridden, replaced, gathered, rendered, parsed]
      default: merged
"""
EXAMPLES = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.argspec.bgp_neighbor_address_family.bgp_neighbor_address_family import (
    Bgp_neighbor_address_familyArgs,
)
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.config.bgp_neighbor_address_family.bgp_neighbor_address_family import (
    Bgp_neighbor_address_family,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Bgp_neighbor_address_familyArgs.argument_spec,
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

    result = Bgp_neighbor_address_family(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
