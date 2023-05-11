from copy import deepcopy
from os import mkdir, chdir
from os.path import exists

import rm
import yaml
from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Button, Divider, ListBox, PopUpDialog, Text

from interruptframe import InterruptFrame
from utils import list_files, to_asciimatics_list, write_to_file, read_from_yaml, get_interfaces, remove_deep_member, \
    remove_vlan_members


class ConfigsModel(object):
    current_config_name = None
    config_list = []
    ovs_objects = []
    ovs_members = []
    linux_objects = []
    linux_members = []
    current_config_raw = None
    _ovs_checkbox = False
    _linux_checkbox = False
    _delete_list = []
    current_network_object = {}  # ovs_data
    edit_mode = False
    member_edit = False
    nic_names = []
    ovs_edit_objects = []
    linux_edit_objects = []

    # Methods for Configs
    @staticmethod
    def get_configs():
        if exists("Configs"):
            chdir("Configs")
            config_list = list_files("*_ovs.yaml")
            temp_wrong_file_list = list_files("Alt_configs/*_ovs.yaml")
            temp_file_list = []
            if len(temp_wrong_file_list):
                for i in temp_wrong_file_list:
                    temp_file_list.append(i[12: len(i): 1])
            config_list += temp_file_list
            if len(config_list) == 0:
                chdir("..")
                return [("None", None)]
            chdir("..")
            return to_asciimatics_list(config_list)
        else:
            return [("None", None)]

    def add_config(self, config_name):
        self.current_config_name = config_name

    def write_config(self, linux_mode=False):
        if not exists("Configs"):
            mkdir("Configs")
        if not exists("Configs/Alt_configs"):
            mkdir("Configs/Alt_configs")
        # touch.touch(str("Configs/" + self.current_config_name + ".yaml"))
        # chdir("Configs")
        # temp = open(self.current_config_name + ".yaml", "w")
        # temp.close()
        # chdir("..")
        if linux_mode:
            if exists("Configs/" + self.current_config_name + "_ovs.yaml"):
                rm.rm("Configs/" + self.current_config_name + "_ovs.yaml")
            if exists("Configs/Alt_configs/" + self.current_config_name + "_linux.yaml"):
                rm.rm("Configs/Alt_configs/" + self.current_config_name + "_linux.yaml")
            write_to_file("Configs/" + self.current_config_name + "_linux.yaml",
                          {"network_config": self.linux_objects})
            write_to_file("Configs/Alt_configs/" + self.current_config_name + "_ovs.yaml",
                          {"network_config": self.ovs_objects})
        else:
            if exists("Configs/" + self.current_config_name + "_linux.yaml"):
                rm.rm("Configs/" + self.current_config_name + "_linux.yaml")
            if exists("Configs/Alt_configs/" + self.current_config_name + "_ovs.yaml"):
                rm.rm("Configs/Alt_configs/" + self.current_config_name + "_ovs.yaml")
            write_to_file("Configs/" + self.current_config_name + "_ovs.yaml",
                          {"network_config": self.ovs_objects})
            write_to_file("Configs/Alt_configs/" + self.current_config_name + "_linux.yaml",
                          {"network_config": self.linux_objects})
        self.ovs_objects = []
        self.linux_objects = []
        return

    @staticmethod
    def delete_config(config_name):
        if config_name is not None:
            if exists("Configs/" + config_name + "_ovs.yaml"):
                rm.rm("Configs/" + config_name + "_ovs.yaml")
            if exists("Configs/" + config_name + "_linux.yaml"):
                rm.rm("Configs/" + config_name + "_linux.yaml")
            if exists("Configs/Alt_configs/" + config_name + "_ovs.yaml"):
                rm.rm("Configs/Alt_configs/" + config_name + "_ovs.yaml")
            if exists("Configs/Alt_configs/" + config_name + "_linux.yaml"):
                rm.rm("Configs/Alt_configs/" + config_name + "_linux.yaml")
            if exists("Configs/Config_members/" + config_name + "_members_ovs.yaml"):
                rm.rm("Configs/Config_members/" + config_name + "_members_ovs.yaml")
            if exists("Configs/Config_members/" + config_name + "_members_linux.yaml"):
                rm.rm("Configs/Config_members/" + config_name + "_members_linux.yaml")
            if exists("Configs/Alt_config_members/" + config_name + "_members_ovs.yaml"):
                rm.rm("Configs/Alt_config_members/" + config_name + "_members_ovs.yaml")
            if exists("Configs/Alt_config_members/" + config_name + "_members_linux.yaml"):
                rm.rm("Configs/Alt_config_members/" + config_name + "_members_linux.yaml")

    @staticmethod
    def name_validator(name):
        is_directory = exists("Configs")
        if not is_directory:
            return
        chdir("Configs")
        if name == "" or name is None or len(list_files(name + ".yaml")) != 0:
            chdir("..")
            return
        chdir("..")
        return True

    def write_config_members(self, linux_mode=False):
        if self.current_config_name is not None:
            if not exists("Configs"):
                mkdir("Configs")
            if not exists("Configs/Config_members"):
                mkdir("Configs/Config_members")
            if not exists("Configs/Alt_config_members"):
                mkdir("Configs/Alt_config_members")
            if linux_mode:
                if exists("Configs/Config_members/" + self.current_config_name + "_members_ovs.yaml"):
                    rm.rm("Configs/Config_members/" + self.current_config_name + "_members_ovs.yaml")
                if exists("Configs/Alt_config_members/" + self.current_config_name + "_members_linux.yaml"):
                    rm.rm("Configs/Alt_config_members/" + self.current_config_name + "_members_linux.yaml")
                write_to_file("Configs/Config_members/" + self.current_config_name + "_members_linux.yaml",
                              self.linux_members)
                write_to_file("Configs/Alt_config_members/" + self.current_config_name + "_members_ovs.yaml",
                              self.ovs_members)
            else:
                if exists("Configs/Config_members/" + self.current_config_name + "_members_linux.yaml"):
                    rm.rm("Configs/Config_members/" + self.current_config_name + "_members_linux.yaml")
                if exists("Configs/Alt_config_members/" + self.current_config_name + "_members_ovs.yaml"):
                    rm.rm("Configs/Alt_config_members/" + self.current_config_name + "_members_ovs.yaml")
                write_to_file("Configs/Config_members/" + self.current_config_name + "_members_ovs.yaml",
                              self.ovs_members)
                write_to_file("Configs/Alt_config_members/" + self.current_config_name + "_members_linux.yaml",
                              self.linux_members)

    def get_config_members(self):
        if self.current_config_name is not None:
            if exists("Configs/Config_members"):
                temp_members = read_from_yaml("Configs/Config_members/" + self.current_config_name + "_members_ovs.yaml")
                self.ovs_members = temp_members if temp_members is not None else []
                temp_members = read_from_yaml("Configs/Config_members/" + self.current_config_name + "_members_linux.yaml")
                self.linux_members = temp_members if temp_members is not None else []
            if exists("Configs/Alt_config_members"):
                temp_members = read_from_yaml("Configs/Alt_config_members/" + self.current_config_name + "_members_ovs.yaml")
                self.ovs_members += temp_members if temp_members is not None else []
                temp_members = read_from_yaml("Configs/Alt_config_members/" + self.current_config_name + "_members_linux.yaml")
                self.linux_members += temp_members if temp_members is not None else []

    def get_interface_names(self):
        if exists("mapping.yaml"):
            mappings_dict = read_from_yaml("mapping.yaml")["interface_mapping"]
            nic_list = []
            for i in mappings_dict:
                nic_list.append(i)
            nic_list += get_interfaces()
            self.nic_names = nic_list

    # Methods for NewConfig

    def discard_config_changes(self):
        self.current_config_name = None
        self.ovs_objects = []
        self.ovs_members = []
        self.linux_objects = []
        self.linux_members = []

    def get_raw_config(self):
        if self.ovs_objects:
            self.current_config_raw = yaml.dump(self.ovs_objects)
            return True
        else:
            return False

    def handle_ovs_object(self, data):
        if self.current_config_name is not None and data is not None:
            self.ovs_objects.append(data)

    def handle_linux_object(self, data):
        if self.current_config_name is not None and data is not None:
            self.linux_objects.append(data)

    def remove_object(self, object_to_remove):

        linux_object_to_remove = deepcopy(object_to_remove)

        if object_to_remove in self.ovs_objects:
            if "members" in object_to_remove.keys():
                for i in object_to_remove["members"]:
                    self.ovs_members.remove(i)
                    if i["type"] == "vlan":
                        i.pop("device")
                    self.ovs_objects.append(i)
            self.ovs_objects.remove(object_to_remove)

        if object_to_remove in self.ovs_members:
            for i in self.ovs_objects:
                remove_deep_member(i, object_to_remove)
            self.ovs_members.remove(object_to_remove)

        if "members" in linux_object_to_remove.keys():
            for i in linux_object_to_remove["members"]:
                if i["type"] == "vlan":
                    self.linux_members.remove(i)
                    self.linux_objects.remove(i)
                    linux_object_to_remove["members"].remove(i)
                    i.pop("device")
                    self.linux_objects.append(i)
            if not linux_object_to_remove["members"]:
                linux_object_to_remove.pop("members")

        remove_vlan_members(linux_object_to_remove)

        if linux_object_to_remove in self.linux_objects:
            if linux_object_to_remove["type"] == "vlan":
                if "device" in linux_object_to_remove.keys():
                    self.linux_members.remove(linux_object_to_remove)
                self.linux_objects.remove(linux_object_to_remove)
            else:
                if "members" in linux_object_to_remove.keys():
                    for i in linux_object_to_remove["members"]:
                        self.linux_objects.append(i)
                        self.linux_members.remove(i)
                self.linux_objects.remove(linux_object_to_remove)
        if linux_object_to_remove in self.linux_members:
            if linux_object_to_remove["type"] != "vlan":
                for i in self.linux_objects:
                    remove_deep_member(i, linux_object_to_remove)
            self.linux_members.remove(linux_object_to_remove)
        self.current_network_object = {}

    def add_interface(self):
        raise NextScene("Interface")

    def add_vlan(self):
        raise NextScene("Vlan")

    def add_linux_bridge(self):
        raise NextScene("LinuxBridge")

    def add_linux_bond(self):
        raise NextScene("LinuxBond")

    def add_ovs_bridge(self):
        raise NextScene("OVSBridge")

    def add_ovs_bond(self):
        raise NextScene("OVSBond")

    def add_ovs_user_bridge(self):
        raise NextScene("OVSUserBridge")

    def add_ovs_dpdk_bond(self):
        raise NextScene("OVSDpdkBond")

    def add_ovs_dpdk_port(self):
        raise NextScene("OVSDpdkPort")


