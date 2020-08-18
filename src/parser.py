import re

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
        new_package = []

        # 'line' starts with space if part of multiline value
        for line in package:
            if len(line) == 0:
                pass
            elif line[0] == ' ':
                new_package[-1] = new_package[-1] + '\n' + line[1:]
            else:
                new_package.append(line)

        package = new_package
        new_package = {}

        for line in package:
            print(parse_key_val_pair(line))
            new_package.update(parse_key_val_pair(line))

        package_list.append(new_package)

    
    
    print(package_list[0])


def parse_key_val_pair(line: str):
    pair    = line.split(": ", 1)
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
        value = value[:-1]
        value = value.split(" <", 1)

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
        value = value.replace("\n ", "\n")

    elif key == "Description":
        value = value.replace("\n ", "\n")

    elif key == "Original-Maintainer":
        value = value[:-1]
        value = value.split(" <", 1)

    elif key == "Homepage":
        pass

    elif key == "Python-Version":
        value = value.split(", ")

    else:
        pass

    return {key : value}
