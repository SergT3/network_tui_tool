import glob
import socket
from copy import deepcopy
from os.path import exists
from os import chdir
import yaml

HEIGHT_MULTIPLIER = 1
WIDTH_MULTIPLIER = 1

bridge = ["LinuxBridge", "OVSBridge"]
bond = ["LinuxBond", "OVSBond"]

def list_files(pattern):
    return glob.glob(pattern)


def get_interfaces():
    interface_list = []
    for interface in socket.if_nameindex():
        interface_list.append(interface[1])
    for i in interface_list:
        if not exists("/sys/class/net/" + i + "/device"):
            interface_list.remove(i)
    return interface_list


def to_asciimatics_list(python_list, dropdown=False):
    asciimatics_list = []
    if dropdown:
        asciimatics_list.append(("None", None))
    for i in range(len(python_list)):
        asciimatics_list.append((python_list[i], python_list[i]))
    return asciimatics_list


def indexed_dup_list(name, size):
    nic_list = []
    for i in range(size):
        nic_list.append(name + str(i + 1))
    return nic_list


# def extended_dup_list(python_list, extension):
#     extended_list = []
#     for i in range(len(python_list)):
#         extended_list.append((python_list[i], python_list + extension))
#     return extended_list


def write_to_file(filename, data, open_type='w'):
    with open(filename, open_type) as file:
        try:
            filedata = yaml.dump(data)
            if open_type == 'a':
                file.write("\n")
            file.write(filedata)
            return True
        except yaml.YAMLError:
            return False


def read_from_yaml(filename):
    if exists(filename):
        with open(filename, "r") as file:
            try:
                file = yaml.full_load(file)
                return file
            except yaml.YAMLError:
                return None
    return None


def remove_empty_keys(empty_key_dict):
    clear_dict = {key: value for (key, value) in empty_key_dict.items()
                  if value is not False
                  and value != ''
                  and value is not None
                  and value != []
                  }
    return clear_dict


def remove_vlan_members(net_object):
    if "members" in net_object.keys():
        for i in net_object["members"]:
            if i["type"] == "vlan":
                net_object["members"].remove(i)
            else:
                remove_vlan_members(i)
        if not net_object["members"]:
            net_object.pop("members")


def remove_deep_member(net_object, member):
    if "members" in net_object.keys():
        for i in net_object["members"]:
            if i == member:
                net_object["members"].remove(i)
                break
            else:
                remove_deep_member(i, member)
        if not net_object["members"]:
            net_object.pop("members")
