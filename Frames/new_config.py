# from copy import deepcopy
from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Label, Divider, Button, CheckBox, MultiColumnListBox, PopupMenu, PopUpDialog

from interruptframe import InterruptFrame
from utils import write_to_file


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
        if self._model.current_network_object != {}:
            if self._model.current_network_object["type"] == "vlan":
                self.object_list.options.append(([self._model.current_network_object["vlan_id"],
                                                  self._model.current_network_object["type"]],
                                                 self._model.current_network_object))
            else:
                self.object_list.options.append(([self._model.current_network_object["name"],
                                                  self._model.current_network_object["type"]],
                                                 self._model.current_network_object))
            self._model.current_network_object = {}
        if self.object_list.options != [(["None"], None)]:
            if (["None"], None) in self.object_list.options:
                self.object_list.options.remove((["None"], None))
        self.object_list._required_height = len(self.object_list.options)
        self.fix()
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
            if self.selected_object in self._model.ovs_members:
                for i in self._model.ovs_objects:
                    if self.selected_object in i["members"]:
                        i["members"].remove(self.selected_object)
                        self._model.ovs_edit_objects.append(i)
                self._model.ovs_members.remove(self.selected_object)
            elif self.selected_object in self._model.ovs_objects:
                self._model.ovs_objects.remove(self.selected_object)

            linux_selected_object = deepcopy(self.selected_object)
            if "members" in linux_selected_object.keys():
                for i in linux_selected_object["members"]:
                    if i["type"] == "vlan":
                        linux_selected_object["members"].remove(i)
                if not linux_selected_object["members"]:
                    linux_selected_object.pop("members")

            if linux_selected_object in self._model.linux_members:
                if linux_selected_object["type"] == "vlan":
                    self._model.linux_objects.remove(linux_selected_object)
                    self._model.linux_members.remove(linux_selected_object)
                else:
                    for i in self._model.linux_objects:
                        if linux_selected_object in i["members"]:
                            i["members"].remove(linux_selected_object)
                            self._model.linux_edit_objects.append(i)
                    self._model.linux_members.remove(linux_selected_object)

            elif linux_selected_object in self._model.linux_objects:
                self._model.linux_objects.remove(linux_selected_object)

            self._model.edit_mode = True
            self._model.current_network_object = self.selected_object
            obj_type = self._model.current_network_object["type"]
            self.selected_object = None

            if obj_type == "interface":
                raise NextScene("Interface")
            if obj_type == "vlan":
                raise NextScene("Vlan")
            if obj_type == "linux_bond":
                raise NextScene("LinuxBond")
            if obj_type == "linux_bridge":
                raise NextScene("LinuxBridge")
            if obj_type == "ovs_bond":
                raise NextScene("OVSBond")
            if obj_type == "ovs_bridge":
                raise NextScene("OVSBridge")
            if obj_type == "ovs_dpdk_bond":
                raise NextScene("OVSDpdkBond")
            if obj_type == "ovs_dpdk_port":
                raise NextScene("OVSDpdkPort")
            if obj_type == "ovs_user_bridge":
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
            self._model.write_config(self.linux_mode.value)
            self._model.write_config_members(self.linux_mode.value)
            self._model.current_config = None
            self._model.ovs_objects = []
            self._model.ovs_members = []
            self._model.linux_objects = []
            self._model.linux_members = []
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
            self.object_list.options = []
            if self._model.ovs_objects or self._model.ovs_members:
                for i in (self._model.ovs_objects + self._model.ovs_members):
                    write_to_file("example", self._model.ovs_objects + self._model.ovs_members)
                    if i["type"] == "vlan":
                        if ([i["vlan_id"], i["type"]], i) not in self.object_list.options:
                            self.object_list.options.append(([i["vlan_id"], i["type"]], i))
                    else:
                        if ([i["name"], i["type"]], i) not in self.object_list.options:
                            self.object_list.options.append(([i["name"], i["type"]], i))
            else:
                self.object_list.options = [(["None"], None)]
        self.object_list._required_height = len(self.object_list.options)
        self.fix()