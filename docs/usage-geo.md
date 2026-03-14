# Geospatial Usage

Use `indiapins` geospatial APIs when you need nearest-pincode queries, radius
searches, bearings, and distance analytics.

Geospatial helpers are powered by `geodistpy`.

## Available Geospatial Functions

### Distance between two pincodes

```python
indiapins.distance("110001", "400001", metric="km")
```

Returns a float distance in the selected metric (`meter`, `km`, `mile`, `nmi`).

### Nearest pincodes to a location

```python
indiapins.nearest_pincodes(28.6139, 77.2090, k=5)
```

Returns a list of dictionaries:

```python
[{"pincode": "110001", "distance": 0.72}, {"pincode": "110002", "distance": 1.86}]
```

### Nearest pincodes from a pincode

```python
indiapins.nearest_to_pincode("110001", k=10)
```

Returns nearest neighboring pincodes (excluding the source pincode).

### Pincodes within a radius

Center can be either `(lat, lon)` or a pincode string.

```python
indiapins.pincodes_in_radius((28.6139, 77.2090), radius_km=5)
indiapins.pincodes_in_radius("110001", radius_km=5)
```

Returns:

```python
[{"pincode": "...", "distance": ...}]
```

### Delivery offices within a radius

```python
indiapins.delivery_offices_in_radius("110001", radius_km=3)
```

Returns delivery-enabled offices only, each with:

- `name`
- `pincode`
- `district`
- `state`
- `latitude`
- `longitude`
- `distance`

### Bearing and midpoint between pincodes

```python
indiapins.bearing("110001", "400001")
indiapins.midpoint("110001", "400001")
```

- `bearing()` returns angle in degrees (`0` to `<360`)
- `midpoint()` returns `(latitude, longitude)` tuple

### Distance matrix for multiple pincodes

```python
matrix = indiapins.distance_matrix(["110001", "400001", "560001"], metric="km")
```

Returns a pairwise distance matrix (`numpy.ndarray`) in the requested metric.

## Input and Validation Rules

### Pincode-based inputs

Functions that accept pincodes validate them as:

- non-empty string
- length exactly 6
- digits only (`0-9`)

### Numeric inputs

- `k` must be a positive integer
- `radius_km` must be a positive number
- `metric` must be one of: `meter`, `km`, `mile`, `nmi`

### Missing coordinates

If a pincode has no usable coordinates, geospatial methods raise `ValueError`.
Internally, `indiapins` also tolerates coordinate rows stored as DMS-like text.

## Practical Examples

### Serviceability check around a branch

```python
serviceable = indiapins.pincodes_in_radius("560001", radius_km=10)
```

### Nearby delivery offices for dispatch

```python
offices = indiapins.delivery_offices_in_radius((12.9716, 77.5946), radius_km=5)
```

### Distance matrix for routing model input

```python
pins = ["110001", "400001", "560001", "600001"]
dm = indiapins.distance_matrix(pins, metric="km")
```
