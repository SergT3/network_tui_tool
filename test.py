from netconfig import NetConfig
import sys
import yaml
import glob
import utils


# test_yaml = yaml.YAMLObject()
# interface_dict = {'nic1': 'ensp1', 'nic2': 'en2'}
# mappings = {'interface_mappings': interface_dict}
# yaml.dump(mappings, sys.stdout)

test = NetConfig()
test.run()

# print(glob.glob("Configs"))
