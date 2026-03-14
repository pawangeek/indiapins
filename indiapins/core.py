"""Core pincode lookup functions and dataset loading."""

import bz2
import json
import os
import re
import sys

_valid_zipcode_length = 6
_digits = re.compile(r"[^\d]")
_unknown_pincode_error = "Invalid Pincode, pincode not in database"

if sys.version_info >= (3, 0):
    bz2_open = bz2.open
else:
    raise TypeError("Indiapins supported only on Python 3")


def _clean_zipcode(fn):
    def decorator(zipcode, *args, **kwargs):
        if not zipcode or not isinstance(zipcode, str):
            raise TypeError("Invalid type, pincode must be a string.")

        return fn(
            _clean(zipcode, _valid_zipcode_length), *args, **kwargs
        )

    return decorator


def _clean(zipcode, valid_length=_valid_zipcode_length):
    """Assumes pincode is of type `str`."""
    if len(zipcode) != valid_length:
        raise ValueError(
            'Invalid format, pincode must be of the format: "######"'
        )

    if bool(_digits.search(zipcode)):
        raise ValueError("Invalid characters, pincode may only contain digits")

    return zipcode


def _clean_region_value(value, field_name):
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string.")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string.")
    return normalized


def _normalize_for_compare(value, case_sensitive=False):
    if not isinstance(value, str):
        return None
    normalized = value.strip()
    if not normalized:
        return None
    return normalized if case_sensitive else normalized.lower()


def _clean_prefix(prefix):
    if not isinstance(prefix, str):
        raise TypeError("prefix must be a string.")
    clean_prefix = prefix.strip()
    if not clean_prefix:
        raise ValueError("prefix must be a non-empty string.")
    if not clean_prefix.isdigit():
        raise ValueError("prefix may only contain digits.")
    if len(clean_prefix) < 2 or len(clean_prefix) > 4:
        raise ValueError("prefix length must be between 2 and 4 digits.")
    return clean_prefix


def _clean_bulk_pincodes(pincodes):
    if not isinstance(pincodes, (list, tuple)):
        raise TypeError("pincodes must be a list or tuple of pincode strings.")
    clean_pincodes = []
    for zipcode in pincodes:
        if not zipcode or not isinstance(zipcode, str):
            raise TypeError("Invalid type, pincode must be a string.")
        clean_pincodes.append(_clean(zipcode, _valid_zipcode_length))
    return clean_pincodes


def _values_for_pincode(zipcode, key, zips):
    values = sorted(
        {
            value.strip()
            for z in zips
            if str(z["Pincode"]) == zipcode
            for value in [z.get(key)]
            if isinstance(value, str) and value.strip()
        }
    )
    if len(values) == 0:
        raise ValueError(_unknown_pincode_error)
    return values


def _resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS.
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


_zips_json = _resource_path(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "pins.json.bz2")
)
with bz2_open(_zips_json, "rt") as f:
    _zips = [json.loads(line) for i, line in enumerate(f)]


@_clean_zipcode
def matching(zipcode, zips=None):
    """Retrieve zipcode dict for provided pincode."""
    if zips is None:
        zips = _zips
    rows = [z for z in zips if str(z["Pincode"]) == zipcode]
    if len(rows) == 0:
        raise ValueError(_unknown_pincode_error)
    return rows


@_clean_zipcode
def isvalid(zipcode):
    return bool([z for z in _zips if str(z["Pincode"]) == zipcode])


@_clean_zipcode
def districtmatch(zipcode, zips=None):
    if zips is None:
        zips = _zips

    districts = _values_for_pincode(zipcode, "District", zips)
    return ", ".join(districts)


@_clean_zipcode
def coordinates(zipcode):
    match_list = matching(zipcode)
    coordinates_dict = {}

    for matches in match_list:
        name = matches["Name"]
        latitude = matches["Latitude"]
        longitude = matches["Longitude"]
        if latitude is not None and longitude is not None:
            coordinates_dict[name] = {"latitude": str(latitude), "longitude": str(longitude)}

    return coordinates_dict


