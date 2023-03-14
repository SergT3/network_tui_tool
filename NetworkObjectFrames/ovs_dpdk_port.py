from asciimatics.widgets import Layout, Text, Button

from NetworkObjectFrames.network_object_attributes import ovs_dpdk_port
from NetworkObjectFrames.ovs_dpdk_bond import OVSDpdkBondFrame


class OVSDpdkPortFrame(OVSDpdkBondFrame):

    @staticmethod
    def get_title():
        return "OVSDpdkPort"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "ovs_dpdk_port"
        self.layout1.add_widget(object_type)
        self.add_common_attr()
        self.add_ovs_common_attr()
        for i in ovs_dpdk_port:
            if i != "members":
                self.widget_dict[i] = Text(label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Cancel", self._cancel))
        self.fix()

    def _on_load(self):
        super()._on_load()
        if self._model.current_network_object == {}:
            self.widget_dict["driver"].value = ""
        else:
            if "driver" in self._model.current_network_object:
                self.widget_dict["driver"] = self._model.current_network_object["driver"]
            else:
                self.widget_dict["device"].value = ""

    def get_available_members(self):
        if len(self._model.current_config_object_list):
            for net_object in self._model.current_config_object_list:
                if net_object["type"] == "interface":
                    if net_object["name"] not in self.member_list:
                        self.available_members.append(
                            {"type": "interface", "name": net_object["name"]})
