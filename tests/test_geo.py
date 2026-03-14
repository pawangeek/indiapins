#!/usr/bin/env python

"""Tests for geospatial helper APIs."""

import pytest

from indiapins import (
    bearing,
    delivery_offices_in_radius,
    distance,
    distance_matrix,
    midpoint,
    nearest_pincodes,
    nearest_to_pincode,
    pincodes_in_radius,
)

try:
    import geodistpy  # noqa: F401
    GEODISTPY_AVAILABLE = True
except ImportError:  # pragma: no cover
    GEODISTPY_AVAILABLE = False


@pytest.mark.skipif(not GEODISTPY_AVAILABLE, reason="geodistpy is not installed")
class TestGeospatialFunctions:
    def test_distance_returns_positive_float(self, delhi_pincode, mumbai_pincode):
        value = distance(delhi_pincode, mumbai_pincode, metric="km")
        assert isinstance(value, float)
        assert value > 0

    def test_nearest_pincodes_returns_expected_shape(self):
        rows = nearest_pincodes(28.6139, 77.2090, k=3)
        assert isinstance(rows, list)
        assert len(rows) == 3
        assert all("pincode" in row and "distance" in row for row in rows)

    def test_nearest_to_pincode_excludes_source(self, delhi_pincode):
        rows = nearest_to_pincode(delhi_pincode, k=5)
        assert len(rows) == 5
        assert all(row["pincode"] != delhi_pincode for row in rows)

    def test_pincodes_in_radius_accepts_pincode_center(self, delhi_pincode):
        rows = pincodes_in_radius(delhi_pincode, radius_km=1)
        assert isinstance(rows, list)
        assert len(rows) > 0
        assert any(row["pincode"] == delhi_pincode for row in rows)

    def test_delivery_offices_in_radius_filters_delivery_only(self, delhi_pincode):
        rows = delivery_offices_in_radius(delhi_pincode, radius_km=2)
        assert isinstance(rows, list)
        assert len(rows) > 0
        assert all("name" in row and "distance" in row for row in rows)

    def test_bearing_in_degree_range(self, delhi_pincode, mumbai_pincode):
        value = bearing(delhi_pincode, mumbai_pincode)
        assert isinstance(value, float)
        assert 0.0 <= value < 360.0

    def test_midpoint_returns_lat_lon_tuple(self, delhi_pincode, mumbai_pincode):
        point = midpoint(delhi_pincode, mumbai_pincode)
        assert isinstance(point, tuple)
        assert len(point) == 2
        assert all(isinstance(v, float) for v in point)

    def test_distance_matrix_square_shape(
        self, delhi_pincode, mumbai_pincode, bangalore_pincode
    ):
        matrix = distance_matrix([delhi_pincode, mumbai_pincode, bangalore_pincode], metric="km")
        assert matrix.shape == (3, 3)
        assert float(matrix[0][0]) == 0.0

    def test_distance_unknown_pincode_raises_value_error(self, delhi_pincode):
        with pytest.raises(ValueError, match="Invalid Pincode"):
            distance(delhi_pincode, "000000", metric="km")

    def test_nearest_to_unknown_pincode_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid Pincode"):
            nearest_to_pincode("000000", k=5)

    def test_radius_with_unknown_pincode_center_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid Pincode"):
            pincodes_in_radius("000000", radius_km=2)
