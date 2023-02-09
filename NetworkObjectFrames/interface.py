from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, CheckBox, Button, PopUpDialog, ListBox

from NetworkObjectFrames.network_object_attributes import common_text, common_check, common_list, interface
from interruptframe import InterruptFrame
from utils import write_to_file

import logging
# class InterfaceModel(object):
#     pass


class InterfaceFrame(InterruptFrame):
    @staticmethod
    def get_title():
        return "Interface"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "interface"
        self.layout1.add_widget(object_type)
        for i in common_check:
            self.widget_dict[i] = CheckBox("", label=i, name=i)
            self.layout1.add_widget(self.widget_dict[i])
        for i in common_text:
            self.widget_dict[i] = Text(label=i, name=i)
            self.layout1.add_widget(self.widget_dict[i])
        # for i in common_list:
        #     if i == "addresses":
        #         self.layout1.add_widget(Button("Add Address", self._address))
        #         self.widget_dict[i] = ListBox(0, label=i, name=i)
        #         self.layout1.add_widget(self.widget_dict[i])
        #     else:
        #         break
        for i in interface:
            if i == "hotplug":
                self.widget_dict[i] = CheckBox("", label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
            else:
                self.widget_dict[i] = Text(label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        for i in common_text:
            self.widget_dict[i].value = ""
        for i in common_check:
            self.widget_dict[i].value = False
        for i in interface:
            if i == "hotplug":
                self.widget_dict[i].value = False
            else:
                self.widget_dict[i].value = ""

    def _save_update(self):
        self.save()
        write_to_file("data_value_old", self.data)
        self.pop_up = PopUpDialog(self._screen, "Save " + self.data["name"] + " ?", ["OK", "Cancel"],
                                  on_close=self._on_close)
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    # def _address(self):
    #     self.widget_dict["addresses"].

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
