common_list = ["addresses", "dns_servers", "domain", "routes", "rules"]
common_text = ["dhclient_args", "mtu", "name"]
common_check = ["defroute", "nm_controlled", "on_boot", "primary", "use_dhcp", "use_dhcpv6"]

ovs_common = ["ovs_options", "ovs_extra", "ovs_fail_mode"]

interface = ["ethtool_opts", "hotplug", "linkdelay"]  # + common_attributes
vlan = ["mtu", "addresses", "routes", "device", "vlan_id"]

linux_bridge = ["members*"]  # + common_attributes
# interfaces

linux_bond = ["members*", "bonding_options"]  # + common_attributes
# interfaces

ovs_bridge = ["members*"]  # + common_attributes + common_ovs_attributes
# interface
#
# linux_bond
#
# ovs_bond
#
# vlan
#
# other OpenvSwitch internal interfaces

ovs_bond = ["members*"]  # + common_attributes + common_ovs_attributes
# interfaces

ovs_user_bridge = ["members*"]  # + common_attributes + common_ovs_attributes
# usually 1 ovs_dpdk_bond

ovs_dpdk_bond = ["members*", "rx_queue"]  # + common_attributes + common_ovs_attributes
# list of ovs_dpdk_port

ovs_dpdk_port = ["members*", "rx_queue", "driver"]  # + common_attributes + common_ovs_attributes
# 1 interface
