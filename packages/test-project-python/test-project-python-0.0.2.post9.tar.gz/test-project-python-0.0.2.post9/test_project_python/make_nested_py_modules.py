import itertools
import os
import shutil

from typing import Any, Optional, Collection, Mapping, TextIO, TypeVar, Tuple, Union


PackageLevelDefinition = Mapping[str, Collection[str]]
PackageLevelsMap       = Mapping[int, PackageLevelDefinition]
T                      = TypeVar('T')


def main(
    package_levels:                Optional[PackageLevelsMap]    = None,
    start:                         int                           = 1,
    end:                           int                           = 2,
    directory_removal_prefixes:    Optional[Collection[str]]     = None,
) -> None:
    none_type = type(None)
    validate_instance_is_from_class(package_levels, (none_type, Mapping), 'package_levels')
    validate_instance_is_from_class(start, int, 'start')
    validate_instance_is_from_class(end,   int, 'end')
    validate_instance_is_from_class(directory_removal_prefixes, (none_type, Collection), 'directory_removal_prefixes')
    if directory_removal_prefixes is None: directory_removal_prefixes = ['package_']
    remove_script_created_contents(directory_removal_prefixes)
    if package_levels is None:
        package_levels = {
            1: {
                'subpackage_prefixes': ['package_'],
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
    create_packages(package_levels, start, end, base_path='.', base_name='', __init__files=[])


def validate_instance_is_from_class(
    obj:                 Any,
    acceptable_types:    Union[T, Tuple],
    variable_name:       str,
) -> Union[bool, TypeError]:
    if isinstance(acceptable_types, tuple): formatted_acceptable_types = f'one of the following types: {acceptable_types}' # multiple acceptable types
    else:                                   formatted_acceptable_types = f'an instance of {acceptable_types}'              # one      acceptable type
    variable_reference = f'variable `{variable_name}`'
    error_message = f'''
    Invalid value provided for {variable_reference}
      You provided {obj} (type {type(obj)}) for {variable_reference}, but
      {variable_reference} needs to be {formatted_acceptable_types}
    '''
    if not isinstance(obj, acceptable_types):
        raise TypeError(error_message)


def remove_script_created_contents(
    directory_removal_prefixes:    Collection[str],
) -> None:
    top_level_path, top_level_nested_directories, top_level_files = next(os.walk('.'))
    # print(top_level_path, top_level_nested_directories, top_level_files)
    for nested_directory in top_level_nested_directories:
        if any(nested_directory.startswith(prefix) for prefix in directory_removal_prefixes):
            remove_directory(nested_directory)


def remove_directory(
    directory:    str,
) -> None:
    shutil.rmtree(directory)


def create_packages(
    package_levels:   PackageLevelsMap,
    start:            int,
    end:              int,
    base_path:        str,
    base_name:        str,
    __init__files:    Collection[Tuple[str, str]],
) -> None:
    if start <= end:
        current_level               = start
        base_name                   = base_name + '.' if base_name else ''
        current_package             = package_levels.get(current_level, {})
        current_subpackage_prefixes = current_package.get('subpackage_prefixes', [f'level_{current_level}_'])
        current_subpackage_suffixes = current_package.get('subpackage_suffixes', ['_package'])
        validate_instance_is_from_class(current_subpackage_prefixes, Collection, f'''package_levels[{current_level}]['subpackage_prefixes']''')
        validate_instance_is_from_class(current_subpackage_suffixes, Collection, f'''package_levels[{current_level}]['subpackage_suffixes']''')
        for subpackage_prefix, subpackage_suffix in itertools.product(current_subpackage_prefixes, current_subpackage_suffixes):
            package_name, package_path        = determine_subpackage_info(subpackage_prefix, subpackage_suffix, base_path, base_name)
            module_prefixes , module_suffixes = determine_module_info_for_subpackage(current_package)
            validate_instance_is_from_class(module_prefixes, Collection, f'''package_levels[{current_level}]['module_prefixes']''')
            validate_instance_is_from_class(module_suffixes, Collection, f'''package_levels[{current_level}]['module_suffixes']''')
            create_subpackage(package_path)
            for __init__file, __init__package_path in __init__files:
                relative_subpackage_path, relative_subpackage_name = determine_relative_subpackage_info(package_name, __init__package_path)
                __init__file.write(f'from {relative_subpackage_path} import {relative_subpackage_name}\n')
            subpackage__init__filepath = os.path.join(package_path, '__init__.py')
            with open(subpackage__init__filepath, mode='w', encoding='utf-8', buffering=-1) as subpackage__init__file:
                create_modules_for_subpackage(package_path, package_name, module_prefixes, module_suffixes, subpackage__init__file)
                __init__files.append((subpackage__init__file, package_name))
                create_packages(package_levels, start+1, end, base_path=package_path, base_name=package_name, __init__files=__init__files)
                __init__files.pop()


def determine_subpackage_info(
    subpackage_prefix:    str,
    subpackage_suffix:    str,
    base_path:            str,
    base_name:            str,
) -> Tuple[str, str]:
    subpackage_name      = subpackage_prefix + subpackage_suffix
    full_subpackage_name = base_name + subpackage_name
    full_subpackage_path = os.path.join(base_path, subpackage_name)
    print(f'package_name is {full_subpackage_name}')
    return full_subpackage_name, full_subpackage_path


def determine_module_info_for_subpackage(
    current_package:    PackageLevelDefinition,
) -> Tuple[str, str]:
    module_suffixes = current_package.get('module_suffixes', ['_name'])
    module_prefixes = current_package.get('module_prefixes', ['module_'])
    return module_prefixes, module_suffixes


def determine_relative_subpackage_info(
    package_name:           str,
    __init__package_path:   str,
) -> Tuple[str, str]:
    # imports still work with the hard coded path but provide less flexibility
    # than relative imports
    #     renaming a base package would require renaming the
    #     subpackage `import` statement in the `__init__` module when
    #     the import is a hard coded import
    #         for example, renaming `package_name` to `new_package_name` would require changing
    #         `import package_name.to.subpackage.module`
    #         to
    #         `import new_package_name.to.subpackage.module`
    #         in the package_name.to.__init__.py module (new_package_name.to.__init__ module after the rename)
    #     renaming a base package would NOT require renaming the
    #     subpackage `import` statement in the `__init__` module when
    #     the import is a relative import
    #         for example, renaming `package_name` to `new_package_name` would require no change to
    #         `from . import subpackage.module`
    #         in the package_name.to.__init__.py module (new_package_name.to.__init__ module after the rename)
    relative_subpackage_path_start = len(__init__package_path)
    normalize_subpackage_path      = package_name[relative_subpackage_path_start:]
    subpackages                    = normalize_subpackage_path.split('.')
    if len(subpackages) == 2:
        relative_subpackage_path = '.'
        relative_subpackage_name = subpackages[1]
    else:
        relative_subpackage_path = '.'.join(subpackages[:-1])
        relative_subpackage_name = subpackages[-1]
    return relative_subpackage_path, relative_subpackage_name


def create_subpackage(
    package_path:    str,
    mode:            int     = 511,
    exist_ok:        bool    = False,
) -> None:
    os.makedirs(name=package_path, mode=mode, exist_ok=exist_ok)


def create_modules_for_subpackage(
    package_path:              str,
    package_name:              str,
    module_prefixes:           Collection[str],
    module_suffixes:           Collection[str],
    subpackage__init__file:    TextIO,
) -> None:
    for module_prefix, module_suffix in itertools.product(module_prefixes, module_suffixes):
        module_name = f'{module_prefix}{module_suffix}'
        subpackage__init__file.write(f'from . import {module_name}\n')
        module_file_path = os.path.join(package_path, f'{module_name}.py')
        with open(module_file_path, mode='w', encoding='utf-8', buffering=-1) as file:
            file.write(f'''print('{package_name}.{module_name}')\n''')


if __name__ == '__main__':
    main()
