# Changelog

All notable changes to indiapins will be documented in this file.

## [1.0.5] - 2026-02-15

### Fixed
- **Critical Bug Fix:** Resolved KeyError that was preventing all functions from working correctly
- The bug was caused by inconsistent key casing in the previous data file
- All functions now work reliably across the entire dataset

### Added
- 8,436 new pincode records (+5.4% increase)
- Enhanced error handling for coordinates with missing data
- Better data validation during processing

### Changed
- Updated database from 157,191 to 165,627 total records
- Improved data consistency with standardized key formatting
- Enhanced coordinates function to automatically skip locations without valid GPS data
- Cleaner code implementation with better performance

### Data Quality
- 100% records have valid Pincode and Name fields
- 99.6% records include District information
- 92.7% records include GPS coordinates (Latitude/Longitude)
- All data uses consistent capitalized key format

### Data Structure Changes
- **Removed fields:** Block and Country (not available in new data source)
- **Available fields:** Circle, Region, Division, Name, Pincode, BranchType, DeliveryStatus, District, State, Latitude, Longitude

## [1.0.4] - 2025-01-26

### Added
- Added new pins

## [1.0.2] - 2024-08-10

### Added
- Added latest libs

## [1.0.1] - 2023-09-12

### Fixed
- Fix pins import error

## [0.1.7] - 2023-09-11

### Changed
- Update Pincode data to latest (Sept 2023)
- Added coordinates info with pins
- Fetch longitude and latitude of any pin

### Security
- Update security vulnerabilities

## [0.1.0] - 2021-07-27

### Added
- Initial release
- Match location with the pins
- Mark pin is valid or not
- Extract cities on basis of pins
