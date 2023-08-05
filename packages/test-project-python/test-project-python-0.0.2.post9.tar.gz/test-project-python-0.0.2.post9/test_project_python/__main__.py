print('Entered test_project_python.__main__ :)')


def function_in__main__() -> None:
    print('Ran test_project_python.__main__.function_in__main__')
    print('''
    To better understand how commands from the 'console_scripts' key inside
    the entry_points dictionary in setup.py works, run and compare
        command_name
        command_name_for_function_in__main__
        python3   -m test_project_python        # Linux/macOS
        python    -m test_project_python        # Windows
        custom_py -m test_project_python        # if you use a custom alias for python command
    This assumes you've already installed the package with:
        pip install test_project_python         # installs from PyPI
        pip install .                           # installs local version (you need to clone this repo and then run this from the test_project/python directory)
    ''')


if __name__ == '__main__':
    print('__name__ == "__main__" is True for test_project_python.__main__')
    function_in__main__()
