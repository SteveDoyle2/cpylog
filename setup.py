#!/usr/bin/env python
import os
import sys
from setuptools import setup, find_packages
PY2 = False
PY3 = True
if sys.version_info < (3, 0):
    PY2 = True
    PY3 = False

imajor, minor1, minor2 = sys.version_info[:3]
if sys.version_info < (2, 7, 7):  # 2.7.15 used
    # makes sure we don't get the following bug:
    #   Issue #19099: The struct module now supports Unicode format strings.
    sys.exit('Upgrade your Python to >= 2.7.7 or 3.5+; version=(%s.%s.%s)' % (imajor, minor1, minor2))

if PY3:
    if sys.version_info < (3, 5, 0):  # 3.7.1 used
        sys.exit('Upgrade your Python to >= 2.7.7 or 3.5+; version=(%s.%s.%s)' % (imajor, minor1, minor2))


# set up all icons
import cpylog
setup(
    name='cpylog',
    version=cpylog.__version__,
    description=cpylog.__desc__,
    long_description="""\
""",
    classifiers=[
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    python_requires='>=3.6*',
    author=cpylog.__author__,
    author_email=cpylog.__email__,
    url=cpylog.__website__,
    license=cpylog.__license__,
    packages=[],
    include_package_data=True,
    zip_safe=False,
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

