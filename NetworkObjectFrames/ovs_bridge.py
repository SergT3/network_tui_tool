from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, ListBox, DropdownList, PopUpDialog, MultiColumnListBox

from NetworkObjectFrames.network_object_attributes import ovs_bridge, ovs_common
from NetworkObjectFrames.linux_bridge import LinuxBridgeFrame


class OVSBridgeFrame(LinuxBridgeFrame):

    ovs_extra_list = []
    selected_option = []
    member_list = []

    @staticmethod
    def get_title():
        return "OVSBridge"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "ovs_bridge"
        self.layout1.add_widget(object_type)
        self.add_common_attr()
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
        for i in ovs_bridge:
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
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        super()._on_load()
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
                        if "ovs_extra" in self._model.current_network_object:
                            self.widget_dict[i].options = []
                            for j in self.ovs_extra_list:
                                self.widget_dict[i].options.append((j, j))
                    else:
                        self.data[i] = self._model.current_network_object[i]
                        self.widget_dict[i].value = self._model.current_network_object[i]
        self.fix()

    def _on_close(self, choice):
        if choice == 0:
            self.opt_data = deepcopy(self.data)
            self.opt_data["addresses"] = self.address_list
            self.opt_data["dns_servers"] = self.dns_list
            self.opt_data["domain"] = self.ovs_extra_list
            self.opt_data["routes"] = self.route_list
            self.opt_data["rules"] = self.rule_list
            self.opt_data["ovs_extra"] = self.ovs_extra_list
            self._model.handle_object(self.opt_data)
            self._model.current_network_object = {}
            raise NextScene("NewConfig")

    def _add_option(self):
        self.widget_dict["OptionPopUp"] = PopUpDialog(self._screen, "Enter new option",
                                                      ["OK", "Cancel"], on_close=self._option_on_close)
        self.widget_dict["OptionPopUp"]._layouts[0].add_widget(Text("Here:", validator=self._model.name_validator,
                                                                    name="text"))
        self.widget_dict["OptionPopUp"].fix()
        self.scene.add_effect(self.widget_dict["OptionPopUp"])

    def _option_on_close(self, choice):
        if choice == 0:
            self.widget_dict["OptionPopUp"].save()
            self.ovs_extra_list.append(self.widget_dict["OptionPopUp"].data["text"])
            if len(self.ovs_extra_list) != 0:
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
            if len(self.ovs_extra_list) == 0:
                self.widget_dict["ovs_extra"]._required_height = 1
                self.widget_dict["ovs_extra"].options = [("None", None)]
            self.selected_option = None
            self.fix()

    def get_available_members(self):
        if len(self._model.current_config_object_list) != 0:
            for net_object in self._model.current_config_object_list:
                if net_object["type"] in ["interface","linux_bond", "ovs_bond"]:
                    if net_object["name"] not in self.member_list:
                        self.available_members.append(
                            {"type": net_object["type"], "name": net_object["name"], "mtu": net_object["mtu"]})
                elif net_object["type"] == "vlan":
                    if net_object["device"] not in self.member_list:
                        self.available_members.append(
                            {"type": "vlan", "device": net_object["device"], "mtu": net_object["mtu"]})

