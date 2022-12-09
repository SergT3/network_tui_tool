from asciimatics.widgets import Layout, Label, Button
from asciimatics.exceptions import NextScene

# from Frames.mappings import MappingsFrame
from myframe import MyFrame


class HomeFrame(MyFrame):

    @staticmethod
    def get_title():
        return "Home"

    def init_layout(self):
        layout1 = Layout([1, 1, 1, 1, 1, 1, 1, 1], True)
        self.add_layout(layout1)
        layout1.add_widget(Label("Home:"))
        layout1.add_widget(Button("Mappings", self._mappings))
        layout1.add_widget(Button("Configs", self._configs))
        layout1.add_widget(Button("Devices", self._devices))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("DONE", self._final_cancel), 3)
        self.fix()

    def _mappings(self):
        raise NextScene("Mappings")

    def _configs(self):
        raise NextScene("Configs")

    def _devices(self):
        raise NextScene("Devices")

    def _save(self):
        return

    def _cancel(self):
        return
