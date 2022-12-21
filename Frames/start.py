from asciimatics.effects import Cycle
from asciimatics.renderers import FigletText
from asciimatics.widgets import Layout

from interruptframe import InterruptFrame


class StartFrame(InterruptFrame):

    @staticmethod
    def get_title():
        return "Start"

    def init_layout(self):
        # effects = [Cycle(self._screen, FigletText("NetConfig", font='big'), self._screen.height // 2,
        # delete_count=60)] self._screen.play([Scene(effects, 5)])
        self.add_layout(Layout([1]))
        self.scene.add_effect(Cycle(self._screen,
                                    FigletText("NetConfig", font='big'),
                                    self._screen.height // 2,
                                    delete_count=60))

    def _cancel(self):
        pass
