from src.parser import *
import pytest


def test_pass_maintainer():
    expected = { "Name": "Test Name", "Email": "test.name@test.com"}
    assert expected == parse_maintainer("Test Name <test.name@test.com>")

@pytest.mark.parametrize("package_list", [
    (
        "test_package (>= 5.0)", 
        [{"Package": "test_package", "Version": ">= 5.0"}]
    ),(   
        "libc6 (>= 2.4), libwrap0 (>= 7.6-4~)",
        [
            {"Package": "libc6", "Version": ">= 2.4"},
            {"Package": "libwrap0", "Version": ">= 7.6-4~"}
        ]
    ),(
        "junit (>= 3.8.2), libplexus-cipher-java",
        [
            {"Package": "junit", "Version": ">= 3.8.2"},
            {"Package": "libplexus-cipher-java"}
        ]

    )
])

def test_parse_package_list(package_list):
    assert parse_package_list(package_list[0]) == package_list[1]

@pytest.mark.parametrize("input", [
    (
        "Depends: test_package (>= 5.0)", 
        {"Depends": [{"Package": "test_package", "Version": ">= 5.0"}]}
    ),(   
        "Depends: libc6 (>= 2.4), libwrap0 (>= 7.6-4~)",
        {"Depends":
            [
                {"Package": "libc6", "Version": ">= 2.4"},
                {"Package": "libwrap0", "Version": ">= 7.6-4~"}
            ]
        }
    ),(
        "Depends: junit (>= 3.8.2), libplexus-cipher-java",
        {"Depends":
            [
                {"Package": "junit", "Version": ">= 3.8.2"},
                {"Package": "libplexus-cipher-java"}
            ]
        }

    )
])

def test_key_val_pair(input):
    assert parse_key_val_pair(input[0]) == input[1]