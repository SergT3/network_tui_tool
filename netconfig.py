from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError

import sys

from Frames.configs import ConfigsFrame
# from Frames.start import StartFrame
from Frames.devices import DevicesFrame
from Frames.nic import NICFrame
from Frames.home import HomeFrame
from Frames.mappings import MappingsFrame
# from Frames.mappings_intro import IntroFrame
from Frames.new_config import NewConfigFrame


class NetConfig(object):

    def __init__(self):

        self.scenes = []
        self.scenes_by_name = {}
        self.frames = [HomeFrame, MappingsFrame, DevicesFrame, ConfigsFrame, NewConfigFrame, NICFrame]
        self.last_scene = None

    def generate_scenes(self, screen):
        self.scenes = []
        self.scenes_by_name = {}
        for frame in self.frames:
            #          if frame.get_title() == "Start" and hasattr(frame, "effects"):
            #        scene_obj = Scene(frame.effects, 0)
            scene_obj = Scene([frame(screen)], -1, name=frame.get_title())
            self.scenes.append(scene_obj)
            self.scenes_by_name[frame.get_title()] = scene_obj
        return self.scenes

    def run(self):
        while True:
            try:
                Screen.wrapper(self.play, catch_interrupt=True, arguments=[self.last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                self.last_scene = e.scene.name

    def play(self, screen, last_scene_name):
        self.generate_scenes(screen)
        last_scene = self.scenes_by_name[last_scene_name] if last_scene_name is not None else None
        screen.play(self.scenes, stop_on_resize=True, start_scene=last_scene, allow_int=True)
