from asciimatics.widgets import Layout, TextBox, Button
from asciimatics.exceptions import NextScene
from interruptframe import InterruptFrame


class RawFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "Raw"

    def init_layout(self):
        layout1 = Layout([1, 1, 1, 1])
        self.add_layout(layout1)
        layout1.add_widget(Button("Done", on_click=self._cancel), 3)
        layout2 = Layout([1], True)
        self.add_layout(layout2)
        self.text_box = TextBox(self._screen.height // 2, readonly=True, name="textbox")
        layout2.add_widget(self.text_box)
        self.fix()

    def _on_load(self):
        if self._model.get_raw_config():
            self.text_box.value = self._model.current_config_raw
        else:
            self.text_box.value = ""

    def _cancel(self):
        self._model.current_config_raw = None
        raise NextScene("NewConfig")
