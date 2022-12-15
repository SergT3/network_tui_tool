from asciimatics.widgets import Layout, Divider, ListBox, DropdownList, Button, PopUpDialog, Text
from asciimatics.exceptions import NextScene
from myframe import MyFrame
from utils import get_interfaces, to_asciimatics_list, dup_list_util, write_to_file


class MappingsModel(object):
    @staticmethod
    def update_nic_list(nic_list, new_nic):
        return nic_list.append((new_nic, new_nic))

    @staticmethod
    def mapping_writer(data, length):
        interface_dict = {}
        temp = []
        for i in range(1, length + 1):
            temp.append({data[str(-i)]: data[str(i)]})
        interface_dict["interface_mapping"] = temp
        return write_to_file("mapping.yaml", interface_dict)


class MappingsFrame(MyFrame):

    @staticmethod
    def get_title():
        return "Mappings"

    __hardware_objects = []
    __nic_list = []

    def init_layout(self):
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout2 = Layout([1, 1, 1, 1, 1], True)
        self.add_layout(layout2)
        self.__hardware_objects = to_asciimatics_list(get_interfaces())
        # to hardware = hardware()
        self.__nic_list = to_asciimatics_list(dup_list_util("nic", len(self.__hardware_objects)), True)
        # to NICs = NICs()
        # layout2.add_widget(ListBox(len(self.__hardware_objects), self.__hardware_objects, name="list"))
        for i in range(1, len(self.__hardware_objects) + 1):
            layout2.add_widget(ListBox(1, [self.__hardware_objects[i - 1]], name=str(i)))
            layout2.add_widget(DropdownList(self.__nic_list, name=str(-i)), 1)
        #  on_change = self._model.choose_nic(self))
        layout3 = Layout([1, 1, 1, 1])
        self.add_layout(layout3)
        layout3.add_widget(Button("Save", self._save_update))
        layout3.add_widget(Button("Add", self._add), 1)
        layout3.add_widget(Button("Delete", self._delete), 2)
        layout3.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        pass

    def _save_update(self):
        self.save()
        self._model.mapping_writer(self.data, len(self.__hardware_objects))
        raise NextScene("Home")

    def _add(self):
        self.pop_up = PopUpDialog(self._screen, "New interface name:", ["OK", "Cancel"],
                                  on_close=self._on_close)
        self.pop_up._layouts[0].add_widget(Text(name="newname"))
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    # on_change = self._nic_tuple
    # def nic_tuple(self):

    # def update_nic_list(self):
    #     name = self.find_widget("newname")
    #     self.__nic_list.append((name, len(self.__nic_list) + 1))
    #     self.find_widget("list")._frame._layouts[0].update_widgets()

    def _on_close(self, choice):
        if choice == 0:
            self.pop_up.save()
            self.__nic_list = self._model.update_nic_list(self.__nic_list, self.pop_up.data["newname"])
            raise NextScene("Mappings")
        else:
            pass

    def _delete(self):
        pass

    def _cancel(self):
        raise NextScene("Home")
