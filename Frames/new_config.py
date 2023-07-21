from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Label, Divider, Button, CheckBox, MultiColumnListBox, PopupMenu, PopUpDialog

from NetworkObjectFrames.network_object_attributes import ovs_common
from frame import InterruptFrame

from utils import remove_vlan_members


class NewConfigFrame(InterruptFrame):
    selected_object = None
    ovs_mode = None
    linux_mode = None

    @staticmethod
    def frame_title():
        return "NewConfig"

    def init_layout(self):

        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        self.config_name = Label("")
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        gap_layout1.add_widget(self.config_name)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))

        # layout1.add_widget(Button("Raw", self._raw), 1)
        # self.ovs_box = CheckBox("OVS", on_change=self._checkbox, name="OVS")
        # self.linux_box = CheckBox("Linux", on_change=self._checkbox, name="linux")
        # layout1.add_widget(self.ovs_box, 2)
        # layout1.add_widget(self.linux_box, 3)
        gap_layout2 = Layout([1])
        self.add_layout(gap_layout2)
        gap_layout2.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1, 1, 1])
        self.add_layout(layout1)
        layout1.add_widget(Button("Save", self._save_update))
        layout1.add_widget(Button("Add", self._add), 1)
        layout1.add_widget(Button("Edit", self._edit), 2)
        layout1.add_widget(Button("Delete", self._delete), 3)
        layout1.add_widget(Button("Cancel", self._cancel), 4)
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

        self.pop_up_menu_list = [
            ("interface", self._model.add_interface),
            ("vlan", self._model.add_vlan),
            ("bridge", self._model.add_linux_bridge),
            ("bond", self._model.add_linux_bond),
            ("OVS_user_bridge", self._model.add_ovs_user_bridge),
            ("OVS_dpdk_bond", self._model.add_ovs_dpdk_bond),
            ("OVS_dpdk_port", self._model.add_ovs_dpdk_port)
        ]

        self._model.get_config_members()
        self.update_object_list()
        if self._model.current_network_object != {}:
            if self._model.current_network_object["type"] == "vlan":
                self.object_list.options.append(([self._model.current_network_object["vlan_id"],
                                                  self._model.current_network_object["type"]],
                                                 self._model.current_network_object))
            elif self._model.current_network_object["type"] in ["linux_bond", "ovs_bond"]:
                self.object_list.options.append(([self._model.current_network_object["name"], "bond"],
                                                 self._model.current_network_object))
            elif self._model.current_network_object["type"] in ["linux_bridge", "ovs_bridge"]:
                self.object_list.options.append(([self._model.current_network_object["name"], "bridge"],
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

    def _show(self):
        self.save()
        self.selected_object = self.object_list.value

    def _edit(self):
        if self.selected_object is not None:
            if self.selected_object in self._model.ovs_members:
                for i in self._model.ovs_objects:
                    if "members" in i.keys():
                        if self.selected_object in i["members"]:
                            i["members"].remove(self.selected_object)
                            self._model.ovs_edit_objects.append(i)
                self._model.ovs_members.remove(self.selected_object)
            elif self.selected_object in self._model.ovs_objects:
                self._model.ovs_objects.remove(self.selected_object)

            linux_selected_object = deepcopy(self.selected_object)
            remove_vlan_members(linux_selected_object)

            if linux_selected_object in self._model.linux_members:
                if linux_selected_object["type"] == "vlan":
                    self._model.linux_objects.remove(linux_selected_object)
                    self._model.linux_members.remove(linux_selected_object)
                else:
                    for i in self._model.linux_objects:
                        if "members" in i.keys():
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
                raise NextScene("OVSBond")
            if obj_type == "linux_bridge":
                raise NextScene("OVSBridge")
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
            if self.linux_mode.value:
                self.linux_swap()
            else:
                self.ovs_swap()
            self._model.write_config(self.linux_mode.value)
            self._model.write_config_members(self.linux_mode.value)
            self._model.current_config_name = None
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
            elif self.selected_object["type"] in ["linux_bond", "ovs_bond"]:
                self.object_list.options.remove(([self.selected_object["name"], "bond"], self.selected_object))
            elif self.selected_object["type"] in ["linux_bridge", "ovs_bridge"]:
                self.object_list.options.remove(([self.selected_object["name"], "bridge"], self.selected_object))
            elif ([self.selected_object["name"], self.selected_object["type"]], self.selected_object) in self.object_list.options:
                self.object_list.options.remove(([self.selected_object["name"], self.selected_object["type"]], self.selected_object))
            self.fix()
        self.selected_object = None


    def _cancel(self):
        self._model.discard_config_changes()
        raise NextScene("Configs")

    def update_object_list(self):
        if self._model.current_config_name is not None:
            self.config_name.text = self._model.current_config_name
            self.object_list.options = []
            if self._model.ovs_objects or self._model.ovs_members:
                for i in (self._model.ovs_objects + self._model.ovs_members):
                    if i["type"] == "vlan":
                        if ([i["vlan_id"], i["type"]], i) not in self.object_list.options:
                            self.object_list.options.append(([i["vlan_id"], i["type"]], i))
                    elif i["type"] in ["linux_bond", "ovs_bond"]:
                        if ([i["name"], i["type"]], i) not in self.object_list.options:
                            self.object_list.options.append(([i["name"], "bond"], i))
                    elif i["type"] in ["linux_bridge", "ovs_bridge"]:
                        if ([i["name"], i["type"]], i) not in self.object_list.options:
                            self.object_list.options.append(([i["name"], "bridge"], i))
                    else:
                        if ([i["name"], i["type"]], i) not in self.object_list.options:
                            self.object_list.options.append(([i["name"], i["type"]], i))
            else:
                self.object_list.options = [(["None"], None)]
        self.object_list._required_height = len(self.object_list.options)
        self.fix()

    def ovs_swap(self):
        for i in self._model.ovs_objects + self._model.ovs_members + self._model.linux_objects + self._model.linux_members:
            self.ovs_swap_util(i)
            if "members" in i.keys():
                for j in i["members"]:
                    if j["type"] in ["linux_bridge", "linux_bond"]:
                        self.ovs_swap_util(j)

    def linux_swap(self):
        for i in self._model.ovs_objects + self._model.ovs_members + self._model.linux_objects + self._model.linux_members:
            self.linux_swap_util(i)
            if "members" in i.keys():
                for j in i["members"]:
                    if j["type"] in ["ovs_bridge", "ovs_bond"]:
                        self.linux_swap_util(j)

    @staticmethod
    def ovs_swap_util(net_object):
        if net_object["type"] == "linux_bridge":
            net_object["type"] = "ovs_bridge"
        if net_object["type"] == "linux_bond":
            net_object["type"] = "ovs_bond"
            if "bonding_options" in net_object.keys():
                net_object.pop("bonding_options")

    @staticmethod
    def linux_swap_util(net_object):
        if net_object["type"] == "ovs_bridge":
            for i in list(net_object):
                if i in ovs_common:
                    net_object.pop(i)
            net_object["type"] = "linux_bridge"
        if net_object["type"] == "ovs_bond":
            for i in list(net_object):
                if i in ovs_common:
                    net_object.pop(i)
            net_object["type"] = "linux_bond"
