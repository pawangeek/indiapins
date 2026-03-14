# Usage

`indiapins` usage is now split into separate guides for clearer documentation:

- **Core Usage** (`usage-core.md`): pincode lookup, validation, district, and coordinates
- **Geospatial Usage** (`usage-geo.md`): distance, nearest, radius, bearing, midpoint, and matrix APIs

## Quick Start

```python
import indiapins

records = indiapins.matching("110001")
nearest = indiapins.nearest_to_pincode("110001", k=5)
```

## Read Next

- Go to **Core Usage** for non-geospatial APIs and validation behavior.
- Go to **Geospatial Usage** for distance and proximity APIs powered by `geodistpy`.
