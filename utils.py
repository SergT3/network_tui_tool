import netifaces


def get_interfaces():
    interface_list = netifaces.interfaces()
    interface_list.remove('lo')
    return interface_list


def to_asciimatics_list(python_list):
    asciimatics_list = []
    for i in range(len(python_list)):
        asciimatics_list.append((python_list[i], i))
    return asciimatics_list


def obj_list_util(name, size):
    nic_list = []
    for i in range(size):
        nic_list.append((name + str(i), i))
    return nic_list
