import re

"""
General structure:
    Lists in file, e.g. 'Depends' or 'Conffiles' are split into python lists
    Tuples, e.g. packages with version numbers, maintainer names + emails, are split into tuples
"""

class pkg_status:
    pass

def read_pkg_status(file_name: str = "/var/lib/dpkg/status"):
    """Read and parse dpkg status files into standard Python data structures"""
    f = open(file_name, "r")
    file = f.read()
    f.close()

    file = file.split("\n\n")

    package_list = []

    for package in file:
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

        package_list.append(package_dict)

    return package_list

def parse_package_list(lst: str):
    """Parse package lists (e.g. in 'Depends') list of dicts
    
    Structure:
        [
            {
                Package: name,
                [Version: number and sign]
            },
            ...
        ]
    """
    value_list = []

    for package in lst.split(", "):
        package = re.sub("[()]", "", package)
        split_package = package.split(" ", 1)

        package_dict = {"Package": split_package[0]}

        if len(split_package) > 1:
            package_dict.update({"Version": split_package[1]})

        value_list.append(package_dict)

    return value_list


def parse_maintainer(value: str):
    """Parse maintainer value (in 'Maintainer' and 'Original-Maintainer') into dict"""
    split_value = value[:-1].split(" <", 1)
    return { "Name": split_value[0], "Email": split_value[1]}


def parse_key_val_pair(line: str):
    """Parse each key:value pair in dpkg status file into standard python dict"""
    pair = re.split(":[\n ]", line, 1)
    if len(pair) <= 1:
        #TODO: Raise exception
        return line

    key     = pair[0]
    value   = pair[1]

    if key == "Package":
        pass

    elif key == "Status":
        pass

    elif key == "Priority":
        pass

    elif key == "Section":
        pass

    elif key == "Installed-Size":
        pass

    elif key == "Maintainer":
        value = parse_maintainer(value)

    elif key == "Architecture":
        pass

    elif key == "Source":
        pass

    elif key == "Version":
        pass

    elif key == "Replaces":
        value = parse_package_list(value)

    elif key == "Provides":
        value = parse_package_list(value)

    elif key == "Depends":
        value = parse_package_list(value)

    elif key == "Suggests":
        value = parse_package_list(value)

    elif key == "Conflicts":
        value = parse_package_list(value)

    elif key == "Conffiles":
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

    elif key == "Original-Maintainer":
        value = parse_maintainer(value)

    elif key == "Homepage":
        pass

    elif key == "Python-Version":
        value = value.split(", ")

    else:
        pass

    return {key : value}
