from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, MultiColumnListBox, PopUpDialog, DropdownList

from NetworkObjectFrames.interface import InterfaceFrame
from NetworkObjectFrames.network_object_attributes import linux_bridge
from utils import remove_empty_keys


class LinuxBridgeFrame(InterfaceFrame):

    member_list = []
    selected_member = None
    available_members = []
    pop_up_members = []

    @staticmethod
    def get_title():
        return "LinuxBridge"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "linux_bridge"
        self.layout1.add_widget(object_type)
        self.add_common_attr()
        for i in linux_bridge:
            if i == "members":
                self.layout1.add_widget(Button("Add member", self._add_member))
                self.layout1.add_widget(Button("Delete member", self._delete_member))
                self.widget_dict[i] = MultiColumnListBox(1, [self._screen.width // 3 + 1, self._screen.width // 3 + 1,
                                                             self._screen.width // 3 - 3],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_member)
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
            for i in self.available_members:
                if i["type"] == "vlan":
                    self.pop_up_members.append((i["vlan_id"], i))
                else:
                    self.pop_up_members.append((i["name"], i))
            if len(self.member_list):
                for i in self.pop_up_members:
                    if i[1] in self.member_list:
                        self.pop_up_members.remove(i)
        else:
            self.pop_up_members = [("None", None)]

        self.fill_common_attr()
        if self._model.current_network_object == {}:
            for i in linux_bridge:
                if i == "members":
                    self.widget_dict[i].options = [(["None"], None)]
        else:
            if "members" in self._model.current_network_object:
                self.member_list = self._model.current_network_object["members"]

            for i in linux_bridge:
                if i == "members":
                    if "members" in self._model.current_network_object:
                        self.widget_dict[i].options = []
                        if self.member_list is not None and len(self.member_list):
                            for j in self.member_list:
                                if j["type"] == "vlan":
                                    self.widget_dict[i].options.append(([j["vlan_id"], j["type"], j["mtu"]], j))
                                else:
                                    self.widget_dict[i].options.append(([j["name"], j["type"], j["mtu"]], j))
                            self.widget_dict[i]._required_height = len(self.member_list)
                        else:
                            self.widget_dict[i]._required_height = 1
                            self.widget_dict[i].options = [(["None"], None)]
                        # self.widget_dict[i]._required_height = len(self.rule_list)
        self.fix()

    def _on_close(self, choice):
        if choice == 0:
            self.opt_data = deepcopy(self.data)
            self.opt_data["addresses"] = deepcopy(self.address_list)
            self.opt_data["dns_servers"] = deepcopy(self.dns_list)
            self.opt_data["domain"] = deepcopy(self.domain_list)
            self.opt_data["routes"] = deepcopy(self.route_list)
            self.opt_data["rules"] = deepcopy(self.rule_list)
            self.opt_data["members"] = deepcopy(self.member_list)
            self.opt_data = remove_empty_keys(self.opt_data)
            if self._model.edit_mode:
                if self._model.current_network_object in self._model.current_config_objects:
                    self._model.current_config_objects.remove(self._model.current_network_object)
                elif self._model.current_network_object in self._model.current_config_members:
                    self._model.current_config_members.remove(self._model.current_network_object)
            self._model.edit_mode = False
            self._model.handle_object(self.opt_data)
            self._model.write_config_members()
            self._model.current_network_object = {}
            raise NextScene("NewConfig")

    def get_available_members(self):
        if len(self._model.current_config_objects):
            for net_object in self._model.current_config_objects:
                if net_object["type"] in ["interface", "bridge", "vlan"] \
                        and net_object not in self.member_list\
                        and net_object not in self._model.current_config_members:
                    self.available_members.append(net_object)

    def _add_member(self):
        self.widget_dict["MemberPopUp"] = PopUpDialog(self._screen, "Select new member:",
                                                    ["OK", "Cancel"], on_close=self._member_on_close)
        self.widget_dict["drop_member"] = DropdownList(self.pop_up_members, label="Available members")
        self.widget_dict["MemberPopUp"]._layouts[0].add_widget(self.widget_dict["drop_member"])
        self.widget_dict["MemberPopUp"].fix()
        self.scene.add_effect(self.widget_dict["MemberPopUp"])

    def _member_on_close(self, choice):
        if choice == 0:
            self.widget_dict["MemberPopUp"].save()
            if self.widget_dict["drop_member"].value is None:
                return
            if self.widget_dict["drop_member"].value["type"] == "vlan":
                self.pop_up_members.remove((self.widget_dict["drop_member"].value["vlan_id"],
                                            self.widget_dict["drop_member"].value))
            else:
                self.pop_up_members.remove((self.widget_dict["drop_member"].value["name"],
                                            self.widget_dict["drop_member"].value))
            self.member_list.append(self.widget_dict["drop_member"].value)
            self._model.current_config_objects.remove(self.widget_dict["drop_member"].value)
            self._model.current_config_members.append(self.widget_dict["drop_member"].value)
            if len(self.member_list) == 1:
                self.widget_dict["members"].options = []
            if self.widget_dict["drop_member"].value["type"] == "vlan":
                self.widget_dict["members"].options.append(([self.widget_dict["drop_member"].value["vlan_id"],
                                                             self.widget_dict["drop_member"].value["type"],
                                                             self.widget_dict["drop_member"].value["mtu"]],
                                                            self.widget_dict["drop_member"].value))
            else:
                self.widget_dict["members"].options.append(([self.widget_dict["drop_member"].value["name"],
                                                             self.widget_dict["drop_member"].value["type"],
                                                             self.widget_dict["drop_member"].value["mtu"]],
                                                            self.widget_dict["drop_member"].value))
            self.widget_dict["members"]._required_height = len(self.member_list)
            self.fix()


    def _show_member(self):
        self.selected_member = self.widget_dict["members"].value

    def _delete_member(self):
        if self.selected_member is not None:
            self.available_members.append(self.selected_member)
            if self.selected_member["type"] == "vlan":
                self.pop_up_members.append((self.selected_member["vlan_id"], self.selected_member))
                member_temp = ([self.selected_member["vlan_id"], self.selected_member["type"],
                                self.selected_member["mtu"]], self.selected_member)
            else:
                self.pop_up_members.append((self.selected_member["name"], self.selected_member))
                member_temp = ([self.selected_member["name"], self.selected_member["type"],
                                self.selected_member["mtu"]], self.selected_member)
            while member_temp in self.widget_dict["members"].options:
                self.widget_dict["members"].options.remove(member_temp)
                self.member_list.remove(self.selected_member)
                self._model.current_config_members.remove(self.selected_member)
                self._model.current_config_objects.append(self.selected_member)
                self.widget_dict["members"]._required_height -= 1
            if not len(self.member_list):
                self.widget_dict["members"]._required_height = 1
                self.widget_dict["members"].options = [(["None"], None)]
            self.selected_member = None
            self.fix()