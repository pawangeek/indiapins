"""Shared pytest fixtures for indiapins test suite."""

import pytest


@pytest.fixture
def delhi_pincode():
    return "110001"


@pytest.fixture
def mumbai_pincode():
    return "400001"


@pytest.fixture
def kolkata_pincode():
    return "700001"


@pytest.fixture
def bangalore_pincode():
    return "560001"


@pytest.fixture
def chennai_pincode():
    return "600001"
