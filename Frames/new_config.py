from asciimatics.widgets import Layout, Label, Divider, Button, CheckBox, MultiColumnListBox
from asciimatics.exceptions import NextScene
from myframe import MyFrame


class NewConfigFrame(MyFrame):

    @staticmethod
    def get_title():
        return "NewConfig"

    def init_layout(self):
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1, 1])
        self.add_layout(layout1)
        self.config_name = Label("")
        layout1.add_widget(self.config_name)
        layout1.add_widget(Button("Raw", self._raw), 1)
        layout1.add_widget(CheckBox("OVS", name="OVS"), 2)
        layout1.add_widget(CheckBox("Linux", name="linux"), 3)
        gap_layout2 = Layout([1])
        self.add_layout(gap_layout2)
        gap_layout2.add_widget(Divider(draw_line=False, height=3))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Add", self._add), 1)
        layout2.add_widget(Button("Delete", self._delete), 2)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        gap_layout3 = Layout([1])
        self.add_layout(gap_layout3)
        gap_layout3.add_widget(Divider(draw_line=False, height=3))
        layout3 = Layout([1], True)
        self.add_layout(layout3)
        options = [(["Object", "Hardware"], 1), (["     SubObject", ""], 2), (["Object2", "Hardware2"], 3)]
        layout3.add_widget(MultiColumnListBox(3, [self._screen.width // 2 + 1, self._screen.width // 2 - 1], options))
        self.fix()

    def _on_load(self):
        self.config_name.text = self._model._last_created_config

    def _raw(self):
        self.save()
        raise NextScene("Raw")

    def _save_update(self):
        pass

    def _add(self):
        pass

    def _delete(self):
        pass

    def _cancel(self):
        self._model.remove_unfinished_config()
        raise NextScene("Home")
