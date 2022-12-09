from asciimatics.widgets import Layout, Button, Divider, ListBox, FileBrowser, PopUpDialog, Text
from asciimatics.exceptions import NextScene
from myframe import MyFrame


class ConfigsFrame(MyFrame):

    @staticmethod
    def get_title():
        return "Configs"

    def init_layout(self):
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1, 1])
        self.add_layout(layout1)
        # layout_browse = Layout([1, 1, 1, 1])
        # self.add_layout(layout_browse)
        # layout_browse.add_widget(FileBrowser(6, "./../../PseudoConfigs/", "Browse"))
        layout1.add_widget(Button("Save", self._save))
        layout1.add_widget(Button("Add", self._add), 1)
        layout1.add_widget(Button("Delete", self._delete), 2)
        layout1.add_widget(Button("Cancel", self._cancel), 3)
        gap_layout2 = Layout([1])
        self.add_layout(gap_layout2)
        gap_layout2.add_widget(Divider(draw_line=False, height=3))
        layout2 = Layout([1, 3], True)
        self.add_layout(layout2)
        configs = [("cfg1", 1), ("cfg2", 2), ("cfg3", 3)]
        layout2.add_widget(ListBox(3, configs))
        descriptions = [("Description1", 1), ("Description2", 2), ("Description3", 3)]
        layout2.add_widget(ListBox(3, descriptions), 1)
        self.fix()

    def _save(self):
        raise NextScene("Home")

    def _add(self):
        pop_up = PopUpDialog(self._screen, "Enter name for new config", ["OK", "Cancel"], on_close=self._on_close)
        # pop_layout = Layout([1])
        # pop_up.add_layout(pop_layout)
        pop_up._layouts[0].add_widget(Text("Here:"))
        pop_up.fix()
        self.scene.add_effect(pop_up)

    @staticmethod
    def _on_close(choice):
        if choice == 0:
            raise NextScene("NewConfig")
        else:
            return

    def _delete(self):
        pass

    def _cancel(self):
        raise NextScene("Home")
