from asciimatics.widgets import Layout, Button, ListBox, TextBox
from asciimatics.exceptions import NextScene

# from Frames.mappings import MappingsFrame
from frame import InterruptFrame


class HomeFrame(InterruptFrame):

    @staticmethod
    def frame_title():
        return "Home"

    def init_layout(self):
        layout1 = Layout([1, 1, 1, 1, 1, 1, 1, 1], True)
        self.add_layout(layout1)
        self.layout1.add_widget(ListBox())
        layout1.add_widget(Button("Mappings", self._mappings))
        layout1.add_widget(Button("Configs", self._configs))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("DONE", self._final_cancel), 3)
        self.fix()

    def _mappings(self):
        raise NextScene("Mappings")

    def _configs(self):
        raise NextScene("Configs")

    def _save_update(self):
        return

    def _cancel(self):
        return
