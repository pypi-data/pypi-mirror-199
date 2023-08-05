from . import make_nested_py_modules


EXAMPLE_1 = {
    1: {
        'subpackage_prefixes': ['example_1_package'],
    }
}

EXAMPLE_2 = {
    1: {
        'subpackage_prefixes': ['example_2_package'],
        'subpackage_suffixes': [''],
        'module_prefixes':     ['module_'],
        'module_suffixes':     ['a', 'b', 'c', 'd', 'e'],
    },
    2: {
        'subpackage_prefixes': ['subpackage_'],
        'subpackage_suffixes': ['a', 'b', 'c'],
        'module_prefixes':     [''],
        'module_suffixes':     ['a', 'b', 'c', 'd', 'e'],
    },
}

EXAMPLE_3 = {
    1: {
        'subpackage_prefixes': ['example_3_package_'],
        'subpackage_suffixes': ['a', 'b', 'c'],
        'module_prefixes':     ['module_'],
        'module_suffixes':     ['a', 'b', 'c', 'd', 'e'],
    },
    2: {
        'subpackage_prefixes': ['subpackage_'],
        'subpackage_suffixes': ['a', 'b', 'c'],
        'module_prefixes':     [''],
        'module_suffixes':     ['a', 'b', 'c', 'd', 'e'],
    },
    3: {
        'subpackage_prefixes': ['subpackage_'],
        'subpackage_suffixes': ['a', 'b', 'c'],
        'module_prefixes':     [''],
        'module_suffixes':     ['a', 'b', 'c', 'd', 'e'],
    },
    4: {
        'subpackage_prefixes': ['subpackage_'],
        'subpackage_suffixes': ['a', 'b', 'c'],
        'module_prefixes':     [''],
        'module_suffixes':     ['a', 'b', 'c', 'd', 'e'],
    },
}


def main() -> None:
    make_nested_py_modules.main(package_levels=EXAMPLE_1, start=1, end=7, directory_removal_prefixes=['example_1_package'])
    make_nested_py_modules.main(package_levels=EXAMPLE_2, start=1, end=2, directory_removal_prefixes=['example_2_package'])
    make_nested_py_modules.main(package_levels=EXAMPLE_3, start=1, end=5, directory_removal_prefixes=['example_3_package'])


if __name__ == '__main__':
    main()