class ConfigsFrame(InterruptFrame):
    selected_config = None

    @staticmethod
    def get_title():
        return "Configs"

    def init_layout(self):
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1, 1])
        self.add_layout(layout1)
        # layout_browse = Layout([1, 1, 1, 1])
        # self.add_layout(layout_browse)
        # layout_browse.add_widget(FileBrowser(6, "./../../PseudoConfigs/", "Browse"))
        layout1.add_widget(Button("OK", self._cancel))
        layout1.add_widget(Button("Add", self._add), 1)
        layout1.add_widget(Button("Edit", self._edit), 2)
        layout1.add_widget(Button("Delete", self._delete), 3)
        gap_layout2 = Layout([1])
        self.add_layout(gap_layout2)
        gap_layout2.add_widget(Divider(draw_line=False, height=3))
        layout2 = Layout([1, 3], True)
        self.add_layout(layout2)
        self.configs_list = ListBox(1, [("None", None)], on_select=self._show, name="configs_list")
        layout2.add_widget(self.configs_list)
        # descriptions = [("Description1", 1), ("Description2", 2), ("Description3", 3)]
        # layout2.add_widget(ListBox(3, descriptions), 1)
        self.fix()

    def _add(self):
        self.pop_up = PopUpDialog(self._screen, "Enter name", ["OK", "Cancel"], on_close=self._on_close)
        # pop_layout = Layout([1])
        # pop_up.add_layout(pop_layout)
        self.pop_up._layouts[0].add_widget(Text("Here:", validator=self._model.name_validator, name="text"))
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    def _on_close(self, choice):
        if choice == 0:
            self.pop_up.save()
            self._model.add_config(self.pop_up.data["text"])
            raise NextScene("NewConfig")
        else:
            return

    def _edit(self):
        if self.selected_config is not None:
            self.save()
            self._model.current_config_name = self.configs_list.value[0: len(self.configs_list.value) - 9]
            self._model.ovs_objects = read_from_yaml("Configs/" + self._model.current_config_name + "_ovs.yaml")
            if self._model.ovs_objects is None:
                self._model.ovs_objects = read_from_yaml("Configs/Alt_configs/" + self._model.current_config_name + "_ovs.yaml")
            self._model.ovs_objects = self._model.ovs_objects["network_config"]
            self._model.linux_objects = read_from_yaml("Configs/" + self._model.current_config_name + "_linux.yaml")
            if self._model.linux_objects is None:
                self._model.linux_objects = read_from_yaml("Configs/Alt_configs/" + self._model.current_config_name + "_linux.yaml")
            self._model.linux_objects = self._model.linux_objects["network_config"]
            self._model.get_config_members()
            raise NextScene("NewConfig")

    def _delete(self):
        if self.selected_config is not None:
            self._model.delete_config(self.configs_list.value[0: len(self.configs_list.value) - 9])
            self.selected_config = None
            self.update_configs_list()

    def _on_load(self):
        self.update_configs_list()

    def _show(self):
        self.save()
        self.selected_config = self.data["configs_list"]
        # self.configs_list.blur()

    def update_configs_list(self):
        self.configs_list.options = self._model.get_configs()
        self.configs_list._required_height = len(self.configs_list.options)
        self.fix()

    def _cancel(self):
        raise NextScene("Home")
