"""Top-level package for indiapins."""

__author__ = """Pawan Kumar Jain"""
__email__ = "pawanjain.432@gmail.com"
__version__ = "1.1.0"

from .core import (
    _clean,
    circlematch,
    coordinates,
    delivery_offices,
    districtmatch,
    districts_in_state,
    divisionmatch,
    has_delivery,
    isvalid,
    isvalid_bulk,
    matching,
    matching_bulk,
    offices_by_branch_type,
    pincodes_in_district,
    pincodes_in_state,
    pincodes_by_prefix,
    regionmatch,
    statematch,
    states,
)
from .geo import (
    bearing,
    delivery_offices_in_radius,
    distance,
    distance_matrix,
    midpoint,
    nearest_pincodes,
    nearest_to_pincode,
    pincodes_in_radius,
)

__all__ = [
    "_clean",
    "matching",
    "isvalid",
    "isvalid_bulk",
    "districtmatch",
    "statematch",
    "divisionmatch",
    "circlematch",
    "regionmatch",
    "coordinates",
    "has_delivery",
    "delivery_offices",
    "states",
    "districts_in_state",
    "pincodes_in_state",
    "pincodes_in_district",
    "offices_by_branch_type",
    "pincodes_by_prefix",
    "matching_bulk",
    "distance",
    "nearest_pincodes",
    "nearest_to_pincode",
    "pincodes_in_radius",
    "delivery_offices_in_radius",
    "bearing",
    "midpoint",
    "distance_matrix",
]
