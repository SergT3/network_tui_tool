from asciimatics.widgets import Layout, Label, Divider, Text, CheckBox
from interruptframe import InterruptFrame


class NICFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "NIC"

    def init_layout(self):
        gap_layout1 = Layout([1, 1])
        self.add_layout(gap_layout1)
        gap_layout1.add_widget(Divider(draw_line=False, height=3))
        layout1 = Layout([1, 1, 1, 1, 1], True)
        self.add_layout(layout1)
        layout1.add_widget(Text("Name: "), 1)
        layout1.add_widget(CheckBox("", label="DHCP: "), 1)
        layout1.add_widget(CheckBox("", label="DNS: "), 1)
        layout1.add_widget(Text("mtu: "), 1)
        layout1.add_widget(Label("DNS Servers: "), 1)
        layout1.add_widget(Label("Domain: "), 1)
        # layout1.add_widget()
        # layout1.add_widget()
        # layout1.add_widget()
        self.fix()

    def _cancel(self):
        pass
