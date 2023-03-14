from os import mkdir, chdir, remove, stat
from os.path import exists

import touch
import yaml
from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Button, Divider, ListBox, PopUpDialog, Text

from interruptframe import InterruptFrame
from utils import list_files, to_asciimatics_list, write_to_file, read_dict_from_yaml,remove_empty_keys


class ConfigsModel(object):
    current_config = None
    config_list = []
    current_config_object_list = []
    current_config_raw = None
    _ovs_checkbox = False
    _linux_checkbox = False
    _delete_list = []
    current_network_object = {}  # opt_data
    edit_mode = False
    # Methods for Configs
    @staticmethod
    def get_configs():
        is_directory = exists("Configs")
        if is_directory:
            chdir("Configs")
            config_list = list_files("*.yaml")
            if len(config_list) == 0:
                chdir("..")
                return [("None", None)]
            chdir("..")
            return to_asciimatics_list(config_list)
        else:
            return [("None", None)]

    def add_config(self, config_name):
        self.current_config = config_name

    def write_config(self):
        if not exists("Configs"):
            mkdir("Configs")
        # touch.touch(str("Configs/" + self.current_config + ".yaml"))
        chdir("Configs")
        temp = open(self.current_config + ".yaml", "w")
        temp.close()
        chdir("..")
        write_to_file("Configs/" + self.current_config + ".yaml", {"network_config": remove_empty_keys(self.current_config_object_list)})
        self.current_config = None
        self.current_config_object_list = []
        return

    @staticmethod
    def delete_config(config_name):
        if config_name is not None:
            chdir("Configs")
            try:
                remove(config_name)
                chdir("..")
            except Exception:
                chdir("..")
                return
        else:
            return

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

    # Methods for NewConfig

    def discard_config_changes(self):
        self.current_config = None
        self.current_config_object_list = []

    def get_raw_config(self):
        if self.current_config_object_list:
            self.current_config_raw = yaml.dump(self.current_config_object_list)
            return True
        else:
            return False

    def handle_object(self, data):
        if self.current_config is not None and data is not None:
            self.current_config_object_list.append(data)

    def remove_object(self, object_to_remove):
        while object_to_remove in self.current_config_object_list:
            self.current_config_object_list.remove(object_to_remove)

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
            self._model.current_config = self.configs_list.value[0: len(self.configs_list.value) - 5]
            self._model.current_config_object_list = \
                (read_dict_from_yaml("Configs/" + self._model.current_config + ".yaml"))["network_config"]
            raise NextScene("NewConfig")

    def _delete(self):
        if self.selected_config is not None:
            self._model.delete_config(self.selected_config)
            self.selected_config = None
            raise NextScene("Configs")

    def _on_load(self):
        self.configs_list.options = self._model.get_configs()
        self.configs_list._required_height = len(self.configs_list.options)

    def _show(self):
        self.save()
        self.selected_config = self.data["configs_list"]
        # self.configs_list.blur()

    def update_configs_list(self):
        self.configs_list.options = self._model.get_configs()
        if len(self._model.current_config_object_list) != 0:
            self.object_list.options = []
            for i in self._model.current_config_object_list:
                self.object_list.options.append(([i["name"], i["type"]], i))
        else:
            self.object_list.options = [(["None"], None)]
        return

    def _cancel(self):
        raise NextScene("Home")
