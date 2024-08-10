=========
indiapins
=========


.. image:: https://img.shields.io/pypi/v/indiapins?label=PyPI&logo=PyPI&logoColor=white&color=blue
        :target: https://pypi.python.org/pypi/indiapins

.. image:: https://img.shields.io/pypi/pyversions/indiapins?label=Python&logo=Python&logoColor=white
    :target: https://www.python.org/downloads
    :alt: Python versions

.. image:: https://ci.appveyor.com/api/projects/status/43hcwr4me6vjb1fg?svg=true
        :target: https://ci.appveyor.com/project/pawangeek/indiapins
        :alt: Build

.. image:: https://static.pepy.tech/badge/indiapins
     :target: https://pepy.tech/project/indiapins
     :alt: Downloads

.. image:: https://pyup.io/repos/github/pawangeek/indiapins/shield.svg
     :target: https://pyup.io/repos/github/pawangeek/indiapins/
     :alt: Updates


**Indiapins is a Python package for getting the places tagged to particular Indian pincode**

**Data is last updated of 10, August, 2024, with 157177 area pin codes**

* Free software: MIT license
* Documentation: https://pawangeek.github.io/indiapins/
* Github Repo: https://github.com/pawangeek/indiapins
* PyPI: https://pypi.org/project/indiapins/


Installation
------------

Install the plugin using 'pip':

.. code-block:: shell

   $ pip install indiapins

Alternatively, install from source by cloning this repo then running
'setup.py':

.. code-block:: shell

   $ python setup.py install


Features
--------
* Get all the mappings of given pins
* The Python sqlite3 module is not required, so easily to use in Clouds (no additional dependencies)
* Works with 3.9, 3.10, 3.11, 3.12, 3.13 and PyPy
* Cross-platform: Windows, Mac, and Linux are officially supported.
* Simple usage and very fast results


Examples
--------

1. Exact Match
##############

To find the names of all places, districts, circles and related information by given Indian Pincode

**Important: The Pincode should be of 6 digits, in string format**

.. code-block:: python

    indiapins.matching('110011')

    [{'Name': 'Nirman Bhawan', 'BranchType': 'Sub Post Office', 'DeliveryStatus': 'Delivery', 'Circle': 'Delhi', 'District': 'Central Delhi', 'Division': 'New Delhi Central', 'Region': 'Delhi', 'Block': 'New Delhi', 'State': 'Delhi', 'Country': 'India', 'Pincode': '110011'},
    {'Name': 'South Avenue', 'BranchType': 'Sub Post Office', 'DeliveryStatus': 'Non-Delivery', 'Circle': 'Delhi', 'District': 'Central Delhi', 'Division': 'New Delhi Central', 'Region': 'Delhi', 'Block': 'New Delhi', 'State': 'Delhi', 'Country': 'India', 'Pincode': '110011'},
    {'Name': 'Udyog Bhawan', 'BranchType': 'Sub Post Office', 'DeliveryStatus': 'Non-Delivery', 'Circle': 'Delhi', 'District': 'Central Delhi', 'Division': 'New Delhi Central', 'Region': 'Delhi', 'Block': 'New Delhi', 'State': 'Delhi', 'Country': 'India', 'Pincode': '110011'}]


2. Valid Pincode
################

To check if the given Pincode is valid or not

.. code-block:: python

    indiapins.isvalid('110011')

    True

3. District by Pincode
######################

It extracts the district of given Indian pincode

.. code-block:: python

    indiapins.districtmatch('302005')

    'Jaipur'

4. Coordinates of Pincode
#########################

It extracts all the coordinates of given Indian pincode

.. code-block:: python

    indiapins.coordinates('110011')

    {'Udyog Bhawan': {'latitude': '28.6111111', 'longitude': '77.2127500'},
    'Nirman Bhawan': {'latitude': '28.6108611', 'longitude': '77.2148611'}}
