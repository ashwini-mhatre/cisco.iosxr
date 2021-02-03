#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The iosxr_bgp_global config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.facts.facts import (
    Facts,
)
from ansible_collections.cisco.iosxr.plugins.module_utils.network.iosxr.rm_templates.bgp_global import (
    Bgp_globalTemplate,
)


class Bgp_global(ResourceModule):
    """
    The iosxr_bgp_global config class
    """

    def __init__(self, module):
        super(Bgp_global, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="bgp_global",
            tmplt=Bgp_globalTemplate(),
        )
        self.parsers = [
            'router',
            'bfd_multiplier',
            'bfd_minimum_interval',
            'bgp_auto_policy_soft_reset',
            'bgp_as_path_loopcheck',
            'bgp_cluster_id',
            'bgp_default_local_preference',
            'bgp_enforce_first_as_disable',
            'bgp_fast_external_fallover_disable',
            'bgp_install_diversion',
            'bgp_max_neighbors',
            'bgp_redistribute_internal',
            'bgp_router_id',
            'bgp_scan_time',
            'bgp_unsafe_ebgp_policy',
            'bgp_update_delay',
            'bgp_bestpath_aigp',
            'bgp_bestpath_as_path_ignore',
            'bgp_bestpath_as_path_multipath_relax',
            'bgp_bestpath_med_always',
            'bgp_bestpath_med_confed',
            'bgp_bestpath_med_missing_as_worst',
            'bgp_bestpath_compare_routerid',
            'bgp_bestpath_cost_community_ignore',
            'bgp_bestpath_origin_as_use',
            'bgp_bestpath_origin_as_allow',
            'bgp_confederation_identifier',
            'bgp_graceful_restart_set',
            'bgp_graceful_restart_graceful_reset',
            'bgp_graceful_restart_restart_time',
            'bgp_graceful_restart_purge_time',
            'bgp_graceful_restart_stalepath_time',
            'bgp_log_message',
            'bgp_log_neighbor_changes_detail',
            'bgp_log_neighbor_changes_disable',
            'bgp_multipath_as_path_ignore_onwards',
            'bgp_origin_as_validation_disable',
            'bgp_origin_as_validation_signal_ibgp',
            'bgp_origin_as_validation_time_off',
            'bgp_origin_as_validation_time',
            'bgp_default_information_originate',
            'bgp_default_metric',
            'bgp_graceful_maintenance',
            'ibgp_policy_out_enforce_modifications',
            'mpls_activate_interface',
            'mvpn',
            'nsr_set',
            'nsr_disable',
            'socket_receive_buffer_size',
            'socket_send_buffer_size',
            'update_in_error_handling_basic_ebgp_disable',
            'update_in_error_handling_basic_ibgp_disable',
            'update_in_error_handling_extended_ebgp',
            'update_in_error_handling_extended_ibgp',
            'update_out_logging',
            'update_limit',
            'rpki_route_value',
            'rd_auto',
            'timers_keepalive',
        ]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
                    want, have and desired state.
                """

        for entry in self.want, self.have:
            self._bgp_list_to_dict(entry)

        # if state is deleted, clean up global params
        if self.state == "deleted":
            if not self.want or (self.have.get("as_number") == self.want.get("as_number")):
                self._compare(want={"as_number": self.want.get("as_number")}, have=self.have)
        elif self.state == "purged":
            if not self.want or (
                    self.have.get("as_number") == self.want.get("as_number")
            ):
                self.addcmd(self.have or {}, "router", True)

        else:
            wantd = self.want
            # if state is merged, merge want onto have and then compare
            if self.state == "merged":
                wantd = dict_merge(self.have, self.want)

            self._compare(want=wantd, have=self.have)

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Bgp_global network resource.
        """
        self._compare_rpki_server(want=want, have=self.have)
        self._compare_neighbors(want=want, have=self.have)
        self._vrfs_compare(want=want, have=have)
        self.compare(parsers=self.parsers, want=want, have=have)
        if self.commands and "router bgp" not in self.commands[0]:
            self.commands.insert(
                0, self._tmplt.render({"as_number": want['as_number']}, "router", False)
            )

    def _compare_rpki_server(self, want, have):
        """Leverages the base class `compare()` method and
                   populates the list of commands to be run by comparing
                   the `want` and `have` data with the `parsers` defined
                   for the Bgp_global rpki servers resource.
                """
        rpki_server_parsers = [
            'rpki_server_purge_time',
            'rpki_server_refresh_time',
            'rpki_server_refresh_time_off',
            'rpki_server_response_time',
            'rpki_server_response_time_off',
            'rpki_server_shutdown',
            'rpki_server_transport_ssh',
            'rpki_server_transport_tcp',
        ]
        want = want.get("rpki", {}).get("servers", {})
        have = have.get("rpki", {}).get("servers", {})
        for name, entry in iteritems(want):
            new_have = have.pop(name, {})
            begin = len(self.commands)
            self.compare(parsers=rpki_server_parsers, want=entry, have=new_have)
            rpki_server_name = entry.get("name")
            if len(self.commands) != begin:
                self.commands.insert(
                    begin, self._tmplt.render({"name": rpki_server_name }, "rpki_server_name", False)
                )
        for name, entry in iteritems(have):
            self.addcmd(entry, "rpki_server_name", True)

    def _compare_neighbors(self, want, have, vrf=None):
        """Leverages the base class `compare()` method and
                   populates the list of commands to be run by comparing
                   the `want` and `have` data with the `parsers` defined
                   for the Bgp_global neighbor resource.
                """
        neighbor_parsers = [
            'advertisement_interval',
            'bfd_fast_detect_disable',
            'bfd_fast_detect_strict_mode',
            'bfd_nbr_minimum_interval',
            'bfd_nbr_multiplier',
            'bmp_activate',
            'dmz_link_bandwidth',
            'dmz_link_bandwidth_inheritance_disable',
            'neighbor_description',
            'neighbor_cluster_id',
            'dscp',
            'ebgp_multihop_value',
            'ebgp_multihop_mpls',
            'ebgp_recv_extcommunity_dmz',
            'ebgp_recv_extcommunity_dmz_set',
            'ebgp_send_extcommunity_dmz',
            'ebgp_send_extcommunity_dmz_set',
            'ebgp_send_extcommunity_dmz_cumulatie',
            'egress_engineering',
            'egress_engineering_set',
            'ignore_connected_check',
            'ignore_connected_check_set',
            'neighbor_enforce_first_as_disable',
            'neighbor_graceful_restart_restart_time',
            'neighbor_graceful_restart_stalepath_time',
            'keychain',
            'keychain_name',
            'local_as_inheritance_disable',
            'local_as',
            'local',
            'local_address',
            'origin_as',
            'remote_as',
            'receive_buffer_size',
            'send_buffer_size',
            'session_open_mode',
            'neighbor_shutdown',
            'neighbor_shutdown_inheritance_disable',
            'neighbor_tcp_mss',
            'neighbor_tcp_mss_inheritance_disable',
            'neighbor_timers_keepalive',
            'update_source',
            'neighbor_ttl_security_inheritance_disable',
            'neighbor_ttl_security',
            'neighbor_graceful_maintenance_set',
            'neighbor_graceful_maintenance_activate',
            'neighbor_graceful_maintenance_activate_inheritance_disable',
            'neighbor_graceful_maintenance_as_prepends',
            'neighbor_graceful_maintenance_local_preference_disable',
            'neighbor_graceful_maintenance_local_preference',
            'neighbor_graceful_maintenance_as_prepends_value',
            'neighbor_capability_additional_paths_send',
            'neighbor_capability_additional_paths_send_disable',
            'neighbor_capability_additional_paths_rcv_disable',
            'neighbor_capability_additional_paths_rcv',
            'neighbor_capability_suppress_4_byte_AS',
            'neighbor_capability_suppress_all',
            'neighbor_capability_suppress_all_inheritance_disable',
            'neighbor_log_message_in_value',
            'neighbor_log_message_in_disable',
            'neighbor_log_message_in_inheritance_disable',
            'neighbor_log_message_out_value',
            'neighbor_log_message_out_disable',
            'neighbor_log_message_out_inheritance_disable',
            'neighbor_update_in_filtering_attribute_filter_group',
            'neighbor_update_in_filtering_logging_disable',
            'neighbor_update_in_filtering_message_buffers',
           ]

        want_nbr = want.get("neighbors", {})
        have_nbr = have.get("neighbors", {})
        for name, entry in iteritems(want_nbr):
            have = have_nbr.pop(name, {})
            begin = len(self.commands)
            self.compare(parsers=neighbor_parsers, want=entry, have=have)
            neighbor_address = entry.get("neighbor", "")
            if len(self.commands) != begin:
                self.commands.insert(
                    begin, self._tmplt.render({"neighbor": neighbor_address}, "neighbor", False)
                )
        for name, entry in iteritems(have_nbr):
            self.addcmd(entry, "neighbor", True)

    def _vrfs_compare(self, want, have):
        """Custom handling of VRFs option
        :params want: the want BGP dictionary
        :params have: the have BGP dictionary
        """
        wvrfs = want.get("vrfs", {})
        hvrfs = have.get("vrfs", {})
        for name, entry in iteritems(wvrfs):
            begin = len(self.commands)
            vrf_have = hvrfs.pop(name, {})
            self._compare_rpki_server(want=entry, have=vrf_have)
            self._compare_neighbors(want=entry, have=vrf_have)
            self.compare(parsers=self.parsers, want=entry, have=vrf_have)
            if len(self.commands) != begin:
                self.commands.insert(
                    begin, self._tmplt.render({"vrf": entry.get('vrf')}, "vrf", False)
                )
        # cleanup remaining VRFs
        # but do not negate it entirely
        # instead remove only those attributes
        # that this module manages
        for name, entry in iteritems(hvrfs):
            self.addcmd(entry, "vrf", True)

    def _bgp_list_to_dict(self, entry):
        """Convert list of items to dict of items
           for efficient diff calculation.
        :params entry: data dictionary
        """

        def _build_key(x):
            """Build primary key for path_attribute
               option.
            :params x: path_attribute dictionary
            :returns: primary key as tuple
            """
            key_1 = "start_{0}".format(x.get("range", {}).get("start", ""))
            key_2 = "end_{0}".format(x.get("range", {}).get("end", ""))
            key_3 = "type_{0}".format(x.get("type", ""))
            key_4 = x["action"]

            return (key_1, key_2, key_3, key_4)
        if "servers" in entry.get("rpki", {}):
            entry["rpki"]["servers"] = {
                x["name"]: x for x in entry.get("rpki", {}).get("servers", [])
            }
        if "neighbors" in entry:
            entry["neighbors"] = {
                x["neighbor"]: x for x in entry.get("neighbors", [])
            }

        if "vrfs" in entry:
            entry["vrfs"] = {x["vrf"]: x for x in entry.get("vrfs", [])}
            for _k, vrf in iteritems(entry["vrfs"]):
                self._bgp_list_to_dict(vrf)





