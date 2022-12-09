from asciimatics.widgets import Layout, Label, Button, Divider
from asciimatics.exceptions import NextScene
from myframe import MyFrame


class IntroFrame(MyFrame):

    @staticmethod
    def get_title():
        return "Intro"

    def init_layout(self):
        layout0 = Layout([1, 1], True)
        self.add_layout(layout0)
        layout0.add_widget(Label("Let's map physical interfaces"))
        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1])
        self.add_layout(layout1)
        layout1.add_widget(Button("Later", self._cancel))
        layout1.add_widget(Button("Default mappings", self._cancel, 1))
        layout1.add_widget(Button("Mappings", self._mappings), 2)
        self.fix()

    def _mappings(self):
        raise NextScene("Mappings")

    def _cancel(self):
        raise NextScene("Home")
