import re

"""
General structure:
    Lists in file, e.g. 'Depends' or 'Conffiles' are split into python lists
    Tuples, e.g. packages with version numbers, maintainer names + emails, are split into tuples
"""

class dpkg_status:
    def __init__(self, file_name: str = "/var/lib/dpkg/status"):
        self.update_dpkg_status(file_name)

    def get_dpkg_status(self):
        return self.data
    
    def update_dpkg_status(self, file_name: str = "/var/lib/dpkg/status"):
        self.data = read_dpkg_status(file_name)
        self.data = update_dependency_lists(self.data)

    def get_package_list(self):
        package_list = []
        
        for package in self.data:
            package_list.append({"name": package["name"]})
        
        return package_list

    def get_package(self, name: str):
        package = [item for item in self.data if item["name"] == name]

        if package == [None] or package == []:
            #TODO: Throw exception
            return None
        else:
            package = package[0]

        return prune_dict(package, ["name", "depends", "rdepends"])

def prune_dict(dict_to_prune: dict, keys_to_keep: [str]):
    pruned_dict = dict_to_prune.copy()

    for key in dict_to_prune.keys():
        if key not in keys_to_keep:
            pruned_dict.pop(key)
    
    return pruned_dict


def update_dependency_lists(data):
    updated_data = data

    for package in data:
        for dependency in package.get("depends"):
            updated_item = [item["rdepends"].append({"name": package["name"]}) for item in updated_data if item["name"] == dependency["name"]]
            if updated_item == [None] or updated_item == []:
                continue

            updated_data = [item for item in updated_data if item["name"] != dependency["name"]]
            updated_data.append(updated_item)

    return updated_data



def read_dpkg_status(file_name: str = "/var/lib/dpkg/status"):
    """Read and parse dpkg status files into standard Python data structures"""
    f = open(file_name, "r")
    file = f.read()
    f.close()

    file = file.split("\n\n")

    package_list = []

    for package in file:
        if len(package) == 0:
            continue

        package = package.split("\n")
        split_package = []

        # 'line' starts with space if part of multiline value
        for line in package:
            if len(line) == 0:
                pass

            elif line[0] == ' ':
                split_package[-1] = split_package[-1] + '\n' + line[1:]

            else:
                split_package.append(line)

        package_dict = {}

        for line in split_package:
            package_dict.update(parse_key_val_pair(line))

        package_dict["rdepends"] = []

        if "depends" not in package_dict:
            package_dict["depends"] = []

        package_list.append(package_dict)

    return package_list

def parse_package_list(lst: str):
    """Parse package lists (e.g. in 'Depends') list of dicts"""
    value_list = []

    for package in lst.split(", "):
        package = re.sub("[()]", "", package)
        split_package = package.split(" ", 1)

        package_dict = {"name": split_package[0]}

        # Uncomment to enable version parsing
        #if len(split_package) > 1:
        #    package_dict.update({"Version": split_package[1]})

        value_list.append(package_dict)

    return value_list


def parse_maintainer(value: str):
    """Parse maintainer value (in 'Maintainer' and 'Original-Maintainer') into dict"""
    split_value = value[:-1].split(" <", 1)
    return { "name": split_value[0], "email": split_value[1]}


def parse_key_val_pair(line: str):
    """Parse each key:value pair in dpkg status file into standard python dict"""
    pair = re.split(":[\n ]", line, 1)
    if len(pair) <= 1:
        #TODO: Raise exception
        return line

    key     = pair[0].lower()
    value   = pair[1]

    if key == "package":
        key = "name"

    elif key == "status":
        pass

    elif key == "priority":
        pass

    elif key == "section":
        pass

    elif key == "installed-size":
        pass

    elif key == "maintainer":
        value = parse_maintainer(value)

    elif key == "architecture":
        pass

    elif key == "source":
        pass

    elif key == "version":
        pass

    elif key == "replaces":
        value = parse_package_list(value)

    elif key == "provides":
        value = parse_package_list(value)

    elif key == "depends":
        value = parse_package_list(value)

    elif key == "suggests":
        value = parse_package_list(value)

    elif key == "conflicts":
        value = parse_package_list(value)

    elif key == "conffiles":
        # Split lines to list with each line being tuple object
        value = value.replace("\n ", "\n")
        value = value.split("\n")
        split_value = []
        for line in value:
            split_value.append(tuple(line.split(" ")))
        
        value = split_value

    elif key == "Description":
        # Remove space from beginnings of lines
        value = value.replace("\n ", "\n")

    elif key == "original-maintainer":
        value = parse_maintainer(value)

    elif key == "homepage":
        pass

    elif key == "python-version":
        value = value.split(", ")

    else:
        pass

    return {key : value}
