"""Top-level package for indiapins."""

__author__ = """Pawan Kumar Jain"""
__email__ = 'pawanjain.432@gmail.com'
__version__ = '0.1.3'

import bz2
import json
import os
import re
import sys

_valid_zipcode_length = 6
_digits = re.compile(r"[^\d]")


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
    """ Assumes pincode is of type `str` """

    if len(zipcode) != _valid_zipcode_length:
        raise ValueError(
            'Invalid format, pincode must be of the format: "######"'
        )

    if bool(_digits.search(zipcode)):
        raise ValueError('Invalid characters, pincode may only contain digits')

    return zipcode


def _resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder nad stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


_zips_json = _resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pins.json.bz2"))
with bz2_open(_zips_json, "rt") as f:
    _zips = [json.loads(line) for i, line in enumerate(f)]


@_clean_zipcode
def matching(zipcode, zips=None):
    """ Retrieve zipcode dict for provided pincode """
    if zips is None:
        zips = _zips

    return [z for z in zips if z['Pincode'] == zipcode]


@_clean_zipcode
def isvalid(zipcode):
    return bool(matching(zipcode))


@_clean_zipcode
def districtmatch(zipcode, zips=None):
    if zips is None:
        zips = _zips

    districts = list(set([z['District'] for z in zips if z['Pincode'] == zipcode]))

    if len(districts) == 0:
        raise ValueError('Invalid Pincode, Pincode not in database')
    else:
        return ', '.join(districts)
