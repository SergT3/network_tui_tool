from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, CheckBox

from NetworkObjectFrames.network_object_attributes import ovs_user_bridge, common_check, common_text, common_list, ovs_common
from interruptframe import InterruptFrame


class OVSUserBridgeModel(object):
    pass


class OVSUserBridgeFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "OVSUserBridge"

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