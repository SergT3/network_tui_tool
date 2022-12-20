from asciimatics.effects import *
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene

from interruptframe import InterruptFrame


class StartFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "Start"

    def init_layout(self):
        effects = [Cycle(self._screen, FigletText("NetConfig", font='big'), self._screen.height // 2, delete_count=60)]
        self._screen.play([Scene(effects, 5)])

    def _save_update(self):
        pass

    def _add(self):
        pass

    def _delete(self):
        pass

    def _cancel(self):
        pass
