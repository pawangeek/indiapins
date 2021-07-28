=========
indiapins
=========


.. image:: https://img.shields.io/pypi/v/indiapins.svg
        :target: https://pypi.python.org/pypi/indiapins

.. image:: https://img.shields.io/travis/pawangeek/indiapins.svg
        :target: https://travis-ci.com/pawangeek/indiapins

.. image:: https://readthedocs.org/projects/indiapins/badge/?version=latest
        :target: https://indiapins.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pawangeek/indiapins/shield.svg
     :target: https://pyup.io/repos/github/pawangeek/indiapins/
     :alt: Updates

.. image:: https://img.shields.io/github/license/pawangeek/indiapins.svg

.. image:: https://img.shields.io/pypi/pyversions/indiapins.svg


Python package for mapping pins to the place where it belong

* Free software: MIT license
* Documentation: https://indiapins.readthedocs.io.
* Github Repo: https://github.com/pawangeek/indiapins
* PyPI: https://pypi.org/project/indiapins/


Installation
------------

Install the plugin using `pip`:

.. code-block:: shell

   $ pip install indiapins

Alternatively, install from source by cloning this repo then running
`setup.py`:

.. code-block:: shell

   $ python setup.py install


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
#####################

It extracts the district of given Indian pincode

.. code-block:: python

    indiapins.districtmatch('302005')

    'Jaipur'

