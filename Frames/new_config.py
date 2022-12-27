from asciimatics.widgets import Layout, Label, Divider, Button, CheckBox, MultiColumnListBox, PopupMenu
from asciimatics.exceptions import NextScene
from interruptframe import InterruptFrame


class NewConfigFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "NewConfig"

    def init_layout(self):
        self._ovs_menu = [
            ("interface", self._model.add_interface),
            ("vlan", self._model.add_vlan),
            ("OVS_bridge", self._model.add_ovs_bridge),
            ("OVS_bond", self._model.add_ovs_bond),
            ("OVS_user_bridge", self._model.add_ovs_user_bridge),
            ("OVS_dpdk_bond", self._model.add_ovs_dpdk_bond),
            ("OVS_dpdk_port", self._model.add_ovs_dpdk_port)
        ]
        self._linux_menu = [
            ("interface", self._model.add_interface),
            ("vlan", self._model.add_vlan),
            ("linux_bridge", self._model.add_linux_bridge),
            ("linux_bond", self._model.add_linux_bond)
        ]

        gap_layout1 = Layout([1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1, 1])
        self.add_layout(layout1)
        self.config_name = Label("")
        layout1.add_widget(self.config_name)
        layout1.add_widget(Button("Raw", self._raw), 1)
        self.ovs_box = CheckBox("OVS", on_change=self._checkbox, name="OVS")
        self.linux_box = CheckBox("Linux", on_change=self._checkbox, name="linux")
        layout1.add_widget(self.ovs_box, 2)
        layout1.add_widget(self.linux_box, 3)
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
        options = [(["Object", "ObjectType1"], 1), (["Object2", "ObjectType2"], 2)]
        self._object_list = MultiColumnListBox(3, [self._screen.width // 2 + 1, self._screen.width // 2 - 1], options, name="objects_list")
        layout3.add_widget(self._object_list)
        self.fix()

    def _on_load(self):
        self.config_name.text = self._model._last_created_config

    def _checkbox(self):
        if self.ovs_box.value == self.linux_box.value:
            self.pop_up_menu_list = [("None", None)]
            self._object_list.disabled = True
        if self.linux_box.value and not self.ovs_box.value:
            self._object_list.disabled = False
            self.pop_up_menu_list = self._linux_menu
        if self.ovs_box.value and not self.linux_box.value:
            self._object_list.disabled = False
            self.pop_up_menu_list = self._ovs_menu

    def _raw(self):
        self.save()
        raise NextScene("Raw")

    def _save_update(self):
        pass

    def _add(self):
        self.pop_up = PopupMenu(self._screen, self.pop_up_menu_list, self._screen.width // 4, self._screen.height // 4)
        self.scene.add_effect(self.pop_up)

    def _delete(self):
        pass

    def _cancel(self):
        self._model.remove_unfinished_config()
        raise NextScene("Home")
