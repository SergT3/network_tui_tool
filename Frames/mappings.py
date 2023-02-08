from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Divider, ListBox, DropdownList, Button, PopUpDialog, Text

from interruptframe import InterruptFrame
from utils import get_interfaces, to_asciimatics_list, dup_list_util, write_to_file


class MappingsModel(object):
    # def __init__(self):
    #     self.get_user_data()

    # @staticmethod
    # def update_nic_list(data, new_nic, nic_list_type=None):
    #     try:
    #         if data[nic_list_type] is not None:
    #             data[nic_list_type].append((new_nic, new_nic))
    #     except KeyError as e:
    #         data[nic_list_type] = [(new_nic, new_nic)]
    #     return

    @staticmethod
    def remove_nic(nic_list, nic_name):
        # try:
        #     nic_list.remove((nic_name, nic_name))
        # except Exception:
        #     return
        nic_list.remove((nic_name, nic_name))

    # this function writes to mappings.yaml
    @staticmethod
    def mapping_writer(data, length):
        interface_dict = {}
        temp = []
        for i in range(1, length + 1):
            temp.append({data[str(-i)]: data[str(i)]})
        interface_dict["interface_mapping"] = temp
        return write_to_file("mapping.yaml", interface_dict)

    @staticmethod
    def save_data(data):
        write_to_file("Mappings_data.yaml", data)

    # @staticmethod
    # def get_data(data):
    #     data = read_dict_from_yaml("Mappings_data.yaml")


class MappingsFrame(InterruptFrame):
    _selected_nic = None

    @staticmethod
    def get_title():
        return "Mappings"

    def init_layout(self):
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout2 = Layout([1, 1, 1, 1, 1], True)
        self.add_layout(layout2)
        self.hardware_objects = to_asciimatics_list(get_interfaces())
        try:
            self.nic_list = self.data["nic_list"]
        except KeyError:
            self.nic_list = None
        try:
            self.nic_show_list = self.data["nic_show_list"]
        except KeyError:
            self.nic_show_list = None
        if self.nic_list is None:
            self.nic_list = to_asciimatics_list(dup_list_util("nic", len(self.hardware_objects)), True)
        if self.nic_show_list is None:
            self.nic_show_list = to_asciimatics_list(dup_list_util("nic", len(self.hardware_objects)))
        for i in range(1, len(self.hardware_objects) + 1):
            layout2.add_widget(ListBox(1, [self.hardware_objects[i - 1]], name=str(i)))
            layout2.add_widget(DropdownList(self.nic_list, on_change=self._on_change, name=str(-i)), 1)
        self._nic_menu = ListBox(len(self.nic_show_list), self.nic_show_list, on_select=self._show,
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
        try:
            if self.data["nic_list"]:
                self.nic_list = self.data["nic_list"]
            if self.data["nic_show_list"]:
                self.nic_show_list = self.data["nic_show_list"]
        except KeyError:
            return

    def _on_select(self):
        self.save()

    def _on_change(self):
        self.save()

    def _show(self):
        self.save()
        self._selected_nic = self.data["nic_menu"]

    def _save_update(self):
        self.save()
        self._model.mapping_writer(self.data, len(self.hardware_objects))
        self.data["nic_list"] = self.nic_list
        self.data["nic_show_list"] = self.nic_show_list
        self._model.save_data(self.data)
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
            self.nic_list.append((self.pop_up.data["newname"], self.pop_up.data["newname"]))
            self.nic_show_list.append((self.pop_up.data["newname"], self.pop_up.data["newname"]))
        else:
            pass

    def _delete(self):
        if self._selected_nic is not None:
            self._model.remove_nic(self.nic_list, self._selected_nic)
            self._model.remove_nic(self.nic_show_list, self._selected_nic)
            self.fix()
            self.save()
            self._selected_nic = None
        return

    def _cancel(self):
        raise NextScene("Home")
