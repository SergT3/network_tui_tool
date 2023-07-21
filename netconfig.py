from asciimatics.screen import Screen
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError

import sys
from NetworkObjectFrames.ovs_dpdk_port import OVSDpdkPortFrame
from NetworkObjectFrames.ovs_dpdk_bond import OVSDpdkBondFrame
from NetworkObjectFrames.ovs_user_bridge import OVSUserBridgeFrame
from NetworkObjectFrames.ovs_bond import OVSBondFrame
from NetworkObjectFrames.ovs_bridge import OVSBridgeFrame
from NetworkObjectFrames.linux_bond import LinuxBondFrame
from NetworkObjectFrames.linux_bridge import LinuxBridgeFrame
from NetworkObjectFrames.vlan import VlanFrame
from NetworkObjectFrames.interface import InterfaceFrame
from Frames.configs import ConfigsFrame, ConfigsModel
from Frames.home import HomeFrame
from Frames.mappings import MappingsFrame, MappingsModel
from Frames.new_config import NewConfigFrame

ModelForFrame = {
    "HomeFrame": None,
    "MappingsFrame": MappingsModel,
    "NICFrame": None
}

NetworkObjects = ["Interface", "Vlan", "LinuxBridge", "LinuxBond", "OVSBridge",
                  "OVSBond", "OVSUserBridge", "OVSDpdkBond", "OVSDpdkPort"]


class NetConfig(object):

    def __init__(self):

        self.scenes = []
        self.scenes_by_name = {}
        self.frames = [HomeFrame, MappingsFrame, ConfigsFrame, NewConfigFrame,
                       InterfaceFrame, VlanFrame, LinuxBridgeFrame, LinuxBondFrame, OVSBridgeFrame, OVSBondFrame,
                       OVSUserBridgeFrame, OVSDpdkBondFrame, OVSDpdkPortFrame]
        self.last_scene = None

    def generate_scenes(self, screen):
        self.scenes = []
        self.scenes_by_name = {}
        shared_configs_model = ConfigsModel()
        for frame in self.frames:
            #          if frame.get_title() == "Start" and hasattr(frame, "effects"):
            #        scene_obj = Scene(frame.effects, 0)
            if frame.frame_title() == "Configs" or frame.frame_title() == "NewConfig"\
                     or frame.frame_title() in NetworkObjects:
                scene_obj = Scene([frame(screen,
                                         model=shared_configs_model)], name=frame.frame_title())
            else:
                scene_obj = Scene([frame(screen,
                                         model=ModelForFrame[frame.frame_title() + "Frame"])], -1, name=frame.frame_title())
            self.scenes.append(scene_obj)
            self.scenes_by_name[frame.frame_title()] = scene_obj
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
