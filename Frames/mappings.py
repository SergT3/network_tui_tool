from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Divider, ListBox, DropdownList, Button, PopUpDialog, Text, Label
from frame import InterruptFrame
from utils import get_interfaces, to_asciimatics_list, indexed_dup_list, write_to_file, read_from_yaml
from os.path import exists


class MappingsModel(object):
    nic_list = []
    nic_show_list = []
    hardware_objects = []

    @staticmethod
    def remove_nic(nic_list, nic_name):
        while (nic_name, nic_name) in nic_list:
            nic_list.remove((nic_name, nic_name))

    # this function writes to mappings.yaml
    @staticmethod
    def mapping_writer(data, length):
        interface_dict = {}
        mapping_dict = {}
        for i in range(1, length + 1):
            if data[str(-i)] is not None:
                mapping_dict[data[str(-i)]] = data[str(i)]
        interface_dict["interface_mapping"] = mapping_dict
        return write_to_file("mapping.yaml", interface_dict)

    @staticmethod
    def save_custom_nics(custom_nics):
        custom_nic_list = []
        for i in custom_nics:
            custom_nic_list.append(i[0])
        write_to_file("custom_nics.yaml", custom_nic_list)

    @staticmethod
    def get_nics():
        if exists("custom_nics.yaml"):
            return read_from_yaml("custom_nics.yaml")
        return []


class MappingsFrame(InterruptFrame):
    _selected_nic = None

    @staticmethod
    def frame_title():
        return "Mappings"

    def init_layout(self):
        self.widget_dict = {}
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout2 = Layout([1, 1, 1, 1, 1], True)
        self.add_layout(layout2)
        layout2.add_widget(Label("Interface mappings:"))
        layout2.add_widget(Divider(1), 1)
        self._on_load()
        for i in range(1, len(self._model.hardware_objects) + 1):
            self.widget_dict[str(i)] = ListBox(1, [self._model.hardware_objects[i - 1]], name=str(i))
            self.widget_dict[str(-i)] = DropdownList(self._model.nic_list, on_change=self._on_change, name=str(-i))
            layout2.add_widget(self.widget_dict[str(i)])
            layout2.add_widget(self.widget_dict[str(-i)], 1)
        self.fill_nics()
        layout2.add_widget(Label("Identifiers:"), 4)
        self._nic_menu = ListBox(len(self._model.nic_show_list), self._model.nic_show_list, on_select=self._show,
                                 name="nic_menu", add_scroll_bar=True)
        layout2.add_widget(self._nic_menu, 4)
        layout3 = Layout([1, 1, 1, 1])
        self.add_layout(layout3)
        layout3.add_widget(Button("Save", self._save_update))
        layout3.add_widget(Button("Add", self._add), 1)
        layout3.add_widget(Button("Delete", self._delete), 2)
        layout3.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        self._model.hardware_objects = to_asciimatics_list(get_interfaces())
        self._model.nic_list = to_asciimatics_list(self._model.get_nics(), True)
        self._model.nic_show_list = to_asciimatics_list(self._model.get_nics())
        if not self._model.nic_list or not self._model.nic_show_list:
            self._model.nic_list = to_asciimatics_list(indexed_dup_list("nic", len(self._model.hardware_objects)), True)
            self._model.nic_show_list = to_asciimatics_list(indexed_dup_list("nic", len(self._model.hardware_objects)))
        if "1" in self.widget_dict.keys():
            self.fill_nics()

    def fill_nics(self):
        if exists("mapping.yaml"):
            mapping_dict = read_from_yaml("mapping.yaml")["interface_mapping"]
            for i in range(1, len(self._model.hardware_objects) + 1):
                for j in mapping_dict:
                    if self.widget_dict[str(i)].value == mapping_dict[j]:
                        self.widget_dict[str(-i)].value = j
                        break
            self.fix()

    def _on_select(self):
        self.save()

    def _on_change(self):
        self.save()

    def _show(self):
        self.save()
        self._selected_nic = self.data["nic_menu"]

    def _save_update(self):
        self.save()
        self._model.mapping_writer(self.data, len(self._model.hardware_objects))
        self.data["nic_list"] = self._model.nic_list
        self.data["nic_show_list"] = self._model.nic_show_list
        self._model.save_custom_nics(self._model.nic_show_list)
        raise NextScene("Home")

    def _add(self):
        self.pop_up = PopUpDialog(self._screen, "New interface name:", ["OK", "Cancel"],
                                  on_close=self._on_close)
        self.pop_up._layouts[0].add_widget(Text(name="newname"))
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    def _on_close(self, choice):
        if choice == 0:
            self.pop_up.save()
            self._model.nic_list.append((self.pop_up.data["newname"], self.pop_up.data["newname"]))
            self._model.nic_show_list.append((self.pop_up.data["newname"], self.pop_up.data["newname"]))
            for i in range(1, len(self._model.hardware_objects) + 1):
                self.widget_dict[str(-i)].options = self._model.nic_list
            self._nic_menu.options = self._model.nic_show_list
            self._nic_menu._required_height += 1
            self.fix()
        else:
            pass

    def _delete(self):
        if self._selected_nic is not None:
            self._model.remove_nic(self._model.nic_list, self._selected_nic)
            self._model.remove_nic(self._model.nic_show_list, self._selected_nic)
            self.save()
            for i in range(1, len(self._model.hardware_objects) + 1):
                self.widget_dict[str(-i)].options = self._model.nic_list
            self._nic_menu.options = self._model.nic_show_list
            self._nic_menu._required_height -= 1
            self.fix()
            self._selected_nic = None
        return

    def _cancel(self):
        raise NextScene("Home")
