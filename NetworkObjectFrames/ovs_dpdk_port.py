from asciimatics.widgets import Layout, Text, Button, MultiColumnListBox

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
            if i == "members":
                self.layout1.add_widget(Button("Add member", self._add_member))
                self.layout1.add_widget(Button("Delete member", self._delete_member))
                self.widget_dict[i] = MultiColumnListBox(1,
                                                         [self._screen.width // 2 + 1, self._screen.width // 2 - 1],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_member)
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
        self.get_available_members()
        if len(self.available_members):
            for i in self.available_members:
                self.pop_up_members.append((i["name"], {"type": "interface", "name": i["name"]}))
            if len(self.member_list):
                self.pop_up_members = []
                for i in self.pop_up_members:
                    for j in self.member_list:
                        if i[1]["type"] == j["type"] and i[1]["name"] == j["name"]:
                            self.pop_up_members.remove(i)
        else:
            self.pop_up_members = [("None", None)]

        self.fill_common_attr()
        self.fill_ovs_common_attr()
        if self._model.current_network_object == {}:
            for i in ovs_dpdk_port:
                if i == "members":
                    self.widget_dict[i].options = [(["None"], None)]
                else:
                    if i in self.widget_dict:
                        self.widget_dict[i].value = ""
        else:
            if "members" in self._model.current_network_object:
                self.member_list = self._model.current_network_object["members"]

            for i in ovs_dpdk_port:
                if i == "members":
                    if "members" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        if self.member_list is not None and len(self.member_list):
                            for j in self.member_list:
                                self.widget_dict[i].options.append(([j["type"], j["name"]], j))
                                self.widget_dict[i]._required_height = len(self.member_list)
                    else:
                        self.widget_dict[i]._required_height = 1
                        self.widget_dict[i].options = [(["None"], None)]
                else:
                    if i in self._model.current_network_object:
                        self.data[i] = self._model.current_network_object[i]
                        self.widget_dict[i].value = self._model.current_network_object[i]
                    else:
                        self.widget_dict[i].value = ""
        self.fix()

    def get_available_members(self):
        if len(self._model.current_config_object_list):
            for net_object in self._model.current_config_object_list:
                if net_object["type"] == "interface":
                    if net_object["name"] not in self.member_list:
                        self.available_members.append(
                            {"type": "interface", "name": net_object["name"]})

    def _member_on_close(self, choice):
        if choice == 0:
            self.widget_dict["MemberPopUp"].save()
            if self.widget_dict["drop_member"].value is None:
                return
            self.pop_up_members.remove(
                (self.widget_dict["drop_member"].value["name"], self.widget_dict["drop_member"].value))
            self.member_list.append(self.widget_dict["drop_member"].value)
            if len(self.member_list) == 1:
                self.widget_dict["members"].options = []
            self.widget_dict["members"].options.append(([self.widget_dict["drop_member"].value["name"],
                                                         self.widget_dict["drop_member"].value["type"]],
                                                        self.widget_dict["drop_member"].value))
            self.widget_dict["members"]._required_height = len(self.member_list)
            self.fix()

    def _delete_member(self):
        if self.selected_member is not None:
            self.available_members.append(self.selected_member)
            self.pop_up_members.append(
                (self.selected_member["name"], self.selected_member))
            member_temp = ([self.selected_member["name"], self.selected_member["type"]],
                           self.selected_member)
            while member_temp in self.widget_dict["members"].options:
                self.widget_dict["members"].options.remove(member_temp)
                self.member_list.remove(self.selected_member)
                self.widget_dict["members"]._required_height -= 1
            if not len(self.member_list):
                self.widget_dict["members"]._required_height = 1
                self.widget_dict["members"].options = [(["None"], None)]
            self.selected_member = None
            self.fix()
