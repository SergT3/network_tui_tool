from asciimatics.widgets import Frame, PopUpDialog
from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from asciimatics.exceptions import StopApplication
from abc import ABCMeta, abstractmethod
from future.utils import with_metaclass

from utils import HEIGHT_MULTIPLIER, WIDTH_MULTIPLIER, bond, bridge
from palette import get_default_palette, get_warning_palette

import logging

import gettext

_ = gettext.gettext


class InterruptFrame(with_metaclass(ABCMeta, Frame)):
    @abstractmethod
    def frame_title(self):
        """
        Set title for the Frame
        :return:
        """

    def __init__(self, screen, model):
        super(InterruptFrame, self).__init__(screen,
                                             int(screen.height * HEIGHT_MULTIPLIER),
                                             int(screen.width * WIDTH_MULTIPLIER),
                                             can_scroll=True,
                                             title=self.single_title(),
                                             on_load=self._on_load if hasattr(self, "_on_load") else None,
                                             has_border=True)
        self.palette = get_default_palette()
        self._theme = 'custom'
        self._screen = screen
        self._model = model
        self.init_layout()

    def single_title(self):
        title = self.frame_title()
        if title == "Home":
            return "Custom network plan"
        if title in bridge:
            return "Bridge"
        if title in bond:
            return "Bond"
        return title

    @abstractmethod
    def init_layout(self):
        """
        Init all layouts for Frame and fix them in the end
        :return:
        """

    def process_event(self, event):
        # Do the key handling for this Frame.
        if isinstance(event, KeyboardEvent):
            logging.debug("Keyboard pressing = \'%s\'" % str(event.key_code))
            if event.key_code == Screen.ctrl("x"):
                raise StopApplication("User terminated application")
            if event.key_code == Screen.ctrl("c"):
                self._cancel()
            if event.key_code == Screen.ctrl("a"):
                self._add()
            if event.key_code == Screen.ctrl("d"):
                self._delete()
            if event.key_code == Screen.ctrl("r"):
                self.reset()
            if event.key_code == Screen.ctrl("u"):
                self._save_update()

        # Now pass on to lower levels for normal handling of the event.
        return super(InterruptFrame, self).process_event(event)

    @abstractmethod
    def _cancel(self):
        """
        Cancel button from current Frame
        :return:
        """

    @abstractmethod
    def _add(self):
        """
        Add button from current Frame
        :return:
        """

    @abstractmethod
    def _delete(self):
        """
        Delete button from current Frame
        :return:
        """

    @abstractmethod
    def _save_update(self):
        """
        Refresh button from current Frame
        :return:
        """

    def _final_cancel(self):
        raise StopApplication("User closed application")


class ErrorPopUpDialog(PopUpDialog):
    pass


class InfoPopUpDialog(PopUpDialog):
    def __init__(self, screen, text, buttons, on_close=None, has_shadow=False, theme="tlj256"):
        super(InfoPopUpDialog, self).__init__(screen, text, buttons, on_close=on_close, has_shadow=has_shadow,
                                              theme=theme)


class WarnPopUpDialog(PopUpDialog):
    def __init__(self, screen, text, buttons, on_close=None, has_shadow=False, theme="green"):
        super(WarnPopUpDialog, self).__init__(screen, text, buttons, on_close=on_close, has_shadow=has_shadow,
                                              theme=theme)
        self.palette = get_warning_palette()
