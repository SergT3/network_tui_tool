from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, PopUpDialog, MultiColumnListBox

from NetworkObjectFrames.linux_bridge import LinuxBridgeFrame
from NetworkObjectFrames.network_object_attributes import ovs_bridge
from utils import remove_empty_keys


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
        self.add_ovs_common_attr()
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
        self.fill_ovs_common_attr()

    def _on_close(self, choice):
        if choice == 0:
            self.opt_data = deepcopy(self.data)
            self.opt_data["addresses"] = deepcopy(self.address_list)
            self.opt_data["dns_servers"] = deepcopy(self.dns_list)
            self.opt_data["domain"] = deepcopy(self.ovs_extra_list)
            self.opt_data["routes"] = deepcopy(self.route_list)
            self.opt_data["rules"] = deepcopy(self.rule_list)
            self.opt_data["members"] = deepcopy(self.member_list)
            self.opt_data["ovs_extra"] = deepcopy(self.ovs_extra_list)
            self.opt_data = remove_empty_keys(self.opt_data)
            if self._model.edit_mode:
                if self._model.current_network_object in self._model.current_config_objects:
                    self._model.current_config_objects.remove(self._model.current_network_object)
                elif self._model.current_network_object in self._model.current_config_members:
                    self._model.current_config_members.remove(self._model.current_network_object)
            self._model.edit_mode = False
            self._model.handle_object(self.opt_data)
            self._model.write_config_members()
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

    def get_available_members(self):
        if len(self._model.current_config_objects):
            for net_object in self._model.current_config_objects:
                if net_object["type"] in ["interface", "linux_bond", "ovs_bond"] \
                        and net_object not in self.member_list \
                        and net_object not in self._model.current_config_members:
                    self.available_members.append(net_object)

