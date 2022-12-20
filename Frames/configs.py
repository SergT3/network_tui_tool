import os
from os import mkdir, chdir

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Button, Divider, ListBox, PopUpDialog, Text

from interruptframe import InterruptFrame
from utils import list_files, exists, to_asciimatics_list


class ConfigsModel(object):
    _last_created_config = None
    _last_config_raw = None
    _ovs_checkbox = False
    _linux_checkbox = False

    # Methods for Configs
    @staticmethod
    def get_configs():
        is_directory = exists("Configs")
        if not is_directory:
            return
        chdir("Configs")
        config_list = list_files("*.yaml")
        chdir("..")
        return to_asciimatics_list(config_list)

    def add_config(self, config_name):
        is_directory = exists("Configs")
        if not is_directory:
            mkdir("Configs")
        chdir("Configs")
        temp_file = open(config_name + ".yaml", "w")
        temp_file.close()
        chdir("..")
        self._last_created_config = config_name
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

    def remove_unfinished_config(self):
        os.chdir("Configs")
        os.remove(self._last_created_config + ".yaml")
        os.chdir("..")
        self._last_created_config = None

    # def ovs(self):
    #     if self._ovs_checkbox == self._linux_checkbox:
    #         self
    #     temp = self._ovs_checkbox
    #     self._linux_checkbox = temp
    #     self._ovs_checkbox = not temp
    #
    # def linux(self):
    #     temp = self._linux_checkbox
    #     self._ovs_checkbox = temp
    #     self._linux_checkbox = not temp

    def get_raw_config(self, filename=_last_created_config):
        os.chdir("Configs")
        try:
            temp = open(filename + ".yaml", mode="r")
        except Exception:
            chdir("..")
            return False
        if os.stat(filename + ".yaml").st_size == 0:
            return False
        raw = temp.readlines()
        self._last_config_raw = raw
        temp.close()
        chdir("..")
        return True

    def add_interface(self):
        pass

    def add_vlan(self):
        pass

    def add_linux_bridge(self):
        pass

    def add_linux_bond(self):
        pass

    def add_ovs_bridge(self):
        pass

    def add_ovs_bond(self):
        pass

    def add_ovs_user_bridge(self):
        pass

    def add_ovs_dpdk_bond(self):
        pass

    def add_ovs_dpdk_port(self):
        pass


class ConfigsFrame(InterruptFrame):

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
        layout1.add_widget(Button("Save", self._save_update))
        layout1.add_widget(Button("Add", self._add), 1)
        layout1.add_widget(Button("Delete", self._delete), 2)
        layout1.add_widget(Button("Cancel", self._cancel), 3)
        gap_layout2 = Layout([1])
        self.add_layout(gap_layout2)
        gap_layout2.add_widget(Divider(draw_line=False, height=3))
        layout2 = Layout([1, 3], True)
        self.add_layout(layout2)
        configs = self._model.get_configs()
        if configs is not None:
            layout2.add_widget(ListBox(len(configs), configs))
        # descriptions = [("Description1", 1), ("Description2", 2), ("Description3", 3)]
        # layout2.add_widget(ListBox(3, descriptions), 1)
        self.fix()

    def _save_update(self):
        raise NextScene("Home")

    def _add(self):
        self.pop_up = PopUpDialog(self._screen, "Enter name for new config", ["OK", "Cancel"], on_close=self._on_close)
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

    def _delete(self):
        pass

    def _cancel(self):
        raise NextScene("Home")
