from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, MultiColumnListBox

from NetworkObjectFrames.network_object_attributes import ovs_dpdk_bond
from NetworkObjectFrames.ovs_bond import OVSBondFrame
from utils import remove_empty_keys, remove_vlan_members


class OVSDpdkBondFrame(OVSBondFrame):

    ovs_extra_list = []
    selected_option = []
    member_list = []

    @staticmethod
    def get_title():
        return "OVSDpdkBond"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        self.data["type"] = "ovs_dpdk_bond"
        self.add_common_attr()
        self.add_ovs_common_attr()
        for i in ovs_dpdk_bond:
            if i == "members":
                self.layout1.add_widget(Button("Add member", self._add_member))
                self.layout1.add_widget(Button("Delete member", self._delete_member))
                self.widget_dict[i] = MultiColumnListBox(1,
                                                         [self._screen.width // 3 + 1, self._screen.width // 3 + 1,
                                                          self._screen.width // 3 - 3],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_member)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "rx_queue":
                self.widget_dict[i] = Text(label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        self.data["type"] = "ovs_dpdk_bond"
        self.get_available_members()
        self.pop_up_members = []
        if self.available_members:
            self.pop_up_members = []
            for i in self.available_members:
                if i["type"] == "ovs_dpdk_port":
                    self.pop_up_members.append((i["name"], i))
            if self.member_list:
                for i in self.pop_up_members:
                    if i[1] in self.member_list:
                        self.pop_up_members.remove(i)
        else:
            self.pop_up_members = [("None", None)]

        self.fill_common_attr()
        self.fill_ovs_common_attr()
        if self._model.current_network_object == {}:
            for i in ovs_dpdk_bond:
                if i == "members":
                    self.widget_dict[i].options = [(["None"], None)]
        else:
            if "members" in self._model.current_network_object:
                self.member_list = self._model.current_network_object["members"]

            for i in ovs_dpdk_bond:
                if i == "members":
                    if "members" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        if self.member_list is not None and len(self.member_list):
                            for j in self.member_list:
                                self.widget_dict[i].options.append(([j["name"], j["type"], j["mtu"]], j))
                                self.widget_dict[i]._required_height = len(self.member_list)
                    else:
                        self.widget_dict[i]._required_height = 1
                        self.widget_dict[i].options = [(["None"], None)]
        self.fix()

    def _on_close(self, choice):
        for i in self.member_list:
            if i["type"] != "ovs_dpdk_port":
                self.member_list.remove(i)
        if choice == 0:
            self.ovs_data = deepcopy(self.data)
            self.ovs_data["addresses"] = deepcopy(self.address_list)
            self.ovs_data["dns_servers"] = deepcopy(self.dns_list)
            self.ovs_data["domain"] = deepcopy(self.domain_list)
            self.ovs_data["routes"] = deepcopy(self.route_list)
            self.ovs_data["rules"] = deepcopy(self.rule_list)
            self.ovs_data["members"] = deepcopy(self.member_list)
            self.ovs_data["ovs_extra"] = deepcopy(self.ovs_extra_list)
            self.ovs_data = remove_empty_keys(self.ovs_data)
            self.linux_data = deepcopy(self.ovs_data)
            remove_vlan_members(self.linux_data)
            self.linux_data = remove_empty_keys(self.linux_data)
            if self._model.edit_mode:
                if len(self._model.ovs_edit_objects):
                    for i in self._model.ovs_objects:
                        if i in self._model.ovs_edit_objects:
                            i["members"].append(self.ovs_data)
                if len(self._model.linux_edit_objects):
                    for i in self._model.linux_objects:
                        if i in self._model.linux_edit_objects:
                            i["members"].append(self.linux_data)
                self._model.ovs_edit_objects = []
                self._model.linux_edit_objects = []
                self._model.edit_mode = False
            if self._model.member_edit:
                self._model.ovs_members.append(self.ovs_data)
                self._model.linux_members.append(self.linux_data)
            else:
                self._model.handle_ovs_object(self.ovs_data)
                self._model.handle_linux_object(self.linux_data)
                self._model.write_config_members()
                self._model.current_network_object = {}
            raise NextScene("NewConfig")

    def get_available_members(self):
        self.available_members = []
        if len(self._model.ovs_objects):
            for net_object in self._model.ovs_objects:
                if net_object["type"] == "ovs_dpdk_port" \
                        and net_object not in self.member_list \
                        and net_object not in self._model.ovs_members:
                    self.available_members.append(net_object)

    # def _member_on_close(self, choice):
    #     if choice == 0:
    #         self.widget_dict["MemberPopUp"].save()
    #         if self.widget_dict["drop_member"].value is None:
    #             return
    #         self._model.ovs_objects.remove(self.widget_dict["drop_member"].value)
    #         vlan_with_device = self.widget_dict["drop_member"].value
    #         vlan_with_device["device"] = self.widget_dict["name"].value
    #         self.member_list.append(vlan_with_device)
    #         self._model.ovs_members.append(vlan_with_device)
    #         if len(self.member_list) == 1:
    #             self.widget_dict["members"].options = []
    #         self.pop_up_members.remove((self.widget_dict["drop_member"].value["name"],
    #                                     self.widget_dict["drop_member"].value))
    #         self.widget_dict["members"].options.append(([self.widget_dict["drop_member"].value["name"],
    #                                                      self.widget_dict["drop_member"].value["type"]],
    #                                                     self.widget_dict["drop_member"].value))
    #         self._model.linux_objects.remove(self.widget_dict["drop_member"].value)
    #         self._model.linux_members.append(self.widget_dict["drop_member"].value)
    #         self.widget_dict["members"]._required_height = len(self.member_list)
    #         self.fix()

    def _delete_member(self):
        if self.selected_member is not None:
            self.available_members.append(self.selected_member)
            self.pop_up_members.append((self.selected_member["name"], self.selected_member))
            member_temp = ([self.selected_member["name"], self.selected_member["type"],
                            self.selected_member["mtu"]], self.selected_member)
            self._model.linux_members.remove(self.selected_member)
            self._model.linux_objects.append(self.selected_member)
            if member_temp in self.widget_dict["members"].options:
                self.widget_dict["members"].options.remove(member_temp)
                self.member_list.remove(self.selected_member)
                self._model.ovs_members.remove(self.selected_member)
                self._model.ovs_objects.append(self.selected_member)
                self.widget_dict["members"]._required_height -= 1
            if not len(self.member_list):
                self.widget_dict["members"]._required_height = 1
                self.widget_dict["members"].options = [(["None"], None)]
            self.selected_member = None
            self.fix()
