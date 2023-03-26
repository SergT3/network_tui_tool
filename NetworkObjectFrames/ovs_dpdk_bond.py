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
        self.get_available_members()
        self.pop_up_members = []
        if len(self.available_members):
            self.pop_up_members = []
            for i in self.available_members:
                if i["type"] == "ovs_dpdk_port":
                    self.pop_up_members.append((i["name"], i))
            if len(self.member_list):
                for i in self.pop_up_members:
                    if i[1] in self.member_list:
                        self.pop_up_members.remove(i)
        else:
            self.pop_up_members = [("None", None)]

        self.fill_common_attr()
        self.fill_ovs_common_attr()
        if self._model.current_network_object == {}:
            for i in ovs_dpdk_bond:
                if i == "members":
                    self.widget_dict[i].options = [(["None"], None)]
        else:
            if "members" in self._model.current_network_object:
                self.member_list = self._model.current_network_object["members"]

            for i in ovs_dpdk_bond:
                if i == "members":
                    if "members" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        if self.member_list is not None and len(self.member_list):
                            for j in self.member_list:
                                self.widget_dict[i].options.append(([j["name"], j["type"]], j))
                                self.widget_dict[i]._required_height = len(self.member_list)
                    else:
                        self.widget_dict[i]._required_height = 1
                        self.widget_dict[i].options = [(["None"], None)]
        self.fix()

    def _on_close(self, choice):
        for i in self.member_list:
            if i["type"] != "ovs_dpdk_port":
                self.member_list.remove(i)
        super()._on_close(choice)

    def get_available_members(self):
        if len(self._model.ovs_current_config_objects):
            for net_object in self._model.ovs_current_config_objects:
                if net_object["type"] == "ovs_dpdk_port" \
                        and net_object not in self.member_list \
                        and net_object not in self._model.ovs_current_config_members:
                    self.available_members.append(net_object)

    def _member_on_close(self, choice):
        if choice == 0:
            self.widget_dict["MemberPopUp"].save()
            if self.widget_dict["drop_member"].value is None:
                return
            self.pop_up_members.remove((self.widget_dict["drop_member"].value["name"], self.widget_dict["drop_member"].value))
            self.member_list.append(self.widget_dict["drop_member"].value)
            self._model.ovs_current_config_objects.remove(self.widget_dict["drop_member"].value)
            self._model.ovs_current_config_members.append(self.widget_dict["drop_member"].value)
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
                self._model.ovs_current_config_members.remove(self.selected_member)
                self._model.ovs_current_config_objects.append(self.selected_member)
                self.widget_dict["members"]._required_height -= 1
            if not len(self.member_list):
                self.widget_dict["members"]._required_height = 1
                self.widget_dict["members"].options = [(["None"], None)]
            self.selected_member = None
            self.fix()
