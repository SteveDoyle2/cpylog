#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages

imajor, minor1, minor2 = sys.version_info[:3]
if sys.version_info < (3, 7):  # 3.7.1 used
    # makes sure we don't get the following bug:
    #   Issue #19099: The struct module now supports Unicode format strings.
    sys.exit('Upgrade your Python to >= 3.7+; version=(%s.%s.%s)' % (imajor, minor1, minor2))


packages = find_packages() # exclude=['ez_setup', 'examples', 'tests'] + exclude_words

#is_dev = (
    #'TRAVIS' in os.environ or
    #'APPVEYOR' in os.environ or
    #'READTHEDOCS' in os.environ
#)
is_travis = 'TRAVIS' in os.environ
#is_rtd = 'READTHEDOCS' in os.environ

install_requires = []
is_windows = 'nt' in os.name
if is_travis and not is_windows:
    #install_requires.append('python-coveralls')
    install_requires.append('codecov')
    #install_requires.append('coverage')


# get package metadata
import cpylog
setup(
    name='cpylog',
    version=cpylog.__version__,
    description=cpylog.__desc__,
    long_description=cpylog.__long__,
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    python_requires='>=3.7',
    author=cpylog.__author__,
    author_email=cpylog.__email__,
    url=cpylog.__website__,
    license=cpylog.__license__,
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    #{'': ['license.txt']}
    #package_data={'': ['*.png']},
    #data_files=[(icon_path, icon_files2)],
    package_data={
        # https://pythonhosted.org/setuptools/setuptools.html#including-data-files
        # If any package contains *.png files, include them:
        '': ['*.png'],
        #'mypkg': ['data/*.dat'],
    },
    entry_points={
        'console_scripts': [
        ]
    },
    test_suite='cpylog.test_log',
)
