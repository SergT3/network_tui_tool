from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, CheckBox, ListBox, MultiColumnListBox, PopUpDialog, DropdownList

from NetworkObjectFrames.network_object_attributes import linux_bridge, common_check, common_text, common_list, \
    route_titles
from interruptframe import InterruptFrame


class LinuxBridgeFrame(InterruptFrame):

    opt_data = None
    address_list = []
    dns_list = []
    domain_list = []
    route_list = []
    rule_list = []
    member_list = []
    selected_address = None
    selected_dns = None
    selected_domain = None
    selected_route = None
    selected_rule = None
    selected_member = None
    available_members = []
    pop_up_members = []

    @staticmethod
    def get_title():
        return "LinuxBridge"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "linux_bridge"
        self.layout1.add_widget(object_type)
        for i in common_text:
            self.widget_dict[i] = Text(label=i, name=i)
            self.layout1.add_widget(self.widget_dict[i])
        for i in common_check:
            self.widget_dict[i] = CheckBox("", label=i, name=i)
            self.layout1.add_widget(self.widget_dict[i])
        for i in common_list:
            if i == "addresses":
                self.layout1.add_widget(Button("Add address", self._add_address))
                self.layout1.add_widget(Button("Delete address", self._delete_address))
                self.widget_dict[i] = MultiColumnListBox(1, [self._screen.width // 3 + 1, self._screen.width // 3 - 1],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_address)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "dns_servers":
                self.layout1.add_widget(Button("Add DNS server", self._add_dns))
                self.layout1.add_widget(Button("Delete DNS server", self._delete_dns))
                self.widget_dict[i] = ListBox(1, [("None", None)], label=i, name=i, on_select=self._show_dns)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "domain":
                self.layout1.add_widget(Button("Add domain", self._add_domain))
                self.layout1.add_widget(Button("Delete domain", self._delete_domain))
                self.widget_dict[i] = ListBox(1, [("None", None)], label=i, name=i, on_select=self._show_domain)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "routes":
                self.layout1.add_widget(Button("Add route", self._add_route))
                self.layout1.add_widget(Button("Delete route", self._delete_route))
                self.widget_dict[i] = MultiColumnListBox(1,
                                                         [self._screen.width // 5 + 1, self._screen.width // 5 + 1,
                                                          self._screen.width // 5 + 1, self._screen.width // 5 + 1,
                                                          self._screen.width // 5 - 4],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_route)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "rules":
                self.layout1.add_widget(Button("Add rule", self._add_rule))
                self.layout1.add_widget(Button("Delete rule", self._delete_rule))
                self.widget_dict[i] = MultiColumnListBox(1, [self._screen.width // 2 + 1, self._screen.width // 2 - 1],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_rule)
                self.layout1.add_widget(self.widget_dict[i])
        for i in linux_bridge:
            if i == "members":
                self.layout1.add_widget(Button("Add member", self._add_member))
                self.layout1.add_widget(Button("Delete member", self._delete_member))
                self.widget_dict[i] = MultiColumnListBox(1, [self._screen.width // 3 + 1, self._screen.width // 3 + 1,
                                                             self._screen.width // 3 - 3],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_member)
                self.layout1.add_widget(self.widget_dict[i])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        self.get_available_members()
        if len(self.available_members) != 0:
            for i in self.available_members:
                self.pop_up_members.append((i["name"], {"type": "interface", "name": i["name"], "mtu": i["mtu"]}))
            if len(self.member_list) != 0:
                for i in self.pop_up_members:
                    for j in self.member_list:
                        if i[1]["type"] == j["type"] and i[1]["name"] == j["name"]:
                            self.pop_up_members.remove(i)
        else:
            self.pop_up_members = [("None", None)]

        if self._model.current_network_object == {}:
            for i in common_text:
                self.widget_dict[i].value = ""
            for i in common_check:
                self.widget_dict[i].value = False
            for i in common_list:
                if i == "dns_servers" or i == "domain":
                    self.widget_dict[i].options = [("None", None)]
                else:
                    self.widget_dict[i].options = [(["None"], None)]
            for i in linux_bridge:
                if i == "members":
                    self.widget_dict[i].options = [(["None"], None)]
        else:
            if "addresses" in self._model.current_network_object:
                self.address_list = self._model.current_network_object["addresses"]
            if "dns_servers" in self._model.current_network_object:
                self.dns_list = self._model.current_network_object["dns_servers"]
            if "domain" in self._model.current_network_object:
                self.domain_list = self._model.current_network_object["domain"]
            if "routes" in self._model.current_network_object:
                self.route_list = self._model.current_network_object["routes"]
            if "rules" in self._model.current_network_object:
                self.rule_list = self._model.current_network_object["rules"]
            if "members" in self._model.current_network_object:
                self.member_list = self._model.current_network_object["members"]

            for i in common_text + common_check:
                self.data[i] = self._model.current_network_object[i]
                self.widget_dict[i].value = self._model.current_network_object[i]
            for i in common_list + linux_bridge:
                self.widget_dict[i].options = []
                if i == "addresses":
                    self.widget_dict[i].options = []
                    if "addresses" in self._model.current_network_object:
                        temp = []
                        for j in self.address_list:
                            temp.append((["ip_netmask:", j["ip_netmask"]],
                                         {"ip_netmask": j["ip_netmask"]}))
                        self.widget_dict[i].options = temp
                        # self.widget_dict[i]._required_height = len(self.address_list)
                elif i == "dns_servers":
                    if "dns_servers" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        for j in self.dns_list:
                            self.widget_dict[i].options.append((j, j))
                        # self.widget_dict[i]._required_height = len(self.dns_list)
                elif i == "domain":
                    if "domain" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        for j in self.domain_list:
                            self.widget_dict[i].options.append((j, j))
                        # self.widget_dict[i]._required_height = len(self.domain_list)
                elif i == "routes":
                    if "routes" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        for j in self.route_list:
                            temp_route_list = []
                            for k in j:
                                temp_route_list.append(j[k])
                            self.widget_dict[i].options.append((temp_route_list, temp_route_list))
                        # self.widget_dict[i]._required_height = len(self.route_list)
                elif i == "rules":
                    if "rules" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        for j in self.rule_list:
                            temp_rule_list = []
                            for k in j:
                                temp_rule_list.append(j[k])
                            self.widget_dict[i].options.append((temp_rule_list, temp_rule_list))
                        # self.widget_dict[i]._required_height = len(self.rule_list)
                elif i == "members":
                    if "members" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        for j in self.member_list:
                            self.widget_dict[i].options.append(([j["name"], j["type"], j["mtu"]], j))
                        # self.widget_dict[i]._required_height = len(self.rule_list)
        self.fix()

    def _cancel(self):
        self._model.current_network_object = {}
        raise NextScene("NewConfig")

    def _save_update(self):
        self.save()
        # write_to_file("data_value_old", self.data)
        self.pop_up = PopUpDialog(self._screen, "Save " + self.data["name"] + " ?", ["OK", "Cancel"],
                                  on_close=self._on_close)
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    def _on_close(self, choice):
        if choice == 0:
            self.opt_data = deepcopy(self.data)
            self.opt_data["addresses"] = self.address_list
            self.opt_data["dns_servers"] = self.dns_list
            self.opt_data["domain"] = self.domain_list
            self.opt_data["routes"] = self.route_list
            self.opt_data["rules"] = self.rule_list
            self.opt_data["members"] = self.member_list
            self._model.handle_object(self.opt_data)
            self._model.current_network_object = {}
            raise NextScene("NewConfig")
        else:
            pass

    def _add_address(self):
        self.widget_dict["AddressPopUp"] = PopUpDialog(self._screen, "Enter new address",
                                                       ["OK", "Cancel"], on_close=self._address_on_close)
        self.widget_dict["AddressPopUp"]._layouts[0].add_widget(Text("Here:", validator=self._model.name_validator,
                                                                     name="text"))
        self.widget_dict["AddressPopUp"].fix()
        self.scene.add_effect(self.widget_dict["AddressPopUp"])

    def _address_on_close(self, choice):
        if choice == 0:
            self.widget_dict["AddressPopUp"].save()
            self.address_list.append({"ip_netmask": self.widget_dict["AddressPopUp"].data["text"]})
            if len(self.address_list) != 0:
                if self.widget_dict["addresses"].options == [(["None"], None)]:
                    self.widget_dict["addresses"].options = []
                self.widget_dict["addresses"].options.append((["ip_netmask:", self.widget_dict["AddressPopUp"].data["text"]],
                                                              {"ip_netmask": self.widget_dict["AddressPopUp"].data["text"]}))
                self.widget_dict["addresses"]._required_height = len(self.address_list)
            self.fix()

    def _show_address(self):
        self.selected_address = self.widget_dict["addresses"].value
    def _delete_address(self):
        if self.selected_address is not None:
            while (["ip_netmask:", self.selected_address["ip_netmask"]], self.selected_address) in self.widget_dict["addresses"].options:
                self.widget_dict["addresses"].options.remove((["ip_netmask:", self.selected_address["ip_netmask"]], self.selected_address))
                self.address_list.remove(self.selected_address)
                self.widget_dict["addresses"]._required_height -= 1
            if len(self.address_list) == 0:
                self.widget_dict["addresses"]._required_height = 1
                self.widget_dict["addresses"].options = [(["None"], None)]
            self.selected_address = None
            self.fix()
    def _add_dns(self):
        self.widget_dict["DNSPopUp"] = PopUpDialog(self._screen, "Enter DNS servers",
                                                   ["OK", "Cancel"], on_close=self._dns_on_close)
        self.widget_dict["DNSPopUp"]._layouts[0].add_widget(Text("DNS1:", validator=self._model.name_validator,
                                                                 name="text1"))
        self.widget_dict["DNSPopUp"]._layouts[0].add_widget(Text("DNS2:", validator=self._model.name_validator,
                                                                 name="text2"))
        self.widget_dict["DNSPopUp"].fix()
        self.scene.add_effect(self.widget_dict["DNSPopUp"])

    def _dns_on_close(self, choice):
        if choice == 0:
            self.widget_dict["DNSPopUp"].save()
            self.dns_list = [self.widget_dict["DNSPopUp"].data["text1"],
                             self.widget_dict["DNSPopUp"].data["text2"]]
            for i in self.dns_list:
                if i == "":
                    self.dns_list.remove(i)
            if len(self.dns_list) != 0:
                self.widget_dict["dns_servers"].options = []
                for i in self.dns_list:
                    self.widget_dict["dns_servers"].options.append((i, i))
                self.widget_dict["dns_servers"]._required_height = len(self.dns_list)
            self.fix()

    def _show_dns(self):
        self.selected_dns = self.widget_dict["dns_servers"].value

    def _delete_dns(self):
        if self.selected_dns is not None:
            while (self.selected_dns, self.selected_dns) in self.widget_dict["dns_servers"].options:
                self.widget_dict["dns_servers"].options.remove((self.selected_dns, self.selected_dns))
                self.dns_list.remove(self.selected_dns)
                self.widget_dict["dns_servers"]._required_height -= 1
            if len(self.dns_list) == 0:
                self.widget_dict["dns_servers"]._required_height = 1
                self.widget_dict["dns_servers"].options = [("None", None)]
            self.selected_dns = None
            self.fix()

    def _add_domain(self):
        self.widget_dict["DomainPopUp"] = PopUpDialog(self._screen, "Enter new domain",
                                                      ["OK", "Cancel"], on_close=self._domain_on_close)
        self.widget_dict["DomainPopUp"]._layouts[0].add_widget(Text("Here:", validator=self._model.name_validator,
                                                                    name="text"))
        self.widget_dict["DomainPopUp"].fix()
        self.scene.add_effect(self.widget_dict["DomainPopUp"])

    def _domain_on_close(self, choice):
        if choice == 0:
            self.widget_dict["DomainPopUp"].save()
            self.domain_list.append(self.widget_dict["DomainPopUp"].data["text"])
            if len(self.domain_list) != 0:
                if self.widget_dict["domain"].options == [("None", None)]:
                    self.widget_dict["domain"].options = []
                self.widget_dict["domain"].options.append((self.widget_dict["DomainPopUp"].data["text"],
                                                           self.widget_dict["DomainPopUp"].data["text"]))
                self.widget_dict["domain"]._required_height = len(self.domain_list)
            self.fix()

    def _show_domain(self):
        self.selected_domain = self.widget_dict["domain"].value

    def _delete_domain(self):
        if self.selected_domain is not None:
            while (self.selected_domain, self.selected_domain) in self.widget_dict["domain"].options:
                self.widget_dict["domain"].options.remove((self.selected_domain, self.selected_domain))
                self.domain_list.remove(self.selected_domain)
                self.widget_dict["domain"]._required_height -= 1
            if len(self.domain_list) == 0:
                self.widget_dict["domain"]._required_height = 1
                self.widget_dict["domain"].options = [("None", None)]
            self.selected_domain = None
            self.fix()

    def _add_route(self):
        self.widget_dict["RoutePopUp"] = PopUpDialog(self._screen, "Enter new route",
                                                     ["OK", "Cancel"], on_close=self._route_on_close)
        for i in route_titles:
            # if i == default:
            # self.widget_dict["RoutePopUp"]._layouts[0].add_widget(CheckBox("", label=i, name=i))
            # error: object of type bool has no len
            self.widget_dict["RoutePopUp"]._layouts[0].add_widget(Text(i + ":", validator=self._model.name_validator, name=i))
        self.widget_dict["RoutePopUp"].fix()
        self.scene.add_effect(self.widget_dict["RoutePopUp"])

    def _route_on_close(self, choice):
        if choice == 0:
            self.widget_dict["RoutePopUp"].save()
            temp_route_dict = {}
            temp_route_list = []
            for i in route_titles:
                if self.widget_dict["RoutePopUp"].data[i] != "":
                    temp_route_dict[i] = self.widget_dict["RoutePopUp"].data[i]
            for i in temp_route_dict:
                temp_route_list.append(temp_route_dict[i])
            self.route_list.append(temp_route_dict)
            if len(self.route_list) == 1:
                self.widget_dict["routes"].options = []
            self.widget_dict["routes"].options.append((tuple(temp_route_list), tuple(temp_route_list)))
            self.widget_dict["routes"]._required_height = len(self.route_list)
            self.fix()

    def _show_route(self):
        self.selected_route = self.widget_dict["routes"].value

    def _delete_route(self):
        if self.selected_route is not None:
            temp_route_dict = {}
            j = 0
            for i in route_titles:
                temp_route_dict[i] = self.selected_route[j]
                j += 1
            while (self.selected_route, self.selected_route) in self.widget_dict["routes"].options:
                self.widget_dict["routes"].options.remove((self.selected_route, self.selected_route))
                self.route_list.remove(temp_route_dict)
                self.widget_dict["routes"]._required_height -= 1
            if len(self.route_list) == 0:
                self.widget_dict["routes"]._required_height = 1
                self.widget_dict["routes"].options = [(["None"], None)]
            self.selected_route = None
            self.fix()

    def _add_rule(self):
        self.widget_dict["RulePopUp"] = PopUpDialog(self._screen, "Enter new address",
                                                    ["OK", "Cancel"], on_close=self._rule_on_close)
        self.widget_dict["RulePopUp"]._layouts[0].add_widget(Text("Here:", validator=self._model.name_validator,
                                                                  name="rule"))
        self.widget_dict["RulePopUp"]._layouts[0].add_widget(Text("And here:", validator=self._model.name_validator,
                                                                  name="comment"))
        self.widget_dict["RulePopUp"].fix()
        self.scene.add_effect(self.widget_dict["RulePopUp"])
    def _rule_on_close(self, choice):
        if choice == 0:
            self.widget_dict["RulePopUp"].save()
            if self.widget_dict["RulePopUp"].data["rule"] != "":
                rule_dict = {}
                temp_rule_list = []
                if self.widget_dict["RulePopUp"].data["comment"] != "":
                    rule_dict = {"rule": self.widget_dict["RulePopUp"].data["rule"],
                                 "comment": self.widget_dict["RulePopUp"].data["comment"]}
                else:
                    rule_dict = {"rule": self.widget_dict["RulePopUp"].data["rule"]}
                for i in rule_dict:
                    temp_rule_list.append(rule_dict[i])
                self.rule_list.append(rule_dict)
                if len(self.rule_list) == 1:
                    self.widget_dict["rules"].options = []
                self.widget_dict["rules"].options.append((tuple(temp_rule_list), tuple(temp_rule_list)))
                self.widget_dict["rules"]._required_height = len(self.rule_list)
                self.fix()

    def _show_rule(self):
        self.selected_rule = self.widget_dict["rules"].value

    def _delete_rule(self):
        if self.selected_rule is not None:
            temp_rule_dict = {}
            j = 0
            for i in ["rule", "comment"]:
                temp_rule_dict[i] = self.selected_rule[j]
                j += 1
            while (self.selected_rule, self.selected_rule) in self.widget_dict["rules"].options:
                self.widget_dict["rules"].options.remove((self.selected_rule, self.selected_rule))
                self.rule_list.remove(temp_rule_dict)
                self.widget_dict["rules"]._required_height -= 1
            if len(self.rule_list) == 0:
                self.widget_dict["rules"]._required_height = 1
                self.widget_dict["rules"].options = [(["None"], None)]
            self.selected_rule = None
            self.fix()

    def get_available_members(self):
        if len(self._model.current_config_object_list) != 0:
            for net_object in self._model.current_config_object_list:
                if net_object["type"] == "interface":
                    if net_object["name"] not in self.member_list:
                        self.available_members.append({"type": "interface", "name": net_object["name"], "mtu": net_object["mtu"]})

                # if net_object["type"] == "vlan":
                #     self.available_devices.append({"type": "vlan", "device": net_object["device"],
                #                                    "mtu": net_object["mtu"], "vlan_id": net_object["vlan_id"]})

    def _add_member(self):
        self.widget_dict["MemberPopUp"] = PopUpDialog(self._screen, "Select new member:",
                                                    ["OK", "Cancel"], on_close=self._member_on_close)
        self.widget_dict["drop_member"] = DropdownList(self.pop_up_members, label="Available members")
        self.widget_dict["MemberPopUp"]._layouts[0].add_widget(self.widget_dict["drop_member"])
        self.widget_dict["MemberPopUp"].fix()
        self.scene.add_effect(self.widget_dict["MemberPopUp"])        # for net_object in self._model.current_config_object_list:
        #     if net_object["type"] == "interface":
        #         self.available_devices.append({"type": "interface", "name": config[i]["name"], "mtu": config[i]["mtu"]})
        #     if net_object["type"] == "vlan":
        #         self.available_devices.append({"type": "vlan", "device": config[i]["device"],
        #                                        "mtu": config[i]["mtu"], "vlan_id": config[i]["vlan_id"]})

    def _member_on_close(self, choice):
        if choice == 0:
            self.widget_dict["MemberPopUp"].save()
            if self.widget_dict["drop_member"].value is None:
                return
            self.pop_up_members.remove((self.widget_dict["drop_member"].value["name"], self.widget_dict["drop_member"].value))
            self.member_list.append(self.widget_dict["drop_member"].value)
            if len(self.member_list) == 1:
                self.widget_dict["members"].options = []
            self.widget_dict["members"].options.append(([self.widget_dict["drop_member"].value["name"],
                                                         self.widget_dict["drop_member"].value["type"],
                                                         self.widget_dict["drop_member"].value["mtu"]],
                                                        self.widget_dict["drop_member"].value))
            self.widget_dict["members"]._required_height = len(self.member_list)
            self.fix()


    def _show_member(self):
        self.selected_member = self.widget_dict["members"].value

    def _delete_member(self):
        if self.selected_member is not None:
            self.available_members.append(self.selected_member)
            self.pop_up_members.append(
                (self.selected_member["name"], self.selected_member))
            member_temp = ([self.selected_member["name"], self.selected_member["type"], self.selected_member["mtu"]],
                           self.selected_member)
            while member_temp in self.widget_dict["members"].options:
                self.widget_dict["members"].options.remove(member_temp)
                self.member_list.remove(self.selected_member)
                self.widget_dict["members"]._required_height -= 1
            if len(self.member_list) == 0:
                self.widget_dict["members"]._required_height = 1
                self.widget_dict["members"].options = [(["None"], None)]
            self.selected_member = None
            self.fix()




# for net_object in self._model.current_config_object_list:
#     if net_object["type"] == "interface":
#         self.available_members.append({"type": "interface", "name": net_object["name"], "mtu": net_object["mtu"]})
#     if net_object["type"] == "vlan":
#         self.available_members.append({"type": "vlan", "device": net_object["device"],
#                                        "mtu": net_object["mtu"], "vlan_id": net_object["vlan_id"]})