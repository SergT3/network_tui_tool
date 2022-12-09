from asciimatics.widgets import Layout, Divider, ListBox, DropdownList, Button, PopUpDialog, Text
from asciimatics.exceptions import NextScene
from myframe import MyFrame
from utils import get_interfaces, to_asciimatics_list, obj_list_util



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
        self.__nic_list = obj_list_util("nic", len(self.__hardware_objects))
        layout2.add_widget(ListBox(len(self.__hardware_objects), self.__hardware_objects, name="list"))
        for i in range(len(self.__hardware_objects)):
            layout2.add_widget(DropdownList(self.__nic_list), 1)
        layout3 = Layout([1, 1, 1, 1])
        self.add_layout(layout3)
        layout3.add_widget(Button("Save", self._save))
        layout3.add_widget(Button("Add", self._add), 1)
        layout3.add_widget(Button("Delete", self._delete), 2)
        layout3.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _save(self):
        raise NextScene("Home")

    def _add(self):
        pop_up = PopUpDialog(self._screen, "New interface name:", ["OK", "Cancel"],
                             on_close=self._on_close)
        pop_up._layouts[0].add_widget(Text(name="newname"))
        pop_up.fix()
        self.scene.add_effect(pop_up)

    # on_change = self._nic_tuple
    # def nic_tuple(self):

    # def update_nic_list(self):
    #     name = self.find_widget("newname")
    #     self.__nic_list.append((name, len(self.__nic_list) + 1))
    #     self.find_widget("list")._frame._layouts[0].update_widgets()

    def _on_close(self, choice):
        if choice == 0:
            # self.update_nic_list()
            raise NextScene("Mappings")
        else:
            pass

    def _delete(self):
        pass

    def _cancel(self):
        raise NextScene("Home")
