from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, MultiColumnListBox, PopUpDialog

import utils
from NetworkObjectFrames.linux_bond import LinuxBondFrame
from NetworkObjectFrames.network_object_attributes import ovs_bond, ovs_common
from utils import remove_empty_keys, remove_vlan_members


class OVSBondFrame(LinuxBondFrame):

    ovs_extra_list = []
    selected_option = []
    member_list = []

    @staticmethod
    def get_title():
        return "OVSBond"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        self.data["type"] = "ovs_bond"
        self.add_common_attr()
        self.add_ovs_common_attr()
        for i in ovs_bond:
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
        self.widget_dict["bonding_options"] = Text(label="bonding_options", name="bonding_options")
        self.layout1.add_widget(self.widget_dict["bonding_options"])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_close(self, choice):
        if choice == 0:
            self.ovs_data = deepcopy(self.data)
            self.ovs_data["addresses"] = deepcopy(self.address_list)
            self.ovs_data["dns_servers"] = deepcopy(self.dns_list)
            self.ovs_data["domain"] = deepcopy(self.domain_list)
            self.ovs_data["routes"] = deepcopy(self.route_list)
            self.ovs_data["rules"] = deepcopy(self.rule_list)
            self.ovs_data["members"] = deepcopy(self.member_list)
            self.ovs_data["ovs_extra"] = deepcopy(self.ovs_extra_list)
            for i in ovs_common:
                if i in self.ovs_data.keys():
                    self.ovs_data["type"] = "ovs_bond"
                    if "bonding_options" in self.ovs_data.keys():
                        self.ovs_data.pop("bonding_options")
            if "bonding_options" in self.ovs_data.keys():
                self.ovs_data["type"] = "linux_bond"
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

    def _on_load(self):
        super()._on_load()
        self.data["type"] = "ovs_bond"
        if "bonding_options" in self._model.current_network_object:
            self.data["bonding_options"] = self._model.current_network_object["bonding_options"]
            self.widget_dict["bonding_options"].value = self._model.current_network_object["bonding_options"]
        else:
            self.widget_dict["bonding_options"].value = ""
        self.fill_ovs_common_attr()

    def _add_option(self):
        self.widget_dict["OptionPopUp"] = PopUpDialog(self._screen, "Enter new option",
                                                      ["OK", "Cancel"], on_close=self._option_on_close)
        self.widget_dict["OptionPopUp"]._layouts[0].add_widget(Text("Here:", validator=self._model.name_validator,
                                                                    name="text"))
        self.widget_dict["OptionPopUp"].fix()
        self.scene.add_effect(self.widget_dict["OptionPopUp"])

    def get_available_members(self):
        self.available_members = []
        if len(self._model.ovs_objects):
            for net_object in self._model.ovs_objects:
                if net_object["type"] in ["interface", "ovs_bridge", "linux_bridge", "vlan"] \
                        and net_object not in self.member_list \
                        and net_object not in self._model.ovs_members:
                    self.available_members.append(net_object)

    def _option_on_close(self, choice):
        if choice == 0:
            self.widget_dict["OptionPopUp"].save()
            self.ovs_extra_list.append(self.widget_dict["OptionPopUp"].data["text"])
            if len(self.ovs_extra_list):
                if self.widget_dict["ovs_extra"].options == [("None", None)]:
                    self.widget_dict["ovs_extra"].options = []
                self.widget_dict["ovs_extra"].options.append((self.widget_dict["OptionPopUp"].data["text"],
                                                              self.widget_dict["OptionPopUp"].data["text"]))
                self.widget_dict["ovs_extra"]._required_height = len(self.ovs_extra_list)
            self.fix()

    def _show_option(self):
        self.selected_option = self.widget_dict["ovs_extra"].value

    def _delete_option(self):
        if self.selected_option is not None:
            while (self.selected_option, self.selected_option) in self.widget_dict["ovs_extra"].options:
                self.widget_dict["ovs_extra"].options.remove((self.selected_option, self.selected_option))
                self.ovs_extra_list.remove(self.selected_option)
                self.widget_dict["ovs_extra"]._required_height -= 1
            if not len(self.ovs_extra_list):
                self.widget_dict["ovs_extra"]._required_height = 1
                self.widget_dict["ovs_extra"].options = [("None", None)]
            self.selected_option = None
            self.fix()
