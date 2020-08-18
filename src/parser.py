import re
import json

class pkg_status:
    pass

def read_pkg_status(file_name: str):
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

def parse_key_val_pair(line: str):
    pair    = re.split(":[\n ]", line, 1)
    if len(pair) <= 1:
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
        # Transform into (name, email) tuple
        value = tuple(value[:-1].split(" <", 1))

    elif key == "Architecture":
        pass

    elif key == "Source":
        pass

    elif key == "Version":
        pass

    elif key == "Replaces":
        value = value.split(", ")

    elif key == "Provides":
        value = value.split(", ")

    elif key == "Depends":
        value = value.split(", ")

    elif key == "Suggests":
        value = value.split(", ")

    elif key == "Conflicts":
        value = value.split(", ")

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
        # Transform into (name, email) tuple
        value = tuple(value[:-1].split(" <", 1))

    elif key == "Homepage":
        pass

    elif key == "Python-Version":
        value = value.split(", ")

    else:
        pass

    return {key : value}
