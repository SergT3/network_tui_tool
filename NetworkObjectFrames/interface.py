from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, CheckBox, Button

from NetworkObjectFrames.network_object_attributes import common_text, common_check, interface
from interruptframe import InterruptFrame


class InterfaceModel(object):
    pass


class InterfaceFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "Interface"

    def init_layout(self):
        layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(layout1)
        for i in common_check:
            layout1.add_widget(CheckBox("", label=i, name=i))
        for i in common_text:
            layout1.add_widget(Text(label=i))
        for i in interface:
            if i == "hotplug":
                layout1.add_widget(CheckBox("", label=i, name=i))
            else:
                layout1.add_widget(Text(label=i))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Cancel", self._cancel))
        self.fix()

    def _cancel(self):
        raise NextScene("NewConfig")
