from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, CheckBox

from NetworkObjectFrames.network_object_attributes import ovs_bond, common_check, common_text, common_list, ovs_common
from interruptframe import InterruptFrame


class OVSBondModel(object):
    pass


class OVSBondFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "OVSBond"

    def init_layout(self):
        layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(layout1)
        for i in common_text + ovs_common:
            layout1.add_widget(Text(label=i, name=i))
        for i in common_check:
            layout1.add_widget(CheckBox("", label=i, name=i))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Cancel", self._cancel))
        self.fix()

    def _cancel(self):
        raise NextScene("NewConfig")

    # def _checkbox(self):
    #     if self.data["use_dhcp"] == self.data["use_dhcp6"]:
    #
    #         self._object_list.disabled = True
    #     if self.linux_box.value and not self.ovs_box.value:
    #         self._object_list.disabled = False
    #         self.pop_up_menu_list = self._linux_menu
    #     if self.ovs_box.value and not self.linux_box.value:
    #         self._object_list.disabled = False
    #         self.pop_up_menu_list = self._ovs_menu
