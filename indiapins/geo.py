"""Geospatial helpers built on top of pincode data."""

import importlib
import re

from .core import (
    _clean,
    _clean_zipcode,
    _unknown_pincode_error,
    _valid_zipcode_length,
    _zips,
)

_valid_metrics = {"meter", "km", "mile", "nmi"}
_dms_pattern = re.compile(
    r"""^\s*([+-]?\d+(?:\.\d+)?)\s*[°ºd]?\s*
    (?:(\d+(?:\.\d+)?)\s*['’m]?\s*)?
    (?:(\d+(?:\.\d+)?)\s*["”s]?\s*)?
    ([NSEW])?\s*$""",
    re.IGNORECASE | re.VERBOSE,
)

_PINCODE_CENTROID_CACHE = None
_DELIVERY_POINTS_CACHE = None
_geo_bearing = None
_geo_geodist = None
_geo_geodist_matrix = None
_geo_geodesic_knn = None
_geo_midpoint = None
_geo_point_in_radius = None


def _require_geodistpy():
    global _geo_bearing
    global _geo_geodist
    global _geo_geodist_matrix
    global _geo_geodesic_knn
    global _geo_midpoint
    global _geo_point_in_radius

    if _geo_geodist is not None:
        return

    try:
        module = importlib.import_module("geodistpy")
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "geodistpy is required for geo distance features. "
            "Install it with `pip install geodistpy`."
        ) from exc

    _geo_bearing = module.bearing
    _geo_geodist = module.geodist
    _geo_geodist_matrix = module.geodist_matrix
    _geo_geodesic_knn = module.geodesic_knn
    _geo_midpoint = module.midpoint
    _geo_point_in_radius = module.point_in_radius


def _validate_metric(metric):
    if metric not in _valid_metrics:
        raise ValueError("Invalid metric. Choose one of: meter, km, mile, nmi.")
    return metric


def _validate_k(k):
    if not isinstance(k, int) or k <= 0:
        raise ValueError("k must be a positive integer.")
    return k


def _validate_radius(radius_km):
    if not isinstance(radius_km, (int, float)) or radius_km <= 0:
        raise ValueError("radius_km must be a positive number.")
    return float(radius_km)


