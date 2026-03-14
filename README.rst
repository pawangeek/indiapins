=========
indiapins
=========


.. image:: https://img.shields.io/pypi/v/indiapins?label=PyPI&logo=PyPI&logoColor=white&color=blue
        :target: https://pypi.python.org/pypi/indiapins

.. image:: https://img.shields.io/pypi/pyversions/indiapins?label=Python&logo=Python&logoColor=white
    :target: https://www.python.org/downloads
    :alt: Python versions

.. image:: https://github.com/pawangeek/indiapins/actions/workflows/ci.yml/badge.svg
        :target: https://github.com/pawangeek/indiapins/actions/workflows/ci.yml
        :alt: CI

.. image:: https://static.pepy.tech/badge/indiapins
     :target: https://pepy.tech/project/indiapins
     :alt: Downloads


**Indiapins is a Python package for getting the places tagged to particular Indian pincode**

**Data is last updated February 21, 2026, with 165,627 area pin codes**

* Free software: MIT license
* Documentation: https://pawangeek.github.io/indiapins/
* Github Repo: https://github.com/pawangeek/indiapins
* PyPI: https://pypi.org/project/indiapins/

What This Library Provides
--------------------------

`indiapins` gives you a local, packaged lookup dataset so you can resolve Indian
pincodes without calling external APIs.

The library currently exposes four core helpers:

* ``matching(zipcode)``: fetch all place records for a pincode
* ``isvalid(zipcode)``: check whether a pincode exists in the dataset
* ``districtmatch(zipcode)``: get district name(s) for a pincode
* ``coordinates(zipcode)``: get location-wise latitude/longitude values

Geospatial helpers are also available:

* ``distance(pin1, pin2, metric="km")``
* ``nearest_pincodes(lat, lon, k=5, metric="km")``
* ``nearest_to_pincode(pin, k=10, metric="km")``
* ``pincodes_in_radius(center, radius_km)``
* ``delivery_offices_in_radius(center, radius_km)``
* ``bearing(pin1, pin2)`` and ``midpoint(pin1, pin2)``
* ``distance_matrix(pincodes, metric="km")``

All public functions validate the input format strictly before lookup:

* pincode must be a Python ``str``
* length must be exactly 6
* only digits are allowed

Validation errors are explicit:

* ``TypeError`` for non-string values (including ``None`` and empty string)
* ``ValueError`` for wrong length or non-digit characters


Installation
------------

Install the plugin using 'pip':

.. code-block:: shell

   $ pip install indiapins

Alternatively, install from source by cloning this repo:

.. code-block:: shell

   $ pip install .


Features
--------
* Get all the mappings of a given pincode
* Offline-friendly lookup from packaged compressed data
* Geodesic distance, nearest, radius, bearing, midpoint, and matrix operations
* No sqlite dependency required, easy to run in cloud/serverless environments
* Works with Python 3.10, 3.11, 3.12, 3.13, 3.14 and PyPy
* Cross-platform support: Windows, macOS, and Linux
* Simple API surface with fast in-memory filtering


Examples
--------

1. Exact Match
##############

Use ``matching`` to retrieve all places and postal metadata tied to a pincode.

**Important: The Pincode should be of 6 digits, in string format**

.. code-block:: python

    indiapins.matching('110011')

    [{'Name': 'Nirman Bhawan', 'BranchType': 'PO', 'DeliveryStatus': 'Delivery', 
      'Circle': 'Delhi Circle', 'District': 'NEW DELHI', 'Division': 'New Delhi Central Division', 
      'Region': 'Delhi Region', 'State': 'DELHI', 'Pincode': 110011,
      'Latitude': 28.6108611, 'Longitude': 77.2148611},
     {'Name': 'Udyog Bhawan', 'BranchType': 'PO', 'DeliveryStatus': 'Non Delivery', 
      'Circle': 'Delhi Circle', 'District': 'NEW DELHI', 'Division': 'New Delhi Central Division',
      'Region': 'Delhi Region', 'State': 'DELHI', 'Pincode': 110011,
      'Latitude': 28.6111111, 'Longitude': 77.2127500}]

Records include these keys:

* ``Name``, ``BranchType``, ``DeliveryStatus``
* ``Circle``, ``Region``, ``Division``, ``District``, ``State``
* ``Pincode`` (integer in returned data)
* ``Latitude`` and ``Longitude`` (float or ``None``)

If the pincode is well-formed but absent in the dataset, ``matching`` raises
``ValueError``.


2. Valid Pincode
################

Use ``isvalid`` to quickly check whether a pincode exists in the dataset.

.. code-block:: python

    indiapins.isvalid('110011')

    True

``isvalid`` returns ``False`` for correctly formatted but unknown pincodes (for
example ``"000000"``), and raises validation errors only for malformed input.

3. District by Pincode
######################

Use ``districtmatch`` when you only need district information.

.. code-block:: python

    indiapins.districtmatch('302005')

    'Jaipur'

If multiple district values exist for a pincode, they are returned as a
comma-separated string. If the pincode format is valid but absent in the
dataset, ``districtmatch`` raises ``ValueError``.

4. Coordinates of Pincode
#########################

Use ``coordinates`` to get office-level latitude/longitude mappings.

.. code-block:: python

    indiapins.coordinates('110011')

    {'Udyog Bhawan': {'latitude': '28.6111111', 'longitude': '77.2127500'},
    'Nirman Bhawan': {'latitude': '28.6108611', 'longitude': '77.2148611'}}

Notes:

* Entries with missing coordinates are excluded
* Latitude/longitude values are returned as strings for consistency
* Unknown but well-formed pincodes raise ``ValueError``

5. Geospatial Queries
#####################

Compute geodesic distance between two pincodes:

.. code-block:: python

    indiapins.distance("110001", "400001", metric="km")

Find nearest pincodes from a location:

.. code-block:: python

    indiapins.nearest_pincodes(28.6139, 77.2090, k=5)

Find neighboring pincodes from a source pincode:

.. code-block:: python

    indiapins.nearest_to_pincode("110001", k=10)

Find pincodes or delivery offices within a radius:

.. code-block:: python

    indiapins.pincodes_in_radius("110001", radius_km=5)
    indiapins.delivery_offices_in_radius((28.6139, 77.2090), radius_km=3)

Directional and matrix utilities:

.. code-block:: python

    indiapins.bearing("110001", "400001")
    indiapins.midpoint("110001", "400001")
    indiapins.distance_matrix(["110001", "400001", "560001"], metric="km")


Input Validation Examples
-------------------------

.. code-block:: python

    import indiapins

    # Valid input
    indiapins.matching("110001")

    # Invalid type -> TypeError
    indiapins.matching(110001)

    # Invalid length -> ValueError
    indiapins.matching("11001")

    # Invalid characters -> ValueError
    indiapins.matching("11A001")


Practical Patterns
------------------

Filter delivery-enabled offices:

.. code-block:: python

    delivery_only = [
        row for row in indiapins.matching("110001")
        if row["DeliveryStatus"] == "Delivery"
    ]

Extract coordinates into tuples for mapping tools:

.. code-block:: python

    points = {
        office: (float(v["latitude"]), float(v["longitude"]))
        for office, v in indiapins.coordinates("560001").items()
    }
