from asciimatics.widgets import Layout, Button, ListBox, Label, TextBox, Widget
from asciimatics.exceptions import NextScene

# from Frames.mappings import MappingsFrame
from frame import InterruptFrame


class HomeFrame(InterruptFrame):

    @staticmethod
    def frame_title():
        return "Home"

    def init_layout(self):
        layout1 = Layout([2, 1], True)
        self.add_layout(layout1)
        layout1.add_widget(Label("Menu"))
        layout1.add_widget(Label('Description'), 1)
        layout1.add_widget(ListBox(2, [("Mappings", "Mappings"), ("Configs", "Configs")],
                                   on_change=self._change, on_select=self._select,
                                   name="menu"))
        self.description = TextBox(Widget.FILL_COLUMN, as_string=True, readonly=True, line_wrap=True,
                                   tab_stop=False)
        self.description.value = next(iter(self.menu.values()))
        self.description.readonly = True
        layout1.add_widget(self.description, 1)
        # layout1.add_widget(Button("Mappings", self._mappings))
        # layout1.add_widget(Button("Configs", self._configs))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("DONE", self._final_cancel), 3)
        self.fix()

    def _change(self):
        self.save()
        selected_option = self.data.get("menu", None)
        if selected_option:
            self.description.value = self.menu[selected_option]
        self.fix()

    def _delete(self):
        pass

    def _select(self):
        self.save()
        raise NextScene(self.data["menu"])

    def _add(self):
        pass

    # def _mappings(self):
    #     raise NextScene("Mappings")
    #
    # def _configs(self):
    #     raise NextScene("Configs")

    def _save_update(self):
        return

    def _cancel(self):
        return

    menu = {
        "Mappings": "Map physical interfaces to nics",
        "Configs": "Manage custom plans"
    }
