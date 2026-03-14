#!/usr/bin/env python

"""Exhaustive tests for `indiapins` package."""

import pytest

from indiapins import (
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


# ──────────────────────────────────────────────
# Expected record keys
# ──────────────────────────────────────────────
EXPECTED_KEYS = {
    "Circle", "Region", "Division", "Name", "Pincode",
    "BranchType", "DeliveryStatus", "District", "State",
    "Latitude", "Longitude",
}


# ──────────────────────────────────────────────
# Tests: matching()
# ──────────────────────────────────────────────
class TestMatching:
    """Tests for the matching() function."""

    def test_matching_returns_list(self, delhi_pincode):
        result = matching(delhi_pincode)
        assert isinstance(result, list)

    def test_matching_non_empty_for_valid_pincode(self, delhi_pincode):
        result = matching(delhi_pincode)
        assert len(result) > 0

    def test_matching_record_has_expected_keys(self, delhi_pincode):
        result = matching(delhi_pincode)
        for record in result:
            assert set(record.keys()) == EXPECTED_KEYS

    def test_matching_pincode_field_matches_input(self, delhi_pincode):
        result = matching(delhi_pincode)
        for record in result:
            assert str(record["Pincode"]) == delhi_pincode

    def test_matching_delhi(self, delhi_pincode):
        result = matching(delhi_pincode)
        assert len(result) > 0
        assert all(r["State"] == "DELHI" for r in result)

    def test_matching_mumbai(self, mumbai_pincode):
        result = matching(mumbai_pincode)
        assert len(result) > 0
        assert all(r["State"] == "MAHARASHTRA" for r in result)

    def test_matching_kolkata(self, kolkata_pincode):
        result = matching(kolkata_pincode)
        assert len(result) > 0
        assert all(r["State"] == "WEST BENGAL" for r in result)

    def test_matching_bangalore(self, bangalore_pincode):
        result = matching(bangalore_pincode)
        assert len(result) > 0
        assert all(r["State"] == "KARNATAKA" for r in result)

    def test_matching_chennai(self, chennai_pincode):
        result = matching(chennai_pincode)
        assert len(result) > 0
        assert all(r["State"] == "TAMIL NADU" for r in result)

    def test_matching_unknown_pincode_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid Pincode"):
            matching("000000")

    def test_matching_record_fields_types(self, delhi_pincode):
        result = matching(delhi_pincode)
        for record in result:
            assert isinstance(record["Name"], str)
            assert isinstance(record["Pincode"], int)
            assert isinstance(record["District"], str)
            assert isinstance(record["State"], str)
            assert isinstance(record["Circle"], str)

    def test_matching_multiple_results(self, delhi_pincode):
        """Delhi 110001 should have multiple post offices."""
        result = matching(delhi_pincode)
        assert len(result) > 1

    def test_matching_contains_known_post_office(self, delhi_pincode):
        result = matching(delhi_pincode)
        names = [r["Name"] for r in result]
        # "Baroda House SO" is a known post office in 110001
        assert "Baroda House SO" in names


# ──────────────────────────────────────────────
# Tests: isvalid()
# ──────────────────────────────────────────────
class TestIsValid:
    """Tests for the isvalid() function."""

    def test_valid_delhi_pincode(self, delhi_pincode):
        assert isvalid(delhi_pincode) is True

    def test_valid_mumbai_pincode(self, mumbai_pincode):
        assert isvalid(mumbai_pincode) is True

    def test_valid_kolkata_pincode(self, kolkata_pincode):
        assert isvalid(kolkata_pincode) is True

    def test_valid_bangalore_pincode(self, bangalore_pincode):
        assert isvalid(bangalore_pincode) is True

    def test_valid_chennai_pincode(self, chennai_pincode):
        assert isvalid(chennai_pincode) is True

    def test_invalid_pincode_returns_false(self):
        assert isvalid("000000") is False

    def test_returns_bool(self, delhi_pincode):
        result = isvalid(delhi_pincode)
        assert isinstance(result, bool)

    @pytest.mark.parametrize("pincode", [
        "110001", "400001", "700001", "560001", "600001",
        "500001", "380001", "226001", "302001", "411001",
    ])
    def test_major_city_pincodes_are_valid(self, pincode):
        assert isvalid(pincode) is True

    @pytest.mark.parametrize("pincode", [
        "000000", "999999", "000001", "999998",
    ])
    def test_unlikely_pincodes_are_invalid(self, pincode):
        assert isvalid(pincode) is False


# ──────────────────────────────────────────────
# Tests: districtmatch()
# ──────────────────────────────────────────────
class TestDistrictMatch:
    """Tests for the districtmatch() function."""

    def test_delhi_district(self, delhi_pincode):
        result = districtmatch(delhi_pincode)
        assert "NEW DELHI" in result

    def test_mumbai_district(self, mumbai_pincode):
        result = districtmatch(mumbai_pincode)
        assert "MUMBAI" in result

    def test_kolkata_district(self, kolkata_pincode):
        result = districtmatch(kolkata_pincode)
        assert "KOLKATA" in result or "CALCUTTA" in result

    def test_returns_string(self, delhi_pincode):
        result = districtmatch(delhi_pincode)
        assert isinstance(result, str)

    def test_non_empty_for_valid_pincode(self, delhi_pincode):
        result = districtmatch(delhi_pincode)
        assert len(result) > 0

    def test_invalid_pincode_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid Pincode"):
            districtmatch("000000")


# ──────────────────────────────────────────────
# Tests: coordinates()
# ──────────────────────────────────────────────
class TestCoordinates:
    """Tests for the coordinates() function."""

    def test_returns_dict(self, delhi_pincode):
        result = coordinates(delhi_pincode)
        assert isinstance(result, dict)

    def test_non_empty_for_valid_pincode(self, delhi_pincode):
        result = coordinates(delhi_pincode)
        assert len(result) > 0

    def test_coordinate_values_have_lat_lng(self, delhi_pincode):
        result = coordinates(delhi_pincode)
        for name, coord in result.items():
            assert "latitude" in coord
            assert "longitude" in coord

    def test_coordinate_values_are_strings(self, delhi_pincode):
        result = coordinates(delhi_pincode)
        for name, coord in result.items():
            assert isinstance(coord["latitude"], str)
            assert isinstance(coord["longitude"], str)

    def test_coordinate_values_are_numeric_strings(self, delhi_pincode):
        result = coordinates(delhi_pincode)
        for name, coord in result.items():
            float(coord["latitude"])  # should not raise
            float(coord["longitude"])  # should not raise

    def test_delhi_coordinates_in_range(self, delhi_pincode):
        """Delhi coordinates should be roughly around 28.6°N, 77.2°E."""
        result = coordinates(delhi_pincode)
        for name, coord in result.items():
            lat = float(coord["latitude"])
            lng = float(coord["longitude"])
            assert 28.0 < lat < 29.0, f"{name}: latitude {lat} out of range"
            assert 77.0 < lng < 78.0, f"{name}: longitude {lng} out of range"

    def test_mumbai_coordinates_in_range(self, mumbai_pincode):
        """Mumbai coordinates should be roughly around 18.9°N, 72.8°E."""
        result = coordinates(mumbai_pincode)
        for name, coord in result.items():
            lat = float(coord["latitude"])
            lng = float(coord["longitude"])
            assert 18.0 < lat < 20.0, f"{name}: latitude {lat} out of range"
            assert 72.0 < lng < 73.5, f"{name}: longitude {lng} out of range"

    def test_keys_are_post_office_names(self, delhi_pincode):
        result = coordinates(delhi_pincode)
        for name in result.keys():
            assert isinstance(name, str)
            assert len(name) > 0

    def test_unknown_pincode_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid Pincode"):
            coordinates("000000")


# ──────────────────────────────────────────────
# Tests: Input validation / _clean()
# ──────────────────────────────────────────────
class TestInputValidation:
    """Tests for input validation and the _clean() helper."""

    # --- Type errors ---
    def test_none_raises_type_error(self):
        with pytest.raises(TypeError, match="Invalid type"):
            matching(None)

    def test_integer_raises_type_error(self):
        with pytest.raises(TypeError, match="Invalid type"):
            matching(110001)

    def test_float_raises_type_error(self):
        with pytest.raises(TypeError, match="Invalid type"):
            matching(110001.0)

    def test_list_raises_type_error(self):
        with pytest.raises(TypeError, match="Invalid type"):
            matching(["110001"])

    def test_dict_raises_type_error(self):
        with pytest.raises(TypeError, match="Invalid type"):
            matching({"pincode": "110001"})

    def test_bool_raises_type_error(self):
        with pytest.raises(TypeError, match="Invalid type"):
            matching(True)

    def test_empty_string_raises_type_error(self):
        with pytest.raises(TypeError, match="Invalid type"):
            matching("")

    # --- Length errors ---
    def test_too_short_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid format"):
            matching("11000")

    def test_too_long_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid format"):
            matching("1100001")

    def test_single_digit_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid format"):
            matching("1")

    # --- Character errors ---
    def test_alphabetic_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid characters"):
            matching("abcdef")

    def test_mixed_alpha_numeric_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid characters"):
            matching("110a01")

    def test_special_chars_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid characters"):
            matching("110-01")

    def test_spaces_raises_value_error(self):
        with pytest.raises(ValueError, match="Invalid characters"):
            matching("110 01")

    # --- _clean() direct tests ---
    def test_clean_valid_pincode(self):
        assert _clean("110001") == "110001"

    def test_clean_wrong_length(self):
        with pytest.raises(ValueError, match="Invalid format"):
            _clean("12345")

    def test_clean_non_digits(self):
        with pytest.raises(ValueError, match="Invalid characters"):
            _clean("12345a")

    # --- Same validation for all public functions ---
    @pytest.mark.parametrize("func", [matching, isvalid, districtmatch, coordinates])
    def test_all_functions_reject_none(self, func):
        with pytest.raises(TypeError):
            func(None)

    @pytest.mark.parametrize("func", [matching, isvalid, districtmatch, coordinates])
    def test_all_functions_reject_integer(self, func):
        with pytest.raises(TypeError):
            func(110001)

    @pytest.mark.parametrize("func", [matching, isvalid, districtmatch, coordinates])
    def test_all_functions_reject_short_string(self, func):
        with pytest.raises(ValueError):
            func("12345")

    @pytest.mark.parametrize("func", [matching, isvalid, districtmatch, coordinates])
    def test_all_functions_reject_alpha_string(self, func):
        with pytest.raises(ValueError):
            func("abcdef")


# ──────────────────────────────────────────────
# Tests: Cross-state coverage
# ──────────────────────────────────────────────
class TestCrossStateCoverage:
    """Test pincodes from various states to ensure broad coverage."""

    @pytest.mark.parametrize("pincode,expected_state", [
        ("110001", "DELHI"),
        ("400001", "MAHARASHTRA"),
        ("700001", "WEST BENGAL"),
        ("560001", "KARNATAKA"),
        ("600001", "TAMIL NADU"),
        ("500001", "TELANGANA"),
        ("380001", "GUJARAT"),
        ("226001", "UTTAR PRADESH"),
        ("302001", "RAJASTHAN"),
        ("411001", "MAHARASHTRA"),
        ("160001", "CHANDIGARH"),
        ("781001", "ASSAM"),
        ("800001", "BIHAR"),
        ("751001", "ODISHA"),
        ("682001", "KERALA"),
    ])
    def test_pincode_maps_to_correct_state(self, pincode, expected_state):
        result = matching(pincode)
        assert len(result) > 0, f"No results for {pincode}"
        states = {r["State"] for r in result}
        assert expected_state in states, f"Expected {expected_state} for {pincode}, got {states}"

    @pytest.mark.parametrize("pincode,expected_district_substr", [
        ("110001", "NEW DELHI"),
        ("400001", "MUMBAI"),
        ("700001", "KOLKATA"),
        ("560001", "BENGALURU"),
        ("302001", "JAIPUR"),
    ])
    def test_pincode_maps_to_correct_district(self, pincode, expected_district_substr):
        result = districtmatch(pincode)
        assert expected_district_substr in result.upper()


# ──────────────────────────────────────────────
# Tests: Record field values
# ──────────────────────────────────────────────
class TestRecordFields:
    """Test individual fields in matching results."""

    def test_branch_type_values(self, delhi_pincode):
        result = matching(delhi_pincode)
        valid_types = {"BO", "SO", "HO", "PO"}
        for record in result:
            # BranchType should be one of known types
            bt = record["BranchType"]
            assert bt in valid_types, f"Unknown BranchType: {bt}"

    def test_delivery_status_values(self, delhi_pincode):
        result = matching(delhi_pincode)
        valid_statuses = {"Delivery", "Non Delivery"}
        for record in result:
            ds = record["DeliveryStatus"]
            assert ds in valid_statuses, f"Unknown status: {ds}"


class TestReverseLookup:
    def test_states_returns_sorted_unique_strings(self):
        result = states()
        assert isinstance(result, list)
        assert len(result) > 0
        assert result == sorted(set(result))
        assert all(isinstance(s, str) and s for s in result)

    def test_districts_in_state_case_insensitive_by_default(self):
        upper = districts_in_state("DELHI")
        lower = districts_in_state("delhi")
        mixed = districts_in_state("DeLhI")
        assert upper == lower == mixed
        assert len(lower) > 0

    def test_districts_in_state_case_sensitive_toggle(self):
        assert districts_in_state("delhi", case_sensitive=True) == []
        assert len(districts_in_state("DELHI", case_sensitive=True)) > 0

    def test_pincodes_in_state_case_insensitive_by_default(self):
        upper = pincodes_in_state("KARNATAKA")
        lower = pincodes_in_state("karnataka")
        assert upper == lower
        assert "560001" in lower

    def test_pincodes_in_district_case_insensitive_by_default(self):
        upper = pincodes_in_district("NEW DELHI")
        lower = pincodes_in_district("new delhi")
        assert upper == lower
        assert "110001" in lower

    def test_unknown_state_or_district_returns_empty_list(self):
        assert districts_in_state("NOT_A_STATE") == []
        assert pincodes_in_state("NOT_A_STATE") == []
        assert pincodes_in_district("NOT_A_DISTRICT") == []

    @pytest.mark.parametrize("bad_state", [None, 123, ["DELHI"], {"state": "DELHI"}])
    def test_malformed_state_type_raises_type_error(self, bad_state):
        with pytest.raises(TypeError):
            districts_in_state(bad_state)
        with pytest.raises(TypeError):
            pincodes_in_state(bad_state)

    @pytest.mark.parametrize("bad_district", [None, 123, ["NEW DELHI"], {"district": "NEW DELHI"}])
    def test_malformed_district_type_raises_type_error(self, bad_district):
        with pytest.raises(TypeError):
            pincodes_in_district(bad_district)

    @pytest.mark.parametrize("empty_value", ["", "   ", "\t"])
    def test_empty_state_or_district_raises_value_error(self, empty_value):
        with pytest.raises(ValueError):
            districts_in_state(empty_value)
        with pytest.raises(ValueError):
            pincodes_in_state(empty_value)
        with pytest.raises(ValueError):
            pincodes_in_district(empty_value)


class TestAdditionalCoreApis:
    def test_statematch_matches_matching_data(self, delhi_pincode):
        records = matching(delhi_pincode)
        expected = ", ".join(sorted({row["State"] for row in records}))
        assert statematch(delhi_pincode) == expected

    def test_division_circle_region_match_against_records(self, delhi_pincode):
        records = matching(delhi_pincode)
        expected_division = ", ".join(sorted({row["Division"] for row in records}))
        expected_circle = ", ".join(sorted({row["Circle"] for row in records}))
        expected_region = ", ".join(sorted({row["Region"] for row in records}))
        assert divisionmatch(delhi_pincode) == expected_division
        assert circlematch(delhi_pincode) == expected_circle
        assert regionmatch(delhi_pincode) == expected_region

    @pytest.mark.parametrize("func", [statematch, divisionmatch, circlematch, regionmatch])
    def test_admin_matchers_unknown_pincode_raise_value_error(self, func):
        with pytest.raises(ValueError, match="Invalid Pincode"):
            func("000000")

    def test_has_delivery_matches_underlying_records(self, delhi_pincode):
        records = matching(delhi_pincode)
        expected = any(row["DeliveryStatus"] == "Delivery" for row in records)
        assert has_delivery(delhi_pincode) is expected

    def test_delivery_offices_returns_delivery_only(self, delhi_pincode):
        offices = delivery_offices(delhi_pincode)
        assert isinstance(offices, list)
        assert len(offices) > 0
        assert all(row["DeliveryStatus"] == "Delivery" for row in offices)

    def test_offices_by_branch_type_case_insensitive_by_default(self, delhi_pincode):
        records = matching(delhi_pincode)
        branch_type = records[0]["BranchType"]
        lower = offices_by_branch_type(delhi_pincode, branch_type.lower())
        assert len(lower) > 0
        assert all(row["BranchType"] == branch_type for row in lower)

    def test_offices_by_branch_type_unknown_returns_empty(self, delhi_pincode):
        assert offices_by_branch_type(delhi_pincode, "ZZ") == []

    def test_offices_by_branch_type_malformed_input_raises(self, delhi_pincode):
        with pytest.raises(TypeError):
            offices_by_branch_type(delhi_pincode, None)
        with pytest.raises(ValueError):
            offices_by_branch_type(delhi_pincode, "  ")

    def test_pincodes_by_prefix_returns_unique_sorted(self, delhi_pincode):
        prefix = delhi_pincode[:2]
        result = pincodes_by_prefix(prefix)
        assert isinstance(result, list)
        assert result == sorted(set(result))
        assert delhi_pincode in result
        assert all(pin.startswith(prefix) for pin in result)

    @pytest.mark.parametrize("bad_prefix", [None, 11, "1", "12345", "AB", "11A"])
    def test_pincodes_by_prefix_malformed_raises(self, bad_prefix):
        with pytest.raises((TypeError, ValueError)):
            pincodes_by_prefix(bad_prefix)

    def test_isvalid_bulk_returns_bool_map(self, delhi_pincode):
        result = isvalid_bulk([delhi_pincode, "000000"])
        assert result[delhi_pincode] is True
        assert result["000000"] is False

    @pytest.mark.parametrize("bad_bulk", [None, "110001", [None], ["11001"], ["11A001"]])
    def test_isvalid_bulk_malformed_raises(self, bad_bulk):
        with pytest.raises((TypeError, ValueError)):
            isvalid_bulk(bad_bulk)

    def test_matching_bulk_returns_map(self, delhi_pincode, mumbai_pincode):
        result = matching_bulk([delhi_pincode, mumbai_pincode])
        assert isinstance(result, dict)
        assert len(result[delhi_pincode]) > 0
        assert len(result[mumbai_pincode]) > 0

    def test_matching_bulk_unknown_pincode_raises(self, delhi_pincode):
        with pytest.raises(ValueError, match="Invalid Pincode"):
            matching_bulk([delhi_pincode, "000000"])
