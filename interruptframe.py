from abc import ABCMeta, abstractmethod
from asciimatics.widgets import Frame
from asciimatics.exceptions import StopApplication
from future.utils import with_metaclass


class InterruptFrame(with_metaclass(ABCMeta, Frame)):

    def __init__(self, screen, model=None):
        super(InterruptFrame, self).__init__(screen,
                                             screen.height,
                                             screen.width,
                                             on_load=self._on_load if hasattr(self, "_on_load") else None,
                                             has_border=True,
                                             title=self.single_title())
        self._screen = screen
        self._model = model
        self.init_layout()

    bridge = ["LinuxBridge", "OVSBridge"]
    bond = ["LinuxBond",  "OVSBond"]

    def single_title(self):
        title = self.get_title()
        if title in self.bridge:
            return "Bridge"
        if title in self.bond:
            return "Bond"
        return title

    @staticmethod
    @abstractmethod
    def get_title(): pass

    def _final_cancel(self):
        raise StopApplication("User closed application")

    @abstractmethod
    def _cancel(self): pass
