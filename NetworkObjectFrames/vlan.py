from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button

from NetworkObjectFrames.network_object_attributes import vlan
from interruptframe import InterruptFrame


class VlanModel(object):
    pass


class VlanFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "Vlan"

    def init_layout(self):
        layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(layout1)
        for i in vlan:
            layout1.add_widget(Text(label=i, name=i))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Cancel", self._cancel))
        self.fix()

    def _cancel(self):
        raise NextScene("NewConfig")
