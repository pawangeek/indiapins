# Welcome to the indiapins documentation

## About

Indiapins is a Python package for resolving Indian pincodes to their associated
postal offices and administrative metadata. The packaged dataset is updated with
latest February 2026 data containing **165,627 pincode records** across India.

The library is designed for:

- Local/offline-friendly lookups (no API dependency)
- Fast access through a compact packaged data file
- Simple function-based usage for scripts and services

## Supported Operations

Currently supported operations:

- Validity of Pincode
- Get coordinates related to that Pincode
- Get all details of a pincode
- Get name of district by pincode
- Geodesic distance between pincodes
- Nearest pincodes from coordinates or source pincode
- Radius-based pincode and delivery-office discovery

## Input Rules (Important)

All pincode inputs must:

- Be passed as a Python string
- Be exactly 6 characters long
- Contain digits only

Malformed inputs raise explicit exceptions to help catch mistakes early.

## Quick Example

```python
import indiapins

records = indiapins.matching("110001")
exists = indiapins.isvalid("110001")
district = indiapins.districtmatch("110001")
coords = indiapins.coordinates("110001")
nearest = indiapins.nearest_to_pincode("110001", k=5)
```

## What's New in v1.1.0

- **Added geospatial APIs** powered by `geodistpy` (distance, nearest, radius, bearing, midpoint, matrix)
- **Expanded core API surface** with reverse lookups, admin matchers, bulk helpers, and delivery/branch filters
- **Standardized behavior contracts** for unknown vs malformed inputs and case-insensitive state/district matching by default

