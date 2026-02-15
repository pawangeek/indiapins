# Usage

To use indiapins in a project:

```python
import indiapins
```

## Available Functions

### Exact Match

Fetch all details of a pincode - returns a list of dictionaries containing complete information.

```python
indiapins.matching('110011')
```

**Returns:**
```python
[{'Name': 'Udyog Bhawan', 'BranchType': 'PO', 'DeliveryStatus': 'Non Delivery', 
  'Circle': 'Delhi', 'District': 'New Delhi', 'Division': 'New Delhi Central Division', 
  'Region': 'DivReportingCircle', 'State': 'Delhi', 'Pincode': 110011, 
  'Latitude': 28.6111111, 'Longitude': 77.2127500},
 {'Name': 'Nirman Bhawan', 'BranchType': 'PO', 'DeliveryStatus': 'Delivery', 
  'Circle': 'Delhi', 'District': 'New Delhi', 'Division': 'New Delhi Central Division', 
  'Region': 'DivReportingCircle', 'State': 'Delhi', 'Pincode': 110011, 
  'Latitude': 28.6108611, 'Longitude': 77.2148611'}]
```

### Valid Pincode

Check if a pincode is valid and exists in the database.

```python
indiapins.isvalid('110011')
```

**Returns:**
```python
True
```

### District by Pincode

Get the district name(s) for a given pincode.

```python
indiapins.districtmatch('302005')
```

**Returns:**
```python
'Jaipur'
```

### Coordinates

Fetch latitude and longitude coordinates for all locations with the given pincode.

```python
indiapins.coordinates('110011')
```

**Returns:**
```python
{'Udyog Bhawan': {'latitude': '28.6111111', 'longitude': '77.2127500'},
 'Nirman Bhawan': {'latitude': '28.6108611', 'longitude': '77.2148611'}}
```

**Note:** Locations without valid coordinates are automatically excluded from results.

## Data Format

Each pincode record contains the following fields:

- **Pincode** - 6-digit pincode (integer)
- **Name** - Office/branch name
- **BranchType** - Type of post office (BO, SO, PO, etc.)
- **DeliveryStatus** - Delivery or Non Delivery
- **District** - District name
- **State** - State name
- **Circle** - Postal circle name
- **Region** - Region name
- **Division** - Division name
- **Latitude** - Latitude coordinate (float or null)
- **Longitude** - Longitude coordinate (float or null)

**Note:** Block and Country fields are not available in the current dataset.

## Error Handling

All functions that accept pincodes will validate the input:

```python
# Pincode must be a string of 6 digits
indiapins.matching('123456')  # Valid
indiapins.matching(123456)     # Raises TypeError
indiapins.matching('12345')    # Raises ValueError
indiapins.matching('ABCDEF')   # Raises ValueError
```

## Database Statistics

- **Total Records:** 165,627 pincodes
- **Coverage:** All Indian states and union territories
- **Last Updated:** February 2026
- **Coordinates:** 92.7% of records include GPS coordinates
