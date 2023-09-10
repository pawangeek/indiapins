#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Pawan Kumar Jain",
    author_email='pawanjain.432@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],
    
    description="Python package for mapping pins to the place where it belong",
    entry_points={
        'console_scripts': [
            'indiapins=indiapins.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='indiapins india pincodes zipcodes',
    name='indiapins',
    packages=find_packages(include=['indiapins', 'indiapins.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pawangeek/indiapins',
    version='0.1.4',
    zip_safe=False,
)
