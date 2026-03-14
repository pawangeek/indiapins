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
```

## What's New in v1.0.6

- **Updated all dependencies** to latest versions
- **Dropped Python 3.9 support**, added **Python 3.14 support**
- **Improved CI pipeline** with updated Python version matrix

