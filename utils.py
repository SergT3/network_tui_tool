import glob
from os.path import exists
import netifaces
import yaml


def list_files(pattern):
    return glob.glob(pattern)


def get_interfaces():
    interface_list = netifaces.interfaces()
    while "lo" in interface_list:
        interface_list.remove("lo")
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
        nic_list.append(name + str(i))
    return nic_list


def extended_dup_list(python_list, extension):
    extended_list = []
    for i in range(len(python_list)):
        extended_list.append((python_list[i], python_list + extension))
    return extended_list


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
                file_dict = yaml.full_load(file)
                return file_dict
            except yaml.YAMLError:
                return None
    return None


def save_data(frame, data):
    write_to_file(frame + "_data.yaml", data)

def get_frame_data(frame):
    if exists(frame.get_title() + "_data.yaml"):
        with open(frame.get_title() + "_data.yaml", "r") as file:
            try:
                frame_data = yaml.full_load(file)
                return frame_data
            except yaml.YAMLError or KeyError:
                return None
    return None

def remove_empty_keys(empty_key_dict):
    temp_dict = {key: value for (key, value) in empty_key_dict.items()
                 if value is not False
                 and value != ''
                 and value is not None
                 and value != []
                 }
    return temp_dict
