from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, CheckBox, Button, PopUpDialog

from NetworkObjectFrames.network_object_attributes import common_text, common_check, interface
from interruptframe import InterruptFrame


# class InterfaceModel(object):
#     pass


class InterfaceFrame(InterruptFrame):
    @staticmethod
    def get_title():
        return "Interface"

    def _on_load(self):
        for i in common_text:
            self.data[i] = ""
        for i in common_check:
            self.data[i] = False
        for i in interface:
            if i == "hotplug":
                self.data[i] = False
            else:
                self.data[i] = ""

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "interface"
        self.layout1.add_widget(object_type)
        for i in common_check:
            self.layout1.add_widget(CheckBox("", label=i, name=i))
        for i in common_text:
            self.layout1.add_widget(Text(label=i, name=i))
        for i in interface:
            if i == "hotplug":
                self.layout1.add_widget(CheckBox("", label=i, name=i))
            else:
                self.layout1.add_widget(Text(label=i, name=i))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _save_update(self):
        self.save()
        self.pop_up = PopUpDialog(self._screen, "Save " + self.data["name"] + " ?", ["OK", "Cancel"],
                                  on_close=self._on_close)
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    def _on_close(self, choice):
        if choice == 0:
            self._model.handle_object(self.data)
            raise NextScene("NewConfig")
        else:
            pass

    # def _on_load(self):
    #     self.data = None
    def _cancel(self):
        raise NextScene("NewConfig")
