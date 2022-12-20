from asciimatics.widgets import Layout, Divider, ListBox, Button, TextBox
from asciimatics.exceptions import NextScene
from interruptframe import InterruptFrame
from utils import get_interfaces, to_asciimatics_list


class DevicesFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "Devices"

    def init_layout(self):
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1])
        self.add_layout(layout1)
        hardware_objects = to_asciimatics_list(get_interfaces())
        layout1.add_widget(ListBox(len(hardware_objects), hardware_objects))
        layout1.add_widget(Button("Done", self._save_update), 2)
        # layout1.add_widget(Button("Mappings",screen.refresh()),2)
        self.fix()

    def _save_update(self):
        raise NextScene("Home")

    def _cancel(self):
        raise NextScene("Home")
