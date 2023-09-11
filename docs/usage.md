# Usage

To use indiapins in a project::

```
import indiapins
```

Exact Match
------------
To fetch all details of a pin code

```
indiapins.matching('110011')

[{'Name': 'Udyog Bhawan', 'BranchType': 'PO', 'DeliveryStatus': 'Non Delivery', 'Circle': 'Delhi', 'District': 'New Delhi', 'Division': 'New Delhi Central Division', 'Region': 'DivReportingCircle', 'Block': 'Delhi', 'State': 'Delhi', 'Country': 'India', 'Pincode': 110011, 'Latitude': 28.6111111, 'Longitude': '77.2127500'},
{'Name': 'Nirman Bhawan', 'BranchType': 'PO', 'DeliveryStatus': 'Delivery', 'Circle': 'Delhi', 'District': 'New Delhi', 'Division': 'New Delhi Central Division', 'Region': 'DivReportingCircle', 'Block': 'Delhi', 'State': 'Delhi', 'Country': 'India', 'Pincode': 110011, 'Latitude': 28.6108611, 'Longitude': '77.2148611'}]

```

Valid Pincode
--------------
```
indiapins.isvalid('110011')

True
```

District by Pincode
-------------------------
```
indiapins.districtmatch('302005')

'Jaipur'
```

Coordinates
-----------
```
indiapins.coordinates('110011')

{'Udyog Bhawan': {'latitude': '28.6111111', 'longitude': '77.2127500'},
'Nirman Bhawan': {'latitude': '28.6108611', 'longitude': '77.2148611'}}

```
