from copy import deepcopy

from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, MultiColumnListBox, PopUpDialog, DropdownList

from NetworkObjectFrames.network_object_attributes import vlan_text, vlan_list, route_titles
from interruptframe import InterruptFrame


class VlanFrame(InterruptFrame):
    opt_data = None
    address_list = []
    route_list = []
    selected_address = None
    selected_route = None
    available_devices = []
    pop_up_devices = []

    @staticmethod
    def get_title():
        return "Vlan"

    def init_layout(self):
        self.layout1 = Layout([1, 1, 1, 1], True)
        self.add_layout(self.layout1)
        self.widget_dict = {}
        object_type = Text(label="type", name="type", readonly=True)
        object_type.value = "vlan"
        self.layout1.add_widget(object_type)
        for i in vlan_text:
            self.widget_dict[i] = Text(label=i, name=i)
            self.layout1.add_widget(self.widget_dict[i])
        for i in vlan_list:
            if i == "addresses":
                self.layout1.add_widget(Button("Add address", self._add_address))
                self.layout1.add_widget(Button("Delete address", self._delete_address))
                self.widget_dict[i] = MultiColumnListBox(1, [self._screen.width // 3 + 1, self._screen.width // 3 - 1],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_address)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "routes":
                self.layout1.add_widget(Button("Add route", self._add_route))
                self.layout1.add_widget(Button("Delete route", self._delete_route))
                self.widget_dict[i] = MultiColumnListBox(1,
                                                         [self._screen.width // 5 + 1, self._screen.width // 5 + 1,
                                                          self._screen.width // 5 + 1, self._screen.width // 5 + 1,
                                                          self._screen.width // 5 - 4],
                                                         [(["None"], None)],
                                                         add_scroll_bar=True, label=i, name=i,
                                                         on_select=self._show_route)
                self.layout1.add_widget(self.widget_dict[i])
            elif i == "device":
                self.widget_dict[i] = DropdownList([("None", None)], label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._save_update))
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def _on_load(self):
        self.get_available_devices()

        if self._model.current_network_object == {}:
            for i in vlan_text:
                self.widget_dict[i].value = ""
            for i in vlan_list:
                if i != "device":
                    self.widget_dict[i].options = [(["None"], None)]
        else:
            if "addresses" in self._model.current_network_object:
                self.address_list = self._model.current_network_object["addresses"]
            if "routes" in self._model.current_network_object:
                self.route_list = self._model.current_network_object["routes"]
            for i in vlan_text:
                self.data[i] = self._model.current_network_object[i]
                self.widget_dict[i].value = self._model.current_network_object[i]
            for i in vlan_list:
                if i == "addresses":
                    self.widget_dict[i].options = []
                    if "addresses" in self._model.current_network_object:
                        temp = []
                        for j in self.address_list:
                            temp.append((["ip_netmask:", j["ip_netmask"]],
                                         {"ip_netmask": j["ip_netmask"]}))
                        self.widget_dict[i].options = temp
                        # self.widget_dict[i]._required_height = len(self.address_list)
                elif i == "routes":
                    self.widget_dict[i].options = []
                    if "routes" in self._model.current_network_object:
                        for j in self.route_list:
                            temp_route_list = []
                            for k in j:
                                temp_route_list.append(j[k])
                            self.widget_dict[i].options.append((temp_route_list, temp_route_list))
                        # self.widget_dict[i]._required_height = len(self.route_list)
                elif i == "device":
                    if "device" in self._model.current_network_object:
                        self.data[i] = self._model.current_network_object[i]
                        self.widget_dict[i].value = self._model.current_network_object[i]


    def _on_close(self, choice):
        if choice == 0:
            self.opt_data = deepcopy(self.data)
            self.opt_data["addresses"] = self.address_list
            self.opt_data["routes"] = self.route_list
            self._model.handle_object(self.opt_data)
            self._model.current_network_object = {}
            raise NextScene("NewConfig")
        else:
            pass

    def _save_update(self):
        self.save()
        # write_to_file("data_value_old", self.data)
        self.pop_up = PopUpDialog(self._screen, "Save this vlan?", ["OK", "Cancel"],
                                  on_close=self._on_close)
        self.pop_up.fix()
        self.scene.add_effect(self.pop_up)

    def _cancel(self):
        self._model.current_network_object = {}
        raise NextScene("NewConfig")

    def _add_address(self):
        self.widget_dict["AddressPopUp"] = PopUpDialog(self._screen, "Enter new address",
                                                       ["OK", "Cancel"], on_close=self._address_on_close)
        self.widget_dict["AddressPopUp"]._layouts[0].add_widget(Text("Here:", validator=self._model.name_validator,
                                                                     name="text"))
        self.widget_dict["AddressPopUp"].fix()
        self.scene.add_effect(self.widget_dict["AddressPopUp"])

    def _address_on_close(self, choice):
        if choice == 0:
            self.widget_dict["AddressPopUp"].save()
            self.address_list.append({"ip_netmask": self.widget_dict["AddressPopUp"].data["text"]})
            if len(self.address_list) != 0:
                if self.widget_dict["addresses"].options == [(["None"], None)]:
                    self.widget_dict["addresses"].options = []
                self.widget_dict["addresses"].options.append((["ip_netmask:", self.widget_dict["AddressPopUp"].data["text"]],
                                                              {"ip_netmask": self.widget_dict["AddressPopUp"].data[
                                                                  "text"]}))
                self.widget_dict["addresses"]._required_height = len(self.address_list)
            self.fix()

    def _show_address(self):
        self.selected_address = self.widget_dict["addresses"].value
    def _delete_address(self):
        if self.selected_address is not None:
            while (["ip_netmask:", self.selected_address["ip_netmask"]], self.selected_address) in self.widget_dict["addresses"].options:
                self.widget_dict["addresses"].options.remove((["ip_netmask:", self.selected_address["ip_netmask"]], self.selected_address))
                self.address_list.remove(self.selected_address)
                self.widget_dict["addresses"]._required_height -= 1
            if len(self.address_list) == 0:
                self.widget_dict["addresses"]._required_height = 1
                self.widget_dict["addresses"].options = [(["None"], None)]
            self.selected_address = None
            self.fix()

    def _add_route(self):
        self.widget_dict["RoutePopUp"] = PopUpDialog(self._screen, "Enter new route",
                                                     ["OK", "Cancel"], on_close=self._route_on_close)
        for i in route_titles:
            # if i == default:
            # self.widget_dict["RoutePopUp"]._layouts[0].add_widget(CheckBox("", label=i, name=i))
            # error: object of type bool has no len
            self.widget_dict["RoutePopUp"]._layouts[0].add_widget(Text(i + ":", validator=self._model.name_validator, name=i))
        self.widget_dict["RoutePopUp"].fix()
        self.scene.add_effect(self.widget_dict["RoutePopUp"])

    def _route_on_close(self, choice):
        if choice == 0:
            self.widget_dict["RoutePopUp"].save()
            temp_route_dict = {}
            temp_route_list = []
            for i in route_titles:
                if self.widget_dict["RoutePopUp"].data[i] != "":
                    temp_route_dict[i] = self.widget_dict["RoutePopUp"].data[i]
            for i in temp_route_dict:
                temp_route_list.append(temp_route_dict[i])
            if self.widget_dict["routes"].options == [(["None"], None)]:
                self.widget_dict["routes"].options = []
            self.widget_dict["routes"].options.append((tuple(temp_route_list), tuple(temp_route_list)))
            self.route_list.append(temp_route_dict)
            self.widget_dict["routes"]._required_height = len(self.route_list)
            self.fix()

    def _show_route(self):
        self.selected_route = self.widget_dict["routes"].value

    def _delete_route(self):
        if self.selected_route is not None:
            temp_route_dict = {}
            j = 0
            for i in route_titles:
                temp_route_dict[i] = self.selected_route[j]
                j += 1
            while (self.selected_route, self.selected_route) in self.widget_dict["routes"].options:
                self.widget_dict["routes"].options.remove((self.selected_route, self.selected_route))
                self.route_list.remove(temp_route_dict)
                self.widget_dict["routes"]._required_height -= 1
            if len(self.route_list) == 0:
                self.widget_dict["routes"]._required_height = 1
                self.widget_dict["routes"].options = [(["None"], None)]
            self.selected_route = None
            self.fix()

    def get_available_devices(self):
        self.available_devices = [("None", None)]
        if len(self._model.current_config_object_list) != 0:
            for net_object in self._model.current_config_object_list:
                if net_object["type"] == "interface" or net_object["type"] == "ovs_bond" or net_object["type"] == "linux_bond":
                    self.available_devices.append((net_object["name"], net_object["name"]))
        self.widget_dict["device"].options = self.available_devices
                # if net_object["type"] == "vlan":
                #     self.available_devices.append({"type": "vlan", "device": net_object["device"],
                #                                    "mtu": net_object["mtu"], "vlan_id": net_object["vlan_id"]})
        self.fix()

# config = (read_dict_from_yaml("Configs/" + self._model.current_config + ".yaml"))["network_config"]
#         for i in config:
#             if config[i]["type"] == "interface":
#                 self.available_devices.append(config[i]["name"])
#             elif config[i]["type"] == "ovs_bond":
#                 self.available_devices.append(config[i]["name"])
#             elif config[i]["type"] == "linux_bond":
#                 self.available_devices.append(config[i]["name"])