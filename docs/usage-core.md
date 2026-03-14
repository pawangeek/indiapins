# Core Usage

Use `indiapins` core APIs for fast, local pincode lookups without external API calls.

## Basic import

```python
import indiapins
```

All core pincode functions accept a pincode string in exactly 6-digit format
(for example, `"110001"`).

## Core Functions

### Exact Match

Fetch all records for a pincode. This is the most detailed API and returns a
list of dictionaries, one dictionary per matching office/branch.

```python
indiapins.matching("110011")
```

**Returns:**

```python
[{"Name": "Udyog Bhawan", "BranchType": "PO", "DeliveryStatus": "Non Delivery",
  "Circle": "Delhi", "District": "New Delhi", "Division": "New Delhi Central Division",
  "Region": "DivReportingCircle", "State": "Delhi", "Pincode": 110011,
  "Latitude": 28.6111111, "Longitude": 77.2127500},
 {"Name": "Nirman Bhawan", "BranchType": "PO", "DeliveryStatus": "Delivery",
  "Circle": "Delhi", "District": "New Delhi", "Division": "New Delhi Central Division",
  "Region": "DivReportingCircle", "State": "Delhi", "Pincode": 110011,
  "Latitude": 28.6108611, "Longitude": 77.2148611}]
```

Each dictionary contains:

- `Name` (str)
- `BranchType` (str, usually `BO`, `SO`, `HO`, `PO`)
- `DeliveryStatus` (str)
- `Circle`, `Region`, `Division`, `District`, `State` (str)
- `Pincode` (int)
- `Latitude`, `Longitude` (float or `None`)

If the pincode format is valid but not present in data, `matching()` raises
`ValueError`.

### Valid Pincode

Check if a pincode exists in the packaged dataset.

```python
indiapins.isvalid("110011")
```

**Returns:**

```python
True
```

Behavior notes:

- Returns `True` for known pincodes.
- Returns `False` for unknown but well-formed pincodes (for example `"000000"`).
- Raises validation errors only for malformed input.

### District by Pincode

Get district name(s) for a pincode.

```python
indiapins.districtmatch("302005")
```

**Returns:**

```python
"Jaipur"
```

Behavior notes:

- Returns a string.
- If multiple district values exist in records, they are joined as a comma-separated string.
- Raises `ValueError` when pincode format is valid but no matching records exist.

### Coordinates

Fetch latitude and longitude values for each office mapped to the pincode.

```python
indiapins.coordinates("110011")
```

**Returns:**

```python
{"Udyog Bhawan": {"latitude": "28.6111111", "longitude": "77.2127500"},
 "Nirman Bhawan": {"latitude": "28.6108611", "longitude": "77.2148611"}}
```

Behavior notes:

- Returns a dictionary keyed by office name.
- `latitude` and `longitude` values are strings in the returned payload.
- Locations without valid coordinates are excluded automatically.
- Unknown but well-formed pincodes raise `ValueError`.

### Reverse Lookup by State/District

Use reverse-lookup helpers when you start from a state or district value.

```python
indiapins.states()
indiapins.districts_in_state("delhi")
indiapins.pincodes_in_state("karnataka")
indiapins.pincodes_in_district("new delhi")
```

Behavior notes:

- `states()` returns a sorted unique list of state names from the dataset.
- State and district comparisons are case-insensitive by default.
- You can enable exact matching with `case_sensitive=True`.
- Unknown but well-formed state/district inputs return `[]`.

### Additional Core Helpers

```python
indiapins.statematch("110001")
indiapins.divisionmatch("110001")
indiapins.circlematch("110001")
indiapins.regionmatch("110001")
indiapins.has_delivery("110001")
indiapins.delivery_offices("110001")
indiapins.offices_by_branch_type("110001", "so")
indiapins.pincodes_by_prefix("11")
indiapins.isvalid_bulk(["110001", "000000"])
indiapins.matching_bulk(["110001", "400001"])
```

Behavior notes:

- `statematch`, `divisionmatch`, `circlematch`, and `regionmatch` mirror `districtmatch` output behavior.
- `has_delivery` returns `True` if at least one delivery-enabled office exists for the pincode.
- `delivery_offices` and `offices_by_branch_type` return filtered record lists.
- `offices_by_branch_type` is case-insensitive by default.
- `pincodes_by_prefix` accepts numeric prefixes of length 2 to 4.
- `isvalid_bulk` returns `{pincode: bool}`.
- `matching_bulk` returns `{pincode: [records...]}` and raises for unknown but well-formed pincodes.

## Validation Rules

Pincode lookup functions (`matching`, `isvalid`, `districtmatch`, `coordinates`,
`nearest_to_pincode`) apply the same pincode validation:

- Pincode must be a non-empty string
- Length must be exactly 6
- Characters must be digits only (`0-9`)

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

Notes:

- `Pincode` is returned as integer in record dictionaries.
- Block and Country fields are not available in the current dataset.

## Error Handling

All functions that accept pincodes validate the input:

```python
# Pincode must be a string of 6 digits
indiapins.matching("123456")   # Valid
indiapins.matching(123456)     # Raises TypeError
indiapins.matching("12345")    # Raises ValueError
indiapins.matching("ABCDEF")   # Raises ValueError
```

Typical error cases:

- `TypeError`: `None`, integers, lists, dicts, or empty string
- `ValueError`: wrong length, non-digit characters, or unknown well-formed pincodes

Reverse-lookup helpers validate textual inputs:

- `TypeError`: non-string `state`/`district` input
- `ValueError`: empty string after trimming whitespace

## Database Statistics

- **Total Records:** 165,627 pincodes
- **Coverage:** All Indian states and union territories
- **Last Updated:** February 2026
- **Coordinates:** Most records include GPS coordinates; rows missing either
  value are skipped by `coordinates()`

## Practical Examples

### Filter offices by delivery status

```python
results = indiapins.matching("110001")
delivery_offices = [r for r in results if r["DeliveryStatus"] == "Delivery"]
```

### Convert coordinate strings to float tuples

```python
office_points = {
    office: (float(v["latitude"]), float(v["longitude"]))
    for office, v in indiapins.coordinates("560001").items()
}
```

### Defensive lookup wrapper

```python
def lookup_pincode(pin: str) -> dict:
    if not indiapins.isvalid(pin):
        return {"valid": False, "records": []}
    return {"valid": True, "records": indiapins.matching(pin)}
```
