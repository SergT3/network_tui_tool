# from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Label, Divider, Button, CheckBox, MultiColumnListBox, PopupMenu, PopUpDialog

from interruptframe import InterruptFrame


class NewConfigFrame(InterruptFrame):
    selected_object = None
    ovs_mode = None
    linux_mode = None

    @staticmethod
    def get_title():
        return "NewConfig"

    def init_layout(self):
        self._ovs_menu = [
            ("interface", self._model.add_interface),
            ("vlan", self._model.add_vlan),
            ("OVS_bridge", self._model.add_ovs_bridge),
            ("OVS_bond", self._model.add_ovs_bond),
            ("OVS_user_bridge", self._model.add_ovs_user_bridge),
            ("OVS_dpdk_bond", self._model.add_ovs_dpdk_bond),
            ("OVS_dpdk_port", self._model.add_ovs_dpdk_port)
        ]
        self._linux_menu = [
            ("interface", self._model.add_interface),
            ("vlan", self._model.add_vlan),
            ("linux_bridge", self._model.add_linux_bridge),
            ("linux_bond", self._model.add_linux_bond)
        ]
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        self.config_name = Label("")
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        gap_layout1.add_widget(self.config_name)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1, 1])
        self.add_layout(layout1)
        layout1.add_widget(Button("Edit", self._edit), 0)
        layout1.add_widget(Button("Raw", self._raw), 1)
        self.ovs_box = CheckBox("OVS", on_change=self._checkbox, name="OVS")
        self.linux_box = CheckBox("Linux", on_change=self._checkbox, name="linux")
        layout1.add_widget(self.ovs_box, 2)
        layout1.add_widget(self.linux_box, 3)
        gap_layout2 = Layout([1])
        self.add_layout(gap_layout2)
        gap_layout2.add_widget(Divider(draw_line=False, height=3))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Add", self._add), 1)
        layout2.add_widget(Button("Delete", self._delete), 2)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        gap_layout3 = Layout([1])
        self.add_layout(gap_layout3)
        gap_layout3.add_widget(Divider(draw_line=False, height=3))
        layout3 = Layout([1], True)
        self.add_layout(layout3)
        self.object_list = MultiColumnListBox(1, [self._screen.width // 2 + 1, self._screen.width // 2 - 1],
                                              [(["None"], None)], name="objects_list", on_select=self._show)
        layout3.add_widget(self.object_list)
        self.fix()

    def _on_load(self):
        self._model.get_config_members()
        self.update_object_list()
        self.ovs_box.value = False
        self.linux_box.value = False

    def _show(self):
        self.save()
        self.selected_object = self.object_list.value

    def _checkbox(self):
        if self.ovs_box.value == self.linux_box.value:
            self.ovs_box.disabled = False
            self.linux_box.disabled = False
            self.pop_up_menu_list = self._linux_menu + self._ovs_menu
            self.pop_up_menu_list.remove(("interface", self._model.add_interface))
            self.pop_up_menu_list.remove(("vlan", self._model.add_vlan))
        if self.linux_box.value and not self.ovs_box.value:
            self.pop_up_menu_list = self._linux_menu
            self.ovs_box.disabled = True
        if self.ovs_box.value and not self.linux_box.value:
            self.pop_up_menu_list = self._ovs_menu
            self.linux_box.disabled = True

    def _edit(self):
        if self.selected_object is not None:
            for i in self._model.ovs_current_config_objects + self._model.ovs_current_config_members:
                if i == self.selected_object:
                    self._model.edit_mode = True
                    self._model.current_network_object = i
                    temp_name = self._model.current_network_object["type"]
                    self.selected_object = None
                    if temp_name == "interface":
                        raise NextScene("Interface")
                    if temp_name == "vlan":
                        raise NextScene("Vlan")
                    if temp_name == "linux_bond":
                        raise NextScene("LinuxBond")
                    if temp_name == "linux_bridge":
                        raise NextScene("LinuxBridge")
                    if temp_name == "ovs_bond":
                        raise NextScene("OVSBond")
                    if temp_name == "ovs_bridge":
                        raise NextScene("OVSBridge")
                    if temp_name == "ovs_dpdk_bond":
                        raise NextScene("OVSDpdkBond")
                    if temp_name == "ovs_dpdk_port":
                        raise NextScene("OVSDpdkPort")
                    if temp_name == "ovs_user_bridge":
                        raise NextScene("OVSUserBridge")

    def _raw(self):
        self.save()
        raise NextScene("Raw")

    def save_mode(self):
        if self.ovs_mode.value == self.linux_mode.value:
            self.ovs_mode.disabled = False
            self.linux_mode.disabled = False
        if self.linux_mode.value and not self.ovs_mode.value:
            self.ovs_mode.disabled = True
        if self.ovs_mode.value and not self.linux_mode.value:
            self.linux_mode.disabled = True

    def _save_update(self):
        self.save()
        # write_to_file("data_value_old", self.data)
        self.pop_up = PopUpDialog(self._screen, "Save " + self.config_name.text + " in", ["OK", "Cancel"],
                                  on_close=self._on_close)
        self.ovs_mode = CheckBox("OVS mode", on_change=self.save_mode, name="OVS")
        self.linux_mode = CheckBox("linux mode", on_change=self.save_mode, name="linux")
        self.pop_up._layouts[0].add_widget(self.ovs_mode)
        self.pop_up._layouts[0].add_widget(self.linux_mode)
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    def _on_close(self, choice):
        if choice == 0:
            self._model.write_config()
            self._model.write_config_members()
            # if linux
            #write_config_alt
            #write_config_alt_members
            self._model.current_config = None
            self._model.ovs_current_config_objects = []
            self._model.ovs_current_config_members = []
            raise NextScene("Configs")

    def _add(self):
        self.pop_up = PopupMenu(self._screen, self.pop_up_menu_list, self._screen.width // 4, self._screen.height // 4)
        self.scene.add_effect(self.pop_up)

    def _delete(self):
        if self.selected_object is not None:
            self._model.remove_object(self.selected_object)
            if self.selected_object["type"] == "vlan":
                self.object_list.options.remove(([self.selected_object["vlan_id"], self.selected_object["type"]], self.selected_object))
            else:
                self.object_list.options.remove(([self.selected_object["name"], self.selected_object["type"]], self.selected_object))
            self.selected_object = None
            self.fix()

    def _cancel(self):
        self._model.discard_config_changes()
        raise NextScene("Configs")

    def update_object_list(self):
        if self._model.current_config is not None:
            self.config_name.text = self._model.current_config
            if len(self._model.ovs_current_config_objects) + len(self._model.ovs_current_config_members):
                self.object_list.options = []
                for i in (self._model.ovs_current_config_objects + self._model.ovs_current_config_members):
                    if i["type"] == "vlan":
                        self.object_list.options.append(([i["vlan_id"], i["type"]], i))
                    else:
                        self.object_list.options.append(([i["name"], i["type"]], i))
            else:
                self.object_list.options = [(["None"], None)]
        self.object_list._required_height = len(self.object_list.options)
        self.fix()

# on_load
# if self.linux_mode.value:
#     for i in self._model.current_config_members:
#         if i["type"] == "vlan":
#             for j in self._model.current_config_objects:
#                 if "members" in j.keys():
#                     if i in j["members"]:
#                         j["members"].remove(i)
#                         self._model.current_config_objects.append(i)
#                         i["device"] = j["name"]
#                         i["parent"] = deepcopy(j)
#                         break
#             for j in self._model.current_config_members:
#                 if "members" in j.keys():
#                     if i in j["members"]:
#                         j["members"].remove(i)
#                         self._model.current_config_objects.append(i)
#                         i["device"] = j["name"]
#                         i["parent"] = deepcopy(j)
#                         break
# on_close
# if self.linux_mode.value:
#     for i in self._model.current_config_members:
#         if i["type"] == "vlan":
#             for j in self._model.current_config_objects:
#                 if "members" in j.keys():
#                     if i in j["members"]:
#                         j["members"].remove(i)
#                         self._model.current_config_objects.append(i)
#                         i["device"] = j["name"]
#                         i["parent"] = deepcopy(j)
#                         break
#             for j in self._model.current_config_members:
#                 if "members" in j.keys():
#                     if i in j["members"]:
#                         j["members"].remove(i)
#                         self._model.current_config_objects.append(i)
#                         i["device"] = j["name"]
#                         i["parent"] = deepcopy(j)
#                         break