def states(zips=None):
    if zips is None:
        zips = _zips
    return sorted(
        {
            state.strip()
            for z in zips
            for state in [z.get("State")]
            if isinstance(state, str) and state.strip()
        }
    )


def districts_in_state(state, case_sensitive=False, zips=None):
    if zips is None:
        zips = _zips

    clean_state = _clean_region_value(state, "state")
    match_state = _normalize_for_compare(clean_state, case_sensitive=case_sensitive)
    districts = {
        z["District"].strip()
        for z in zips
        if _normalize_for_compare(z.get("State"), case_sensitive=case_sensitive) == match_state
        and isinstance(z.get("District"), str)
        and z["District"].strip()
    }
    return sorted(districts)


def pincodes_in_state(state, case_sensitive=False, zips=None):
    if zips is None:
        zips = _zips

    clean_state = _clean_region_value(state, "state")
    match_state = _normalize_for_compare(clean_state, case_sensitive=case_sensitive)
    pincodes = {
        str(z["Pincode"])
        for z in zips
        if _normalize_for_compare(z.get("State"), case_sensitive=case_sensitive) == match_state
    }
    return sorted(pincodes)


def pincodes_in_district(district, case_sensitive=False, zips=None):
    if zips is None:
        zips = _zips

    clean_district = _clean_region_value(district, "district")
    match_district = _normalize_for_compare(clean_district, case_sensitive=case_sensitive)
    pincodes = {
        str(z["Pincode"])
        for z in zips
        if _normalize_for_compare(z.get("District"), case_sensitive=case_sensitive)
        == match_district
    }
    return sorted(pincodes)


@_clean_zipcode
def statematch(zipcode, zips=None):
    if zips is None:
        zips = _zips
    states_for_pin = _values_for_pincode(zipcode, "State", zips)
    return ", ".join(states_for_pin)


@_clean_zipcode
def divisionmatch(zipcode, zips=None):
    if zips is None:
        zips = _zips
    divisions = _values_for_pincode(zipcode, "Division", zips)
    return ", ".join(divisions)


@_clean_zipcode
def circlematch(zipcode, zips=None):
    if zips is None:
        zips = _zips
    circles = _values_for_pincode(zipcode, "Circle", zips)
    return ", ".join(circles)


@_clean_zipcode
def regionmatch(zipcode, zips=None):
    if zips is None:
        zips = _zips
    regions = _values_for_pincode(zipcode, "Region", zips)
    return ", ".join(regions)


@_clean_zipcode
def has_delivery(zipcode, zips=None):
    if zips is None:
        zips = _zips
    rows = matching(zipcode, zips=zips)
    return any(row["DeliveryStatus"] == "Delivery" for row in rows)


@_clean_zipcode
def delivery_offices(zipcode, zips=None):
    if zips is None:
        zips = _zips
    rows = matching(zipcode, zips=zips)
    return [row for row in rows if row["DeliveryStatus"] == "Delivery"]


@_clean_zipcode
def offices_by_branch_type(zipcode, branch_type, case_sensitive=False, zips=None):
    if zips is None:
        zips = _zips
    clean_branch_type = _clean_region_value(branch_type, "branch_type")
    match_type = _normalize_for_compare(clean_branch_type, case_sensitive=case_sensitive)
    rows = matching(zipcode, zips=zips)
    return [
        row for row in rows
        if _normalize_for_compare(row["BranchType"], case_sensitive=case_sensitive)
        == match_type
    ]


def pincodes_by_prefix(prefix, zips=None):
    if zips is None:
        zips = _zips
    clean_prefix = _clean_prefix(prefix)
    return sorted({str(row["Pincode"]) for row in zips if str(row["Pincode"]).startswith(clean_prefix)})


def isvalid_bulk(pincodes):
    clean_pincodes = _clean_bulk_pincodes(pincodes)
    return {zipcode: isvalid(zipcode) for zipcode in clean_pincodes}


def matching_bulk(pincodes):
    clean_pincodes = _clean_bulk_pincodes(pincodes)
    return {zipcode: matching(zipcode) for zipcode in clean_pincodes}
