=====
Usage
=====

To use indiapins in a project::

    import indiapins

Exact Match
------------

.. code-block:: python

    >>> indiapins.matching('110011')

    [{'Name': 'Nirman Bhawan', 'BranchType': 'Sub Post Office', 'DeliveryStatus': 'Delivery', 'Circle': 'Delhi', 'District': 'Central Delhi', 'Division': 'New Delhi Central', 'Region': 'Delhi', 'Block': 'New Delhi', 'State': 'Delhi', 'Country': 'India', 'Pincode': '110011'}, 
    {'Name': 'South Avenue', 'BranchType': 'Sub Post Office', 'DeliveryStatus': 'Non-Delivery', 'Circle': 'Delhi', 'District': 'Central Delhi', 'Division': 'New Delhi Central', 'Region': 'Delhi', 'Block': 'New Delhi', 'State': 'Delhi', 'Country': 'India', 'Pincode': '110011'}, 
    {'Name': 'Udyog Bhawan', 'BranchType': 'Sub Post Office', 'DeliveryStatus': 'Non-Delivery', 'Circle': 'Delhi', 'District': 'Central Delhi', 'Division': 'New Delhi Central', 'Region': 'Delhi', 'Block': 'New Delhi', 'State': 'Delhi', 'Country': 'India', 'Pincode': '110011'}]


valid Pincode
--------------

.. code-block:: python

    >>> indiapins.isvalid('110011')

    True

District by Pincode
-------------------------

.. code-block:: python

    >>> indiapins.districtmatch('302005')

    'Jaipur'
