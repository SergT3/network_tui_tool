from asciimatics.exceptions import NextScene
from asciimatics.widgets import Layout, Text, Button, MultiColumnListBox, PopUpDialog, DropdownList
from utils import read_dict_from_yaml
from NetworkObjectFrames.network_object_attributes import vlan, route_titles
from interruptframe import InterruptFrame


class VlanFrame(InterruptFrame):
    opt_data = None
    address_list = []
    route_list = []
    selected_address = None
    selected_route = None
    available_devices = []

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
        for i in vlan:
            if i == "vlan_id" or i == "mtu":
                self.layout1.add_widget(Text(label=i, name=i))
            elif i == "addresses":
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
                self.widget_dict[i] = DropdownList(self.available_devices, on_change=self._on_change, label=i, name=i)
                self.layout1.add_widget(self.widget_dict[i])
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Cancel", self._cancel))
        self.fix()

    def _cancel(self):
        raise NextScene("NewConfig")

    def _on_change(self):
        pass

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
                self.widget_dict["addresses"].options.append(([self.widget_dict["AddressPopUp"].data["text"]],
                                                              {"ip_netmask": self.widget_dict["AddressPopUp"].data[
                                                                  "text"]}))
                self.address_list.append({"ip_netmask": self.widget_dict["AddressPopUp"].data["text"]})
                self.widget_dict["addresses"]._required_height += 1
            self.fix()

    def _show_address(self):
        self.selected_address = self.widget_dict["addresses"].value

    def _delete_address(self):
        if self.selected_address is not None:
            while ([self.selected_address["ip_netmask"]], self.selected_address) in self.widget_dict[
                "addresses"].options:
                self.widget_dict["addresses"].options.remove(
                    ([self.selected_address["ip_netmask"]], self.selected_address))
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
            self.widget_dict["RoutePopUp"]._layouts[0].add_widget(
                Text(i + ":", validator=self._model.name_validator, name=i))
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
        config = (read_dict_from_yaml("Configs/" + self._model.current_config + ".yaml"))["network_config"]
        for i in config:
            if config[i]["type"] == "interface":
                self.available_devices.append(config[i]["name"])
            elif config[i]["type"] == "ovs_bond":
                self.available_devices.append(config[i]["name"])
            elif config[i]["type"] == "linux_bond":
                self.available_devices.append(config[i]["name"])

    def _select_device(self):
        pass
