from asciimatics.widgets import Layout, Text, Button, MultiColumnListBox

from NetworkObjectFrames.network_object_attributes import ovs_dpdk_bond
from NetworkObjectFrames.ovs_bond import OVSBondFrame


class OVSDpdkBondFrame(OVSBondFrame):

    ovs_extra_list = []
    selected_option = []
    member_list = []

    @staticmethod
    def get_title():
        return "OVSDpdkBond"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "ovs_dpdk_bond"
        self.layout1.add_widget(object_type)
        self.add_common_attr()
        self.add_ovs_common_attr()
        for i in ovs_dpdk_bond:
            if i == "members":
                self.layout1.add_widget(Button("Add member", self._add_member))
                self.layout1.add_widget(Button("Delete member", self._delete_member))
                self.widget_dict[i] = MultiColumnListBox(1,
                                                         [self._screen.width // 3 + 1, self._screen.width // 3 + 1,
                                                          self._screen.width // 3 - 3],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_member)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "rx_queue":
                self.widget_dict[i] = Text(label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        super()._on_load()
        if self._model.current_network_object == {}:
            self.widget_dict["rx_queue"].value = ""
        else:
            if "rx_queue" in self._model.current_network_object:
                self.widget_dict["rx_queue"] = self._model.current_network_object["rx_queue"]
            else:
                self.widget_dict["rx_queue"].value = ""

    def get_available_members(self):
        if len(self._model.current_config_object_list):
            for net_object in self._model.current_config_object_list:
                if net_object["type"] == "ovs_dpdk_port":
                    if net_object["name"] not in self.member_list:
                        self.available_members.append(
                            {"type": "ovs_dpdk_port", "name": net_object["name"],
                             "mtu": net_object["mtu"], "members": net_object["members"]})
