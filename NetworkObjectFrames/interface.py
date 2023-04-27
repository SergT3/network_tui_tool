from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, CheckBox, Button, PopUpDialog, ListBox, MultiColumnListBox, DropdownList

from NetworkObjectFrames.network_object_attributes import common_text, common_check, common_list, ovs_common, \
    interface, route_titles
from interruptframe import InterruptFrame
from utils import remove_empty_keys, to_asciimatics_list


class InterfaceFrame(InterruptFrame):
    ovs_data = None
    address_list = []
    dns_list = []
    domain_list = []
    route_list = []
    rule_list = []
    selected_address = None
    selected_dns = None
    selected_domain = None
    selected_route = None
    selected_rule = None

    @staticmethod
    def get_title():
        return "Interface"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "interface"
        self.layout1.add_widget(object_type)
        self.add_common_attr()
        for i in interface:
            if i == "hotplug":
                self.widget_dict[i] = CheckBox("", label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
            else:
                self.widget_dict[i] = Text(label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        self.fill_common_attr()
        if self._model.current_network_object == {}:
            for i in interface:
                if i == "hotplug":
                    self.widget_dict[i].value = False
                else:
                    self.widget_dict[i].value = ""
        else:
            for i in interface:
                if i == "hotplug":
                    if i in self._model.current_network_object:
                        self.widget_dict[i].value = self._model.current_network_object[i]
                    else:
                        self.widget_dict[i].value = False
                else:
                    if i in self._model.current_network_object:
                        self.widget_dict[i].value = self._model.current_network_object[i]
                    else:
                        self.widget_dict[i].value = ""
        self.fix()

    def add_common_attr(self):
        for i in common_text:
            if i == "name" and self.get_title() == "Interface":
                self._model.get_interface_names()
                self.widget_dict[i] = DropdownList(to_asciimatics_list(self._model.nic_names), label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
            else:
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

    def add_ovs_common_attr(self):
        for i in ovs_common:
            if i == "ovs_options":
                self.widget_dict[i] = Text(label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "ovs_extra":
                self.layout1.add_widget(Button("Add extra option", self._add_option))
                self.layout1.add_widget(Button("Delete extra option", self._delete_option))
                self.widget_dict[i] = ListBox(1, [("None", None)], label=i, name=i, on_select=self._show_option)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "ovs_fail_mode":
                self.widget_dict[i] = DropdownList([("standard", "standard"), ("secure", "secure")], label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])

    def fill_common_attr(self):
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

            for i in common_text:
                if i in self._model.current_network_object:
                    self.data[i] = self._model.current_network_object[i]
                    self.widget_dict[i].value = self._model.current_network_object[i]
                else:
                    self.widget_dict[i].value = ""
            for i in common_check:
                if i in self._model.current_network_object:
                    self.data[i] = self._model.current_network_object[i]
                    self.widget_dict[i].value = self._model.current_network_object[i]
                else:
                    self.widget_dict[i].value = False
            for i in common_list:
                self.widget_dict[i].options = []
                if i == "addresses":
                    if "addresses" in self._model.current_network_object:
                        temp = []
                        for j in self.address_list:
                            temp.append((["ip_netmask:", j["ip_netmask"]],
                                         {"ip_netmask": j["ip_netmask"]}))
                        self.widget_dict[i].options = temp
                        # self.widget_dict[i]._required_height = len(self.address_list)
                    else:
                        self.widget_dict[i].options = [(["None"], None)]
                        self.widget_dict[i]._required_height = 1
                elif i == "dns_servers":
                    if "dns_servers" in self._model.current_network_object:
                        for j in self.dns_list:
                            self.widget_dict[i].options.append((j, j))
                    else:
                        self.widget_dict[i].options = [("None", None)]
                        self.widget_dict[i]._required_height = 1
                        # self.widget_dict[i]._required_height = len(self.dns_list)
                elif i == "domain":
                    if "domain" in self._model.current_network_object:
                        for j in self.domain_list:
                            self.widget_dict[i].options.append((j, j))
                    else:
                        self.widget_dict[i]._required_height = 1
                        self.widget_dict[i].options = [("None", None)]
                        # self.widget_dict[i]._required_height = len(self.domain_list)
                elif i == "routes":
                    if "routes" in self._model.current_network_object:
                        for j in self.route_list:
                            temp_route_list = []
                            for k in j:
                                temp_route_list.append(j[k])
                            self.widget_dict[i].options.append((temp_route_list, temp_route_list))
                        # self.widget_dict[i]._required_height = len(self.route_list)
                    else:
                        self.widget_dict[i]._required_height = 1
                        self.widget_dict[i].options = [(["None"], None)]
                elif i == "rules":
                    if "rules" in self._model.current_network_object:
                        for j in self.rule_list:
                            temp_rule_list = []
                            for k in j:
                                temp_rule_list.append(j[k])
                            self.widget_dict[i].options.append((temp_rule_list, temp_rule_list))
                    else:
                        self.widget_dict[i]._required_height = 1
                        self.widget_dict[i].options = [(["None"], None)]
                        # self.widget_dict[i]._required_height = len(self.rule_list)
        self.fix()

    def fill_ovs_common_attr(self):
        if self._model.current_network_object == {}:
            for i in ovs_common:
                if i == "ovs_extra":
                    self.widget_dict[i].options = [("None", None)]
                else:
                    self.widget_dict[i].value = ""
        else:
            if "ovs_extra" in self._model.current_network_object:
                self.ovs_extra_list = self._model.current_network_object["ovs_extra"]
            for i in ovs_common:
                if i in self._model.current_network_object:
                    if i == "ovs_extra":
                        self.widget_dict[i].options = []
                        for j in self.ovs_extra_list:
                            self.widget_dict[i].options.append((j, j))
                    else:
                        self.data[i] = self._model.current_network_object[i]
                        self.widget_dict[i].value = self._model.current_network_object[i]
                else:
                    if i == "ovs_extra":
                        self.widget_dict[i].options = [("None", None)]
                    else:
                        self.widget_dict[i].value = ""
        self.fix()

    def _save_update(self):
        self.save()
        # write_to_file("data_value_old", self.data)
        self.pop_up = PopUpDialog(self._screen, "Save " + self.data["name"] + " ?", ["OK", "Cancel"],
                                  on_close=self._on_close)
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    def _on_close(self, choice):
        if choice == 0:
            self.ovs_data = deepcopy(self.data)
            self.ovs_data["addresses"] = self.address_list
            self.ovs_data["dns_servers"] = self.dns_list
            self.ovs_data["domain"] = self.domain_list
            self.ovs_data["routes"] = self.route_list
            self.ovs_data["rules"] = self.rule_list
            self.ovs_data = remove_empty_keys(self.ovs_data)
            if self._model.edit_mode:
                if len(self._model.ovs_edit_objects):
                    for i in self._model.ovs_objects:
                        if i in self._model.ovs_edit_objects:
                            i["members"].append(self.ovs_data)
                if len(self._model.linux_edit_objects):
                    for i in self._model.linux_objects:
                        if i in self._model.linux_edit_objects:
                            i["members"].append(self.ovs_data)
                self._model.ovs_edit_objects = []
                self._model.linux_edit_objects = []
            if self._model.member_edit:
                self._model.ovs_members.append(self.ovs_data)
                self._model.linux_members.append(self.ovs_data)
                self._model.member_edit = False
            else:
                self._model.handle_ovs_object(self.ovs_data)
                self._model.handle_linux_object(self.ovs_data)
                self._model.current_network_object = {}
            raise NextScene("NewConfig")

    def _cancel(self):
        if not self._model.edit_mode:
            self._model.current_network_object = {}
        self._model.edit_mode = False
        raise NextScene("NewConfig")

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
            if len(self.address_list):
                if self.widget_dict["addresses"].options == [(["None"], None)]:
                    self.widget_dict["addresses"].options = []
                self.widget_dict["addresses"].options.append(
                    (["ip_netmask:", self.widget_dict["AddressPopUp"].data["text"]],
                     {"ip_netmask": self.widget_dict["AddressPopUp"].data[
                         "text"]}))
                self.widget_dict["addresses"]._required_height = len(self.address_list)
            self.fix()

    def _show_address(self):
        self.selected_address = self.widget_dict["addresses"].value

    def _delete_address(self):
        if self.selected_address is not None:
            while (["ip_netmask:", self.selected_address["ip_netmask"]], self.selected_address) in self.widget_dict["addresses"].options:
                self.widget_dict["addresses"].options.remove(
                    (["ip_netmask:", self.selected_address["ip_netmask"]], self.selected_address))
                self.address_list.remove(self.selected_address)
                self.widget_dict["addresses"]._required_height -= 1
            if not len(self.address_list):
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
            if len(self.dns_list):
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
            if not len(self.dns_list):
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
            if len(self.domain_list):
                if self.widget_dict["domain"].options == [("None", None)]:
                    self.widget_dict["domain"].options = []
                self.widget_dict["domain"].options.append((self.widget_dict["DomainPopUp"].data["text"],
                                                           self.widget_dict["DomainPopUp"].data["text"]))
                self.widget_dict["domain"]._required_height = len(self.domain_list)
            self.fix()

    def _show_domain(self):
        self.selected_option = self.widget_dict["domain"].value

    def _delete_domain(self):
        if self.selected_domain is not None:
            while (self.selected_domain, self.selected_domain) in self.widget_dict["domain"].options:
                self.widget_dict["domain"].options.remove((self.selected_domain, self.selected_domain))
                self.domain_list.remove(self.selected_domain)
                self.widget_dict["domain"]._required_height -= 1
            if not len(self.domain_list):
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
            self.widget_dict["RoutePopUp"]._layouts[0].add_widget(
                Text(i + ":", validator=self._model.name_validator, name=i))
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
            if self.widget_dict["routes"].options == [(["None"], None)]:
                self.widget_dict["routes"].options = []
            self.widget_dict["routes"].options.append((tuple(temp_route_list), tuple(temp_route_list)))
            self.route_list.append(temp_route_dict)
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
            if not len(self.route_list):
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
            if not len(self.rule_list):
                self.widget_dict["rules"]._required_height = 1
                self.widget_dict["rules"].options = [(["None"], None)]
            self.selected_rule = None
            self.fix()
