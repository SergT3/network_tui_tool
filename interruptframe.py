from abc import ABCMeta, abstractmethod
from asciimatics.widgets import Frame
from asciimatics.exceptions import StopApplication
from asciimatics.screen import Screen
from future.utils import with_metaclass


class InterruptFrame(with_metaclass(ABCMeta, Frame)):

    def __init__(self, screen, model=None):
        super(InterruptFrame, self).__init__(screen,
                                             screen.height,
                                             screen.width,
                                             on_load=self._on_load if hasattr(self, "_on_load") else None,
                                             has_border=True,
                                             title=self.single_title())
        self.palette = {
        "background": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "shadow": (Screen.COLOUR_BLACK, None, Screen.COLOUR_BLACK),
        "disabled": (Screen.COLOUR_BLACK, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "invalid": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_RED),
        "label": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "borders": (Screen.COLOUR_BLACK, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "scroll": (Screen.COLOUR_GREEN, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "title": (Screen.COLOUR_GREEN, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "edit_text": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "focus_edit_text": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "readonly": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_readonly": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "button": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_button": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_YELLOW),
        "control": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "selected_control": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_control": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "selected_focus_control": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
        "field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "selected_field": (Screen.COLOUR_YELLOW, Screen.A_BOLD, Screen.COLOUR_BLUE),
        "focus_field": (Screen.COLOUR_WHITE, Screen.A_NORMAL, Screen.COLOUR_BLUE),
        "selected_focus_field": (Screen.COLOUR_WHITE, Screen.A_BOLD, Screen.COLOUR_CYAN),
    }

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