def _to_decimal_coordinate(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if not isinstance(value, str):
        return None

    candidate = value.strip()
    if not candidate:
        return None

    try:
        return float(candidate)
    except ValueError:
        pass

    match = _dms_pattern.match(candidate)
    if not match:
        return None

    deg = float(match.group(1))
    mins = float(match.group(2)) if match.group(2) is not None else 0.0
    secs = float(match.group(3)) if match.group(3) is not None else 0.0
    direction = match.group(4).upper() if match.group(4) else ""

    sign = -1.0 if deg < 0 else 1.0
    abs_deg = abs(deg) + mins / 60.0 + secs / 3600.0

    if direction in {"S", "W"}:
        sign = -1.0
    elif direction in {"N", "E"}:
        sign = 1.0

    return sign * abs_deg


def _build_pincode_centroids():
    global _PINCODE_CENTROID_CACHE

    if _PINCODE_CENTROID_CACHE is not None:
        return _PINCODE_CENTROID_CACHE

    grouped = {}
    for row in _zips:
        lat = _to_decimal_coordinate(row.get("Latitude"))
        lon = _to_decimal_coordinate(row.get("Longitude"))
        if lat is None or lon is None:
            continue
        pincode = str(row["Pincode"])
        grouped.setdefault(pincode, []).append((lat, lon))

    centroid_by_pincode = {}
    pincode_list = []
    centroid_points = []
    for pincode, coords in grouped.items():
        lat = sum(c[0] for c in coords) / len(coords)
        lon = sum(c[1] for c in coords) / len(coords)
        point = (lat, lon)
        centroid_by_pincode[pincode] = point
        pincode_list.append(pincode)
        centroid_points.append(point)

    _PINCODE_CENTROID_CACHE = (centroid_by_pincode, pincode_list, centroid_points)
    return _PINCODE_CENTROID_CACHE


def _build_delivery_points():
    global _DELIVERY_POINTS_CACHE

    if _DELIVERY_POINTS_CACHE is not None:
        return _DELIVERY_POINTS_CACHE

    records = []
    points = []
    for row in _zips:
        lat = _to_decimal_coordinate(row.get("Latitude"))
        lon = _to_decimal_coordinate(row.get("Longitude"))
        if lat is None or lon is None:
            continue
        if row.get("DeliveryStatus") != "Delivery":
            continue
        point = (lat, lon)
        points.append(point)
        records.append((row, point))

    _DELIVERY_POINTS_CACHE = (records, points)
    return _DELIVERY_POINTS_CACHE


def _pincode_point(zipcode):
    clean_zip = _clean(zipcode, _valid_zipcode_length)
    centroid_by_pincode, _, _ = _build_pincode_centroids()
    point = centroid_by_pincode.get(clean_zip)
    if point is None:
        raise ValueError(f"{_unknown_pincode_error} or has no coordinates")
    return point


def _normalize_center(center):
    if isinstance(center, str):
        return _pincode_point(center)

    if (
        isinstance(center, (tuple, list))
        and len(center) == 2
        and isinstance(center[0], (int, float))
        and isinstance(center[1], (int, float))
    ):
        return (float(center[0]), float(center[1]))

    raise TypeError(
        "center must be either a pincode string or a (latitude, longitude) tuple/list."
    )


def _rows_from_indexes(indexes, distances, pincode_list):
    rows = []
    for idx, dist in zip(indexes, distances):
        pincode = pincode_list[int(idx)]
        rows.append({"pincode": pincode, "distance": float(dist)})
    rows.sort(key=lambda x: x["distance"])
    return rows


def distance(pin1, pin2, metric="km"):
    _require_geodistpy()
    metric = _validate_metric(metric)
    point1 = _pincode_point(pin1)
    point2 = _pincode_point(pin2)
    return float(_geo_geodist(point1, point2, metric=metric))


def nearest_pincodes(lat, lon, k=5, metric="km"):
    _require_geodistpy()
    k = _validate_k(k)
    metric = _validate_metric(metric)
    center = (float(lat), float(lon))
    _, pincode_list, centroid_points = _build_pincode_centroids()
    indexes, distances = _geo_geodesic_knn(center, centroid_points, k=k, metric=metric)
    return _rows_from_indexes(indexes, distances, pincode_list)


@_clean_zipcode
def nearest_to_pincode(zipcode, k=10, metric="km"):
    _require_geodistpy()
    k = _validate_k(k)
    metric = _validate_metric(metric)
    center = _pincode_point(zipcode)
    _, pincode_list, centroid_points = _build_pincode_centroids()

    max_k = min(len(centroid_points), k + 1)
    indexes, distances = _geo_geodesic_knn(center, centroid_points, k=max_k, metric=metric)
    rows = _rows_from_indexes(indexes, distances, pincode_list)
    rows = [r for r in rows if r["pincode"] != zipcode]
    return rows[:k]


def pincodes_in_radius(center, radius_km):
    _require_geodistpy()
    radius_km = _validate_radius(radius_km)
    center_point = _normalize_center(center)
    _, pincode_list, centroid_points = _build_pincode_centroids()
    indexes, distances = _geo_point_in_radius(center_point, centroid_points, radius_km, metric="km")
    return _rows_from_indexes(indexes, distances, pincode_list)


def delivery_offices_in_radius(center, radius_km):
    _require_geodistpy()
    radius_km = _validate_radius(radius_km)
    center_point = _normalize_center(center)
    records, delivery_points = _build_delivery_points()
    indexes, distances = _geo_point_in_radius(center_point, delivery_points, radius_km, metric="km")
    rows = []
    for idx, dist in zip(indexes, distances):
        row, point = records[int(idx)]
        rows.append(
            {
                "name": row["Name"],
                "pincode": str(row["Pincode"]),
                "district": row["District"],
                "state": row["State"],
                "latitude": point[0],
                "longitude": point[1],
                "distance": float(dist),
            }
        )
    rows.sort(key=lambda x: x["distance"])
    return rows


def bearing(pin1, pin2):
    _require_geodistpy()
    point1 = _pincode_point(pin1)
    point2 = _pincode_point(pin2)
    return float(_geo_bearing(point1, point2))


def midpoint(pin1, pin2):
    _require_geodistpy()
    point1 = _pincode_point(pin1)
    point2 = _pincode_point(pin2)
    lat, lon = _geo_midpoint(point1, point2)
    return (float(lat), float(lon))


def distance_matrix(pincodes, metric="km"):
    _require_geodistpy()
    metric = _validate_metric(metric)

    if not isinstance(pincodes, (list, tuple)) or len(pincodes) == 0:
        raise ValueError("pincodes must be a non-empty list or tuple of strings.")

    points = []
    for zipcode in pincodes:
        if not isinstance(zipcode, str):
            raise TypeError("All pincodes must be strings.")
        points.append(_pincode_point(zipcode))

    return _geo_geodist_matrix(points, metric=metric)
