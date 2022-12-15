import netifaces
import yaml
import glob

def exists(dir_name):
    return len(glob.glob(dir_name)) != 0

def list_files(pattern):
    return glob.glob(pattern)


def get_interfaces():
    interface_list = netifaces.interfaces()
    interface_list.remove('lo')
    return interface_list


def to_asciimatics_list(python_list, dropdown=False):
    asciimatics_list = []
    if dropdown:
        asciimatics_list.append(("None", "None"))
    for i in range(len(python_list)):
        asciimatics_list.append((python_list[i], python_list[i]))
    return asciimatics_list


def dup_list_util(name, size):
    nic_list = []
    for i in range(size):
        nic_list.append(name + str(i))
    return nic_list


def write_to_file(filename, data):
    with open(filename, 'w') as file:
        try:
            filedata = yaml.dump(data)
            file.write(filedata)
            return True
        except Exception:
            return False
