# https://pypi.org/classifiers/
# https://test.pypi.org/pypi?%3Aaction=list_classifiers
# https://github.com/pypa/sampleproject/blob/master/setup.py
# https://packaging.python.org/guides/distributing-packages-using-setuptools/
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name                          = 'test-project-python',
    version                       = '0.0.2.post9',
    description                   = 'Test project to see how packaging works on PyPI.',
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
    url                           = 'https://github.com/shailshouryya/test-project',
    author                        = 'shailshouryya',
    author_email                  = 'slowbutsteady1234+github@gmail.com',
    license                       = 'MIT',


    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: Free For Educational Use',
        'License :: Free For Home Use',
        'License :: Free for non-commercial use',
        'License :: Freely Distributable',
        'License :: Freeware',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 11',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Home Automation',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: System :: Installation/Setup',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
    keywords='PyPI packaging package subpackage module namespace plugin extensions import macos windows linux setuptools setup',


    # http://code.nabla.net/doc/setuptools/api/setuptools/setuptools.find_packages.html
    # https://stackoverflow.com/questions/51286928/what-is-where-argument-for-in-setuptools-find-packages
    packages=find_packages(), # reawd links above to understand how to use variations below
    # packages=find_packages(exclude=['includes_all_directories', 'other_than', 'the_ones_here']),
    # packages=find_namespace_packages(include=['only_includes_this']),
    # package_dir={'':'src'},


    python_requires  = '>=3.6.*, <4',
    install_requires = [],  # Optional
    # https://packaging.python.org/discussions/install-requires-vs-requirements/


    # If there are data files included in your packages that need to be installed, specify them here.
    # If using Python 2.6 or earlier, then these have to be included in MANIFEST.in as well.
    package_data = {  # Optional
        # 'sample': ['package_data.dat'],
    },
    # Although 'package_data' is the preferred approach, in some case you may need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],  # Optional


    # # To provide executable scripts, use entry points in preference to the "scripts" keyword.
    # # Entry points provide cross-platform support and allow `pip` to create the appropriate form of executable for the target platform.
    # # For example, the following would provide a command called `test_project_python` which
    # #   tries to run a __main__ function (or whatever comes after the ":" (colon) for the defined command) from
    # #   the test_project_python package when invoked directly from the command line
    # # This means we
    # #   - load test_project_python.__init__
    # #     - the __init__ module subsequently loads all other modules in the test_project_python package including the __main__ module
    # #   - try to call a __main__ function from whatever is loaded in this (__init__ module) namespace
    # #   - fail since the __init__ module loads the __main__ module
    # #     - therefore, there is no __main__ function in the test_project_python namespace since
    # #       the __main__ we loaded is a reference to the test_project_python.__main__ module
    # # - see https://stackoverflow.com/a/782984 for a better explanation
    # entry_points={  # Optional
    #    'console_scripts': [
    #        'test_project_python=test_project_python:__main__',
    #    ],
    # },
    #
    #
    # # contents of /home/USERNAME/.local/bin/test_project_python after running the above:
    #
    # # #!/path/to/your/bin/for/python_command
    # # # -*- coding: utf-8 -*-
    # # import re
    # # import sys
    # # from test_project_python import __main__
    # # if __name__ == '__main__':
    # #     sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    # #     sys.exit(__main__())
    #
    # # the test_project_python command FAILS
    # # if a `__main__` function is not defined inside
    # # test_project_python (inside the test_project_python.__init__ namespace):
    #
    # # $ test_project_python
    # # Entered test_project_python.__main__ :)
    # # Traceback (most recent call last):
    # #   File "/home/USERNAME/.local/bin/test_project_python", line 8, in <module>
    # #     sys.exit(__main__())
    # # TypeError: 'module' object is not callable
    # # potential useful references:
    # #   https://stackoverflow.com/questions/4534438/typeerror-module-object-is-not-callable
    # #   https://stackoverflow.com/questions/5280203/what-does-this-mean-exit-main


     entry_points={  # Optional
       'console_scripts': [
           'command_name=test_project_python:function_name',                                        # compare the output of `command_name`                         versus `python3 -m test_project_python`
           'command_name_for_function_in__main__=test_project_python.__main__:function_in__main__', # compare the output of `command_name_for_function_in__main__` versus `python3 -m test_project_python`
       ],
    },


    project_urls = {
        'Bug Reports':  'https://github.com/shailshouryya/test-project/issues',
        'PyPi Funding': 'https://donate.pypi.org',
        'Source':       'https://github.com/shailshouryya/test-project'
    },
)

'''
files created by setuptools for the commands specified in entry_points['console_scripts'] for reference:


# contents of /path/to/your/bin/for/python_command/command_name:
#!/path/to/your/bin/for/python_command
# -*- coding: utf-8 -*-
import re
import sys
from test_project_python import function_name
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(function_name())


# contents of /path/to/your/bin/for/python_command/command_name_for_function_in__main__:
#!/path/to/your/bin/for/python_command
# -*- coding: utf-8 -*-
import re
import sys
from test_project_python.__main__ import function_in__main__
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(function_in__main__())

'''
