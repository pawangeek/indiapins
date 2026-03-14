# Changelog

All notable changes to `indiapins` are documented in this file.

## [1.1.0] - 2026-03-14

### Added
- Added geospatial APIs powered by `geodistpy`: `distance`, `nearest_pincodes`, `nearest_to_pincode`, `pincodes_in_radius`, `delivery_offices_in_radius`, `bearing`, `midpoint`, and `distance_matrix`
- Added centroid caching for pincode-level geospatial queries to speed up repeated nearest/radius lookups
- Added reverse-lookup core APIs: `states`, `districts_in_state`, `pincodes_in_state`, and `pincodes_in_district`
- Added core helpers: `statematch`, `divisionmatch`, `circlematch`, `regionmatch`, `has_delivery`, `delivery_offices`, `offices_by_branch_type`, `pincodes_by_prefix`, `isvalid_bulk`, and `matching_bulk`

### Changed
- Added `geodistpy` as a runtime dependency for geodesic calculations
- Updated README and usage documentation with geospatial examples and API behavior
- Split docs usage into separate core and geospatial guides for easier navigation
- Standardized unknown-but-well-formed pincode handling: lookup/query APIs now raise `ValueError`, while `isvalid` continues to return `False`
- Standardized state/district comparisons to be case-insensitive by default, with optional `case_sensitive=True` for exact matching
- Dropped Python 3.10 support

## [1.0.6] - 2026-02-21

### Changed
- Updated dependencies to latest versions (`click 8.3.1`, `pytest 9.0.2`, `flake8 7.3.0`, `coverage 7.13.4`, `twine 6.2.0`, `mkdocs 1.6.1`)
- Dropped Python 3.9 support
- Added Python 3.14 support

## [1.0.5] - 2026-02-15

### Fixed
- Resolved a critical `KeyError` that prevented all functions from working correctly
- The bug was caused by inconsistent key casing in the previous data file
- All functions now work reliably across the entire dataset

### Added
- 8,436 new pincode records (+5.4% increase)
- Enhanced error handling for coordinates with missing data
- Better data validation during processing

### Changed
- Updated database from 157,191 to 165,627 total records
- Improved data consistency with standardized key formatting
- Enhanced `coordinates` to automatically skip locations without valid GPS data
- Cleaner code implementation with better performance

### Data Quality
- 100% records have valid Pincode and Name fields
- 99.6% records include District information
- 92.7% records include GPS coordinates (Latitude/Longitude)
- All data uses a consistent capitalized key format

### Data Structure Changes
- **Removed fields:** Block and Country (not available in new data source)
- **Available fields:** `Circle`, `Region`, `Division`, `Name`, `Pincode`, `BranchType`, `DeliveryStatus`, `District`, `State`, `Latitude`, `Longitude`

## [1.0.4] - 2025-01-26

### Added
- Added new pincode data

## [1.0.2] - 2024-08-10

### Added
- Updated library dependencies

## [1.0.1] - 2023-09-12

### Fixed
- Fixed pin data import error

## [0.1.7] - 2023-09-11

### Changed
- Update Pincode data to latest (Sept 2023)
- Added coordinates info with pincode records
- Added ability to fetch latitude and longitude for any pin

### Security
- Updated vulnerable dependencies

## [0.1.0] - 2021-07-27

### Added
- Initial release
- Match locations with pincodes
- Check whether a pincode is valid
- Extract cities on the basis of pincodes
